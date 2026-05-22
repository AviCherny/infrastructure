import pytest
import allure
from api.clients.airports_client import get_airport
from ui.pages.home_page import HomePage


@pytest.mark.e2e
@allure.feature("E2E")
@allure.story("API-verified route is searchable in the UI")
def test_api_verified_airports_are_searchable_in_ui(session, page):
    # Step 1 — API: confirm both airports exist and are valid
    boston = get_airport(session, "BOS").json()["data"]
    rome = get_airport(session, "FCO").json()["data"]
    assert boston["attributes"]["iata"] == "BOS"
    assert rome["attributes"]["iata"] == "FCO"

    # Step 2 — UI: search for a flight on that route and verify results load
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")

    assert results.get_flight_count() > 0
