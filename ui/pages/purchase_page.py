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
        self.trip_summary = page.locator("h2")
        self.name = page.locator("#inputName")
        self.address = page.locator("#address")
        self.city = page.locator("#city")
        self.state = page.locator("#state")
        self.zip_code = page.locator("#zipCode")
        self.card_type = page.locator("select[name='cardType']")
        self.credit_card_number = page.locator("#creditCardNumber")
        self.credit_card_month = page.locator("#creditCardMonth")
        self.credit_card_year = page.locator("#creditCardYear")
        self.name_on_card = page.locator("#nameOnCard")
        self.purchase_btn = page.locator("input[value='Purchase Flight']")

    def fill_and_submit(self, details: PassengerDetails):
        self.name.fill(details.name)
        self.address.fill(details.address)
        self.city.fill(details.city)
        self.state.fill(details.state)
        self.zip_code.fill(details.zip_code)
        self.card_type.select_option(details.card_type)
        self.credit_card_number.fill(details.credit_card_number)
        self.credit_card_month.fill(details.credit_card_month)
        self.credit_card_year.fill(details.credit_card_year)
        self.name_on_card.fill(details.name_on_card)
        self.purchase_btn.click()
        self.page.wait_for_url("**/confirmation.php")
        return ConfirmationPage(self.page)
