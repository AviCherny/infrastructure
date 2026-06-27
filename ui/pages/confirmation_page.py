from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class ConfirmationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._title = page.locator("h1")
        self._booking_id = page.locator("tr", has=page.locator("td", has_text="Id")).locator("td").nth(1)

    def get_title(self) -> str:
        return self._title.inner_text()

    def get_booking_id(self) -> str:
        return self._booking_id.inner_text()
