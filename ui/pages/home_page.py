import allure
from playwright.sync_api import Page
from config import UI_BASE_URL
from ui.pages.base_page import BasePage
from ui.pages.results_page import ResultsPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._from_port = page.locator("select[name='fromPort']")
        self._to_port = page.locator("select[name='toPort']")
        self._find_flights_btn = page.locator("input[value='Find Flights']")

    @allure.step("Open home page")
    def open(self) -> None:
        self.navigate_to(UI_BASE_URL)

    @allure.step("Search flights: {departure} → {destination}")
    def search_flights(self, departure: str, destination: str) -> ResultsPage:
        self._from_port.select_option(departure)
        self._to_port.select_option(destination)
        self._find_flights_btn.click()
        self.wait_for_url("**/reserve.php")
        return ResultsPage(self.page)
