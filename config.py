import os

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://blazedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://airportgap.com/api")

# Playwright
PLAYWRIGHT_HEADLESS = os.getenv("CI") == "true"
PLAYWRIGHT_TIMEOUT = 15_000
PLAYWRIGHT_VIDEO_DIR = "videos/"
PLAYWRIGHT_TRACE_DIR = "traces/"
