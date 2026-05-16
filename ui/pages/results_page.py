from playwright.sync_api import Page
from ui.pages.purchase_page import PurchasePage


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self._heading = page.locator("h3")
        self._flight_rows = page.locator("table tbody tr")

    def get_heading(self) -> str:
        return self._heading.inner_text()

    def get_flight_count(self) -> int:
        return self._flight_rows.count()

    def choose_flight(self, index: int = 0):
        self._flight_rows.nth(index).locator("input[value='Choose This Flight']").click()
        self.page.wait_for_url("**/purchase.php")
        return PurchasePage(self.page)
