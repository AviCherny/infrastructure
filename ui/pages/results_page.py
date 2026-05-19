import allure
from playwright.sync_api import Page
from ui.pages.base_page import BasePage
from ui.pages.purchase_page import PurchasePage


class ResultsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._heading = page.get_by_role("heading", level=3)
        self._flight_rows = page.get_by_role("row").filter(has=page.locator("input[value='Choose This Flight']"))

    def get_heading(self) -> str:
        return self._heading.inner_text()

    def get_flight_count(self) -> int:
        return self._flight_rows.count()

    @allure.step("Choose flight #{index}")
    def choose_flight(self, index: int = 0):
        self._flight_rows.nth(index).locator("input[value='Choose This Flight']").click()
        self.wait_for_url("**/purchase.php")
        return PurchasePage(self.page)
