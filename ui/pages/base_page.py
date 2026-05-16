from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._console_errors: list[str] = []
        page.on("console", lambda msg: self._console_errors.append(msg.text) if msg.type == "error" else None)

    def get_console_errors(self) -> list[str]:
        return self._console_errors
