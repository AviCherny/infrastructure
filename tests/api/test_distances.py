import pytest
from api.clients.distances_client import post_distance


@pytest.mark.api
def test_post_distance_returns_200(session):
    response = post_distance(session, "KIX", "SYD")

    assert response.status_code == 200


@pytest.mark.api
def test_post_distance_returns_distance_data(session):
    response = post_distance(session, "KIX", "SYD")
    data = response.json()["data"]

    assert data["type"] == "airport_distance"
    assert "kilometers" in data["attributes"]
    assert "miles" in data["attributes"]
    assert "nautical_miles" in data["attributes"]


@pytest.mark.api
def test_post_distance_value_is_positive(session):
    response = post_distance(session, "KIX", "SYD")
    attributes = response.json()["data"]["attributes"]

    assert attributes["kilometers"] > 0
    assert attributes["miles"] > 0


@pytest.mark.api
def test_post_distance_includes_airport_details(session):
    response = post_distance(session, "KIX", "SYD")
    attributes = response.json()["data"]["attributes"]

    assert attributes["from_airport"]["iata"] == "KIX"
    assert attributes["to_airport"]["iata"] == "SYD"
