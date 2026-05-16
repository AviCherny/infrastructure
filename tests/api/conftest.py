import pytest
import requests
from api.clients.airports_client import get_airports


@pytest.fixture(scope="session")
def session():
    with requests.Session() as s:
        s.headers.update({"Content-Type": "application/json"})
        yield s


@pytest.fixture(scope="session")
def airports_data(session):
    return get_airports(session).json()["data"]
