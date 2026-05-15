import re
import pytest
import allure
from api.clients.airports_client import get_airports, get_airport


@pytest.mark.api
@allure.feature("Airports")
@allure.story("Get all airports")
def test_get_airports_returns_list(session):
    response = get_airports(session)
    data = response.json()["data"]

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.api
@allure.feature("Airports")
@allure.story("Get all airports")
def test_get_airports_iata_codes_are_valid(session):
    airports = get_airports(session).json()["data"]

    for airport in airports:
        # IATA codes are always 3 uppercase letters
        assert re.match(r"^[A-Z]{3}$", airport["id"]), f"Invalid IATA: {airport['id']}"
        # id and iata attribute must stay in sync — separate DB fields that can drift
        assert airport["id"] == airport["attributes"]["iata"]


@pytest.mark.api
@allure.feature("Airports")
@allure.story("Get all airports")
def test_get_airports_item_has_expected_fields(session):
    response = get_airports(session)
    airport = response.json()["data"][0]

    assert airport["id"]
    assert airport["type"] == "airport"
    assert "name" in airport["attributes"]
    assert "iata" in airport["attributes"]
    assert "country" in airport["attributes"]


@pytest.mark.api
@allure.feature("Airports")
@allure.story("Get airport by ID")
def test_get_airport_by_id_returns_correct_airport(session):
    response = get_airport(session, "KIX")
    airport = response.json()["data"]

    assert response.status_code == 200
    assert airport["id"] == "KIX"
    assert airport["attributes"]["iata"] == "KIX"
    assert "name" in airport["attributes"]
    assert "country" in airport["attributes"]


@pytest.mark.api
@allure.feature("Airports")
@allure.story("Get airport by ID")
def test_get_airport_invalid_id_returns_404(session):
    response = get_airport(session, "INVALID")

    assert response.status_code == 404
