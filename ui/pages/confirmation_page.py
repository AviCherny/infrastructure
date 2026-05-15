from playwright.sync_api import Page


class ConfirmationPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("h1")
        self.booking_id = page.locator("table tbody tr:nth-child(1) td:nth-child(2)")

    def get_title(self) -> str:
        return self.title.inner_text()

    def get_booking_id(self) -> str:
        return self.booking_id.inner_text()
