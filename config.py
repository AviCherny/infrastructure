import os

UI_BASE_URL = os.getenv("UI_BASE_URL", "https://blazedemo.com")
API_BASE_URL = os.getenv("API_BASE_URL", "https://airportgap.com/api")

# Parallel execution — override with WORKERS=4 pytest ... or set to 1 to disable
WORKERS = int(os.getenv("WORKERS", "2"))

# Playwright
PLAYWRIGHT_HEADLESS = os.getenv("HEADLESS", "true") == "true"
PLAYWRIGHT_TIMEOUT = 15_000
PLAYWRIGHT_VIDEO_DIR = "videos/"
PLAYWRIGHT_TRACE_DIR = "traces/"
