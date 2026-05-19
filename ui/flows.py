import allure
from playwright.sync_api import Page
from ui.pages.home_page import HomePage
from ui.pages.results_page import ResultsPage


@allure.step("Search flights: {departure} → {destination}")
def search_flights(page: Page, departure: str, destination: str) -> ResultsPage:
    home = HomePage(page)
    home.open()
    return home.search_flights(departure, destination)
