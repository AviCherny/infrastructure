from playwright.sync_api import Page
from config import UI_BASE_URL
from ui.pages.base_page import BasePage
from ui.pages.results_page import ResultsPage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.from_port = page.locator("select[name='fromPort']")
        self.to_port = page.locator("select[name='toPort']")
        self.find_flights_btn = page.locator("input[value='Find Flights']")

    def open(self):
        self.page.goto(UI_BASE_URL)

    def search_flights(self, departure: str, destination: str):
        self.from_port.select_option(departure)
        self.to_port.select_option(destination)
        self.find_flights_btn.click()
        self.page.wait_for_url("**/reserve.php")
        return ResultsPage(self.page)
