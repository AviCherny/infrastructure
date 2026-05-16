import logging
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        page.on("console", self._on_console)

    def _on_console(self, msg):
        if msg.type == "error":
            logging.error(f"[Browser Console Error] {msg.text}")
