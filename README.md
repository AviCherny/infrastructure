# Infrastructure — Automation Framework

A Python-based test automation framework covering API and UI testing, built for learning, interview preparation, and as a reusable foundation.

**Targets:**
- API: [AirportGap API](https://airportgap.com/api)
- UI: [BlazeDemo](https://blazedemo.com)

**Live Allure Report:** https://avicherny.github.io/infrastructure/

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Test runner | pytest |
| API testing | requests |
| UI testing | Playwright |
| Reporting | Allure |
| CI | GitHub Actions |

---

## Project Structure

```
infrastructure/
├── api/
│   ├── clients/          # One class per API resource (airports, distances)
│   └── builders/         # URL and request body construction
├── ui/
│   └── pages/            # Page Object classes (one file per page)
├── tests/
│   ├── api/              # API test files + conftest
│   └── ui/               # UI test files + conftest
├── config.py             # Base URLs and environment settings
├── requirements.txt
├── pytest.ini
└── .github/workflows/    # CI pipeline
```

---

## Setup

**Prerequisites:** Python 3.12+

```bash
# Clone the repo
git clone https://github.com/AviCherny/infrastructure.git
cd infrastructure

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

---

## Running Tests

```bash
# All tests
pytest

# API tests only
pytest -m api

# UI tests only
pytest -m ui
```

### Environment overrides

Base URLs default to production. Override via environment variables:

```bash
UI_BASE_URL=https://blazedemo.com pytest -m ui
API_BASE_URL=https://airportgap.com/api pytest -m api
```

---

## Allure Report

### Locally

```bash
# Run tests and collect results
pytest --alluredir=allure-results

# Generate and open the report
allure serve allure-results
```

> Requires Allure CLI: `npm install -g allure-commandline`

### CI (GitHub Actions)

Every push to `main` runs the full test suite and publishes the Allure report to GitHub Pages.

Report: https://avicherny.github.io/infrastructure/

The workflow also uploads the report as an artifact (retained for 14 days) under the **Actions** tab.

---

## Design Principles

**UI/API separation — run independently, fail independently**
UI tests fail due to browser rendering and navigation timing. API tests fail due to contracts and data. Mixing them means a flaky UI test can mask a real API regression. Keeping them separate lets each layer be run, debugged, and extended without touching the other.

**No base classes until two or more concrete classes share real logic**
A base class created too early locks in assumptions before you understand the real commonality. The cost of adding one later is low. The cost of ripping out a wrong one is high.

**No utility folders unless three or more files need the same function**
A `utils/` folder is where code goes to become invisible. If only one file needs a helper, the helper lives there. If two need it, it moves when the third appears — not before.

**Smallest working solution first — abstractions are added when the signal appears, not before**
Every abstraction has a maintenance cost. A `BodyBuilder`, a URL builder, a Page Object — each one is justified by repeated use. The rule is: build the concrete thing, then extract the pattern when you see it twice.
