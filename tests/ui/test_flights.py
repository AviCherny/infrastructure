import pytest
from ui.pages.home_page import HomePage
from ui.pages.purchase_page import PassengerDetails


@pytest.mark.ui
def test_search_for_flight(page):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")

    assert results.flight_rows.count() > 0


@pytest.mark.ui
def test_select_flight(page):
    home = HomePage(page)
    home.open()
    results = home.search_flights("Boston", "Rome")
    purchase = results.choose_flight(0)

    assert purchase.name.is_visible()
    assert purchase.purchase_btn.is_visible()


@pytest.mark.ui
def test_complete_purchase_flow(page):
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

    assert "Thank you" in confirmation.get_title()
    assert confirmation.get_booking_id()
