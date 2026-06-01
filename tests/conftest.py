import json
import logging
import pytest
import requests
import allure
from config import WORKERS


def pytest_configure(config):
    # If pytest-xdist is installed and -n was not explicitly passed, use WORKERS from config
    try:
        if config.option.numprocesses is None:
            config.option.numprocesses = WORKERS
    except AttributeError:
        pass  # pytest-xdist not installed


def _log_response(response: requests.Response, *args, **kwargs):
    method = response.request.method
    url = response.url
    status = response.status_code
    try:
        body = json.dumps(response.json(), indent=2)
    except ValueError:
        body = response.text

    logging.info(f"[HTTP] {method} {url} → {status}")
    allure.attach(
        f"{method} {url}\nStatus: {status}\n\n{body}",
        name=f"{method} {url.split('/')[-1]} → {status}",
        attachment_type=allure.attachment_type.TEXT,
    )


@pytest.fixture(scope="session")
def session():
    with requests.Session() as s:
        s.headers.update({"Content-Type": "application/json"})
        s.hooks["response"].append(_log_response)
        logging.info("[session] HTTP session started")
        yield s


@pytest.fixture
def register_cleanup():
    """
    Register teardown callbacks that run even if the test fails mid-way.
    Always register BEFORE the action that creates state — not after:

        register_cleanup(lambda: delete_item(session, item_id))  # register first
        item_id = create_item(session, payload).json()["id"]      # act after

    Cleanups execute in reverse registration order (LIFO).
    """
    cleanups: list = []
    yield cleanups.append
    for fn in reversed(cleanups):
        fn()
