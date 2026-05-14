import pytest
import requests


@pytest.fixture
def session():
    with requests.Session() as s:
        s.headers.update({"Content-Type": "application/json"})
        yield s
