import pytest
from api.clients.distances_client import post_distance


@pytest.mark.api
def test_post_distance_returns_distance_data(session):
    response = post_distance(session, "KIX", "SYD")
    data = response.json()["data"]

    assert response.status_code == 200
    assert data["type"] == "airport_distance"
    assert isinstance(data["attributes"]["kilometers"], (int, float))
    assert isinstance(data["attributes"]["miles"], (int, float))
    assert isinstance(data["attributes"]["nautical_miles"], (int, float))


@pytest.mark.api
def test_post_distance_unit_relationship_is_correct(session):
    attrs = post_distance(session, "KIX", "SYD").json()["data"]["attributes"]

    # 1 km = 0.621 miles = 0.540 nautical miles → km is always the largest value
    assert attrs["kilometers"] > attrs["miles"] > attrs["nautical_miles"]


@pytest.mark.api
def test_post_distance_is_symmetric(session):
    km_forward = post_distance(session, "KIX", "SYD").json()["data"]["attributes"]["kilometers"]
    km_reverse = post_distance(session, "SYD", "KIX").json()["data"]["attributes"]["kilometers"]

    assert km_forward == km_reverse


@pytest.mark.api
def test_post_distance_includes_airport_details(session):
    attributes = post_distance(session, "KIX", "SYD").json()["data"]["attributes"]

    assert attributes["from_airport"]["iata"] == "KIX"
    assert attributes["to_airport"]["iata"] == "SYD"


@pytest.mark.api
def test_post_distance_invalid_airport_returns_error(session):
    response = post_distance(session, "INVALID", "SYD")

    assert response.status_code == 422
