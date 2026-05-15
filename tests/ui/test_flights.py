import pytest
from ui.pages.home_page import HomePage
from ui.pages.purchase_page import PassengerDetails


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
def test_complete_purchase_flow_returns_booking_confirmation(page):
    details = PassengerDetails(
        name="John Doe",
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701",
        card_type="visa",
        credit_card_number="4111111111111111",
        credit_card_month="12",
        credit_card_year="2027",
        name_on_card="John Doe",
    )

    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(details)

    # A booking was successfully created — the system returned a unique ID
    assert "Thank you" in confirmation.get_title()
    booking_id = confirmation.get_booking_id()
    assert booking_id and booking_id.strip()
