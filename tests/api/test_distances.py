import pytest
import allure
from api.clients.distances_client import (
    post_distance,
    distance_payload,
    distance_payload_missing_from,
    distance_payload_missing_to,
    empty_distance_payload,
)
from tests.api.test_data import FROM_AIRPORT, TO_AIRPORT


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Calculate distance")
def test_post_distance_returns_distance_data(session):
    response = post_distance(session, distance_payload(FROM_AIRPORT, TO_AIRPORT))
    data = response.json()["data"]

    assert response.status_code == 200
    assert data["type"] == "airport_distance"
    assert isinstance(data["attributes"]["kilometers"], (int, float))
    assert isinstance(data["attributes"]["miles"], (int, float))
    assert isinstance(data["attributes"]["nautical_miles"], (int, float))


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Calculate distance")
def test_post_distance_unit_relationship_is_correct(session):
    attrs = post_distance(session, distance_payload(FROM_AIRPORT, TO_AIRPORT)).json()["data"]["attributes"]

    # 1 km = 0.621 miles = 0.540 nautical miles → km is always the largest value
    assert attrs["kilometers"] > attrs["miles"] > attrs["nautical_miles"]


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Calculate distance")
def test_post_distance_is_symmetric(session):
    km_forward = post_distance(session, distance_payload(FROM_AIRPORT, TO_AIRPORT)).json()["data"]["attributes"]["kilometers"]
    km_reverse = post_distance(session, distance_payload(TO_AIRPORT, FROM_AIRPORT)).json()["data"]["attributes"]["kilometers"]

    assert km_forward == km_reverse


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Calculate distance")
def test_post_distance_includes_airport_details(session):
    attributes = post_distance(session, distance_payload(FROM_AIRPORT, TO_AIRPORT)).json()["data"]["attributes"]

    assert attributes["from_airport"]["iata"] == FROM_AIRPORT
    assert attributes["to_airport"]["iata"] == TO_AIRPORT


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Validation")
def test_post_distance_invalid_airport_returns_error(session):
    response = post_distance(session, distance_payload("INVALID", TO_AIRPORT))

    assert response.status_code == 422


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Validation")
def test_post_distance_missing_from_field_returns_error(session):
    response = post_distance(session, distance_payload_missing_from(TO_AIRPORT))

    assert response.status_code == 422


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Validation")
def test_post_distance_missing_to_field_returns_error(session):
    response = post_distance(session, distance_payload_missing_to(FROM_AIRPORT))

    assert response.status_code == 422


@pytest.mark.api
@allure.feature("Distances")
@allure.story("Validation")
def test_post_distance_empty_body_returns_error(session):
    response = post_distance(session, empty_distance_payload())

    assert response.status_code == 422
