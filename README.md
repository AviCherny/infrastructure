# Infrastructure — Test Automation Framework

[Live Allure Report →](https://avicherny.github.io/infrastructure/)

A layered Python automation framework covering API, UI, and E2E testing — built to demonstrate production-grade architecture decisions, not just passing tests.

---

## What This Demonstrates

- Tests that read like specs — no URLs, HTTP verbs, or raw dicts in test files
- Layered architecture: Test → Client → Builder, each layer with a single responsibility
- Reusable fixtures and session management across API and UI layers
- Automatic failure diagnostics: screenshot, video, Playwright trace, and console errors on failure
- Page Object chaining that makes multi-step flows self-documenting
- Full CI/CD pipeline: test run → Allure report → GitHub Pages deploy

---

## Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.12 |
| Test runner | pytest |
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
Clients own the HTTP method. The URL builder is the single source of truth for all endpoints. Payloads go through a chainable `BodyBuilder` — no plain dicts, no key typos.

**UI layer**
```
Test → Flow → Page Object → Base Page
```
Each page action returns the next page in the flow. Selectors live only in page classes. Tests never break for infrastructure reasons.

**Test layers**

| Marker | Purpose |
|--------|---------|
| `@pytest.mark.api` | Contract validation — status codes, response structure, data integrity |
| `@pytest.mark.ui` | Browser behavior — user flows, page transitions |
| `@pytest.mark.e2e` | API sets preconditions, UI asserts the user-facing result |

---

## Project Structure

```
infrastructure/
├── api/
│   ├── clients/           # airports_client.py, distances_client.py
│   └── builders/          # url_builder.py, body_builder.py
├── ui/
│   ├── pages/             # base_page, home, results, purchase, confirmation
│   └── flows.py           # reusable multi-step user journeys
├── tests/
│   ├── conftest.py        # session-scoped HTTP session + Allure hook
│   ├── api/               # test_airports.py, test_distances.py, test_data.py
│   └── ui/                # test_flights.py, test_api_then_ui.py, test_data.py
├── config.py              # base URLs, env-overridable
├── pytest.ini             # markers, paths, log format
└── .github/workflows/     # CI: test → report → deploy
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
pytest            # all tests
pytest -m api     # API only
pytest -m ui      # UI only
pytest -m e2e     # E2E only
```

Environment overrides:

```bash
API_BASE_URL=https://airportgap.com/api pytest -m api
UI_BASE_URL=https://blazedemo.com pytest -m ui
HEADED=true pytest -m ui
```

---

## CI/CD

Every push to `main` triggers: **test → report → deploy**.
Allure results and Playwright traces are uploaded as artifacts. The report publishes to GitHub Pages on success.

[View live report →](https://avicherny.github.io/infrastructure/)

---

*Built by [Avi Cherny](https://www.linkedin.com/in/avi-c-83013238/)*
