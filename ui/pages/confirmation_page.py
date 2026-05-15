from playwright.sync_api import Page


class ConfirmationPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("h1")
        self.booking_id = page.locator("tr", has=page.locator("td", has_text="Id")).locator("td").nth(1)

    def get_title(self) -> str:
        return self.title.inner_text()

    def get_booking_id(self) -> str:
        return self.booking_id.inner_text()
