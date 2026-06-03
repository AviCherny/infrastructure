# Infrastructure — Test Automation Framework

[Live Allure Report →](https://avicherny.github.io/infrastructure/)

A layered Python automation framework covering API, UI, and E2E testing — built to demonstrate production-grade architecture decisions, not just passing tests.

---

## What This Demonstrates

- Tests that read like specs — no URLs, HTTP verbs, or raw dicts in test files
- Layered architecture: Test → Client → Builder and Test → Flow → Page, each layer with a single responsibility
- Reusable fixtures: session-scoped HTTP session, function-scoped browser contexts, pre-navigated UI fixture
- Automatic failure diagnostics: screenshot, video, Playwright trace, and console errors — captured on every failure, published to Allure
- Parallel execution controlled from config, with full test isolation across workers
- `smoke` / `regression` markers for selective execution at different stages of a CI pipeline
- Allure report always published — even when tests fail, which is when it matters most
- Design rationale documented in [DESIGN.md](DESIGN.md) — decisions, tradeoffs, and what was intentionally not built

---

## Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.12 |
| Test runner | pytest + pytest-xdist |
| API | requests |
| UI | Playwright |
| Reporting | Allure |
| CI/CD | GitHub Actions → GitHub Pages |

---

## Architecture

**API layer**
```
Test → Client → URL Builder + Body Builder + Session
```
Clients own the HTTP method. The URL builder is the single source of truth for all endpoints. Payloads go through a chainable `BodyBuilder` — no plain dicts, no silent key typos.

**UI layer**
```
Test → Flow → Page Object → Base Page
```
Each page action returns the next page in the flow. Selectors live only in page classes. Tests never break for infrastructure reasons.

**Test markers**

| Marker | Purpose |
|--------|---------|
| `@pytest.mark.api` | Contract validation — status codes, response structure, data integrity, response times |
| `@pytest.mark.ui` | Browser behavior — user flows, page transitions |
| `@pytest.mark.e2e` | API sets preconditions, UI asserts the user-facing result |
| `@pytest.mark.smoke` | Critical path — confirms the system is alive; 5 tests, runs in seconds |
| `@pytest.mark.regression` | Full coverage — edge cases, validation, error handling |

---

## Project Structure

```
infrastructure/
├── api/
│   ├── clients/               # airports_client.py, distances_client.py
│   └── builders/              # url_builder.py, body_builder.py
├── ui/
│   ├── pages/                 # base_page, home, results, purchase, confirmation
│   └── flows.py               # reusable multi-step user journeys
├── tests/
│   ├── conftest.py            # session-scoped HTTP session, Allure hook, register_cleanup
│   ├── api/                   # test_airports.py, test_distances.py, test_data.py
│   └── ui/                    # test_flights.py, test_api_then_ui.py, test_failure_demo.py
├── config.py                  # base URLs, Playwright settings, worker count — all env-overridable
├── pytest.ini                 # markers, timeout, log format
├── allure-categories.json     # classifies failures: product defect vs infrastructure problem
├── DESIGN.md                  # architecture decisions and rationale
└── .github/workflows/         # parallel CI: api-tests + ui-tests → report → deploy
```

**Targets:** API tests run against [AirportGap](https://airportgap.com/api). UI and E2E tests run against [BlazeDemo](https://blazedemo.com). Both are public demo apps — the framework design is the deliverable.

---

## Setup

```bash
git clone https://github.com/AviCherny/infrastructure.git
cd infrastructure

python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
playwright install chromium
```

---

## Running Tests

```bash
pytest                  # full suite, parallel (2 workers by default)
pytest -m api           # API tests only
pytest -m ui            # UI tests only
pytest -m e2e           # E2E tests only
pytest -m smoke         # 5 critical-path tests — fast health check
pytest -m regression    # edge cases, validation, error handling
```

**Parallel execution:**

```bash
WORKERS=4 pytest        # run with 4 workers
WORKERS=1 pytest        # disable parallelism (serial, live logs)
pytest -n 0             # same as WORKERS=1 — useful for debugging
```

**Environment overrides:**

```bash
API_BASE_URL=https://airportgap.com/api pytest -m api
UI_BASE_URL=https://blazedemo.com pytest -m ui
HEADED=true pytest -m ui          # run browser in headed mode
```

---

## CI/CD

Every push to `main` triggers two parallel jobs — API tests and UI + E2E tests — followed by report generation and deploy.

The Allure report is **always published**, regardless of test outcome. Allure categories automatically classify failures as product defects or infrastructure problems. On failure, the Playwright trace is attached directly to Allure — download the zip and open with `playwright show-trace trace.zip`, or upload to [trace.playwright.dev](https://trace.playwright.dev) with no installation required.

[View live report →](https://avicherny.github.io/infrastructure/)

---

*Built by [Avi Cherny](https://www.linkedin.com/in/avi-c-83013238/)*
