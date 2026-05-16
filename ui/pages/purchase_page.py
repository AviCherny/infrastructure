from dataclasses import dataclass
from playwright.sync_api import Page
from ui.pages.confirmation_page import ConfirmationPage


@dataclass
class PassengerDetails:
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    card_type: str
    credit_card_number: str
    credit_card_month: str
    credit_card_year: str
    name_on_card: str


class PurchasePage:
    def __init__(self, page: Page):
        self.page = page
        self._trip_summary = page.locator("h2")
        self._name = page.locator("#inputName")
        self._address = page.locator("#address")
        self._city = page.locator("#city")
        self._state = page.locator("#state")
        self._zip_code = page.locator("#zipCode")
        self._card_type = page.locator("select[name='cardType']")
        self._credit_card_number = page.locator("#creditCardNumber")
        self._credit_card_month = page.locator("#creditCardMonth")
        self._credit_card_year = page.locator("#creditCardYear")
        self._name_on_card = page.locator("#nameOnCard")
        self._purchase_btn = page.locator("input[value='Purchase Flight']")

    def get_trip_summary(self) -> str:
        return self._trip_summary.inner_text()

    def fill_and_submit(self, details: PassengerDetails):
        self._name.fill(details.name)
        self._address.fill(details.address)
        self._city.fill(details.city)
        self._state.fill(details.state)
        self._zip_code.fill(details.zip_code)
        self._card_type.select_option(details.card_type)
        self._credit_card_number.fill(details.credit_card_number)
        self._credit_card_month.fill(details.credit_card_month)
        self._credit_card_year.fill(details.credit_card_year)
        self._name_on_card.fill(details.name_on_card)
        self._purchase_btn.click()
        self.page.wait_for_url("**/confirmation.php")
        return ConfirmationPage(self.page)
