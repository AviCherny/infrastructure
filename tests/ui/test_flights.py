import pytest
import allure
from dataclasses import replace
from ui.pages.home_page import HomePage
import ui.flows as flows


@pytest.mark.ui
@allure.feature("Flights")
@allure.story("Search")
def test_search_for_flight_returns_relevant_results(page):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")

    # The results heading must reflect the searched route — not just any page
    heading = results.get_heading()
    assert "Boston" in heading
    assert "Rome" in heading
    assert results.get_flight_count() > 0


@pytest.mark.ui
@allure.feature("Flights")
@allure.story("Select flight")
def test_select_flight_reaches_purchase_page_for_correct_trip(page):
    results = flows.search_flights(page, "Boston", "Rome")
    purchase = results.choose_flight(0)

    # The purchase page must confirm the trip the user actually selected
    summary = purchase.get_trip_summary()
    assert "Boston" in summary
    assert "Rome" in summary


@pytest.mark.ui
@allure.feature("Flights")
@allure.story("Purchase")
def test_complete_purchase_flow_returns_booking_confirmation(page, default_passenger):
    results = flows.search_flights(page, "Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(default_passenger)

    # A booking was successfully created — the system returned a unique ID
    assert "Thank you" in confirmation.get_title()
    booking_id = confirmation.get_booking_id()
    assert booking_id and booking_id.strip()


@pytest.mark.ui
@allure.feature("Flights")
@allure.story("Purchase")
def test_purchase_with_different_cardholder_returns_booking_confirmation(page, default_passenger):
    passenger = replace(default_passenger, name="Jane Smith", name_on_card="Jane Smith")

    results = flows.search_flights(page, "Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(passenger)

    # Booking must succeed even when cardholder name differs from default
    assert "Thank you" in confirmation.get_title()
    booking_id = confirmation.get_booking_id()
    assert booking_id and booking_id.strip()
