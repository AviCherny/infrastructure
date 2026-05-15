from playwright.sync_api import Page


class ResultsPage:
    def __init__(self, page: Page):
        self.page = page
        self.flight_rows = page.locator("table tbody tr")

    def choose_flight(self, index: int = 0):
        from ui.pages.purchase_page import PurchasePage
        self.flight_rows.nth(index).locator("input[value='Choose This Flight']").click()
        self.page.wait_for_url("**/purchase.php")
        return PurchasePage(self.page)
