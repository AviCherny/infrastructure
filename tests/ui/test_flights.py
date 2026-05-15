import pytest
from dataclasses import replace
from ui.pages.home_page import HomePage


@pytest.mark.ui
def test_search_for_flight_returns_relevant_results(page):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")

    # The results heading must reflect the searched route — not just any page
    assert "Boston" in results.heading.inner_text()
    assert "Rome" in results.heading.inner_text()
    assert results.flight_rows.count() > 0


@pytest.mark.ui
def test_select_flight_reaches_purchase_page_for_correct_trip(page):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")
    purchase = results.choose_flight(0)

    # The purchase page must confirm the trip the user actually selected
    summary = purchase.trip_summary.inner_text()
    assert "Boston" in summary
    assert "Rome" in summary


@pytest.mark.ui
def test_complete_purchase_flow_returns_booking_confirmation(page, default_passenger):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(default_passenger)

    # A booking was successfully created — the system returned a unique ID
    assert "Thank you" in confirmation.get_title()
    booking_id = confirmation.get_booking_id()
    assert booking_id and booking_id.strip()


@pytest.mark.ui
def test_purchase_with_different_cardholder_returns_booking_confirmation(page, default_passenger):
    passenger = replace(default_passenger, name="Jane Smith", name_on_card="Jane Smith")

    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(passenger)

    # Booking must succeed even when cardholder name differs from default
    assert "Thank you" in confirmation.get_title()
    booking_id = confirmation.get_booking_id()
    assert booking_id and booking_id.strip()
