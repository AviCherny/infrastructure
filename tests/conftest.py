import json
import logging
import pytest
import requests
import allure


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
