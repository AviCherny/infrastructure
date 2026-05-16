from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_url(self, pattern: str) -> None:
        self.page.wait_for_url(pattern)
