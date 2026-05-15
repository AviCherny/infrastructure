import pytest
import requests


@pytest.fixture(scope="session")
def session():
    with requests.Session() as s:
        s.headers.update({"Content-Type": "application/json"})
        yield s
