import pytest
from api.clients.airports_client import get_airports, get_airport


@pytest.mark.api
def test_get_airports_returns_200(session):
    response = get_airports(session)

    assert response.status_code == 200


@pytest.mark.api
def test_get_airports_returns_list(session):
    response = get_airports(session)
    data = response.json()["data"]

    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.api
def test_get_airports_item_has_expected_fields(session):
    response = get_airports(session)
    airport = response.json()["data"][0]

    assert airport["id"]
    assert airport["type"] == "airport"
    assert "name" in airport["attributes"]
    assert "iata" in airport["attributes"]
    assert "country" in airport["attributes"]


@pytest.mark.api
def test_get_airport_by_id_returns_200(session):
    response = get_airport(session, "KIX")

    assert response.status_code == 200


@pytest.mark.api
def test_get_airport_by_id_returns_correct_airport(session):
    response = get_airport(session, "KIX")
    airport = response.json()["data"]

    assert airport["id"] == "KIX"
    assert airport["attributes"]["iata"] == "KIX"


@pytest.mark.api
def test_get_airport_invalid_id_returns_404(session):
    response = get_airport(session, "INVALID")

    assert response.status_code == 404
