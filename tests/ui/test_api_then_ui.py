import pytest
import allure
import ui.flows as flows
from api.clients.airports_client import get_airport


@pytest.mark.e2e
@pytest.mark.smoke
@allure.feature("E2E")
@allure.story("API-verified route is searchable in the UI")
def test_api_verified_airports_are_searchable_in_ui(session, page):
    # Step 1 — API: confirm both airports exist and are valid
    boston = get_airport(session, "BOS").json()["data"]
    rome = get_airport(session, "FCO").json()["data"]
    assert boston["attributes"]["iata"] == "BOS"
    assert rome["attributes"]["iata"] == "FCO"

    # Step 2 — UI: search for a flight on that route and verify results load
    results = flows.search_flights(page, "Boston", "Rome")

    assert results.get_flight_count() > 0
