import pytest
from playwright.sync_api import sync_playwright
from ui.pages.purchase_page import PassengerDetails


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture
def default_passenger():
    return PassengerDetails(
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
