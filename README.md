# Infrastructure — Test Automation Framework

[![Tests](https://github.com/AviCherny/infrastructure/actions/workflows/tests.yml/badge.svg)](https://github.com/AviCherny/infrastructure/actions)

A Python test automation framework with layered architecture, covering API, UI, and cross-layer E2E testing.
Built as a reusable foundation that demonstrates real-world automation patterns — the kind of framework you'd hand off to a team and it just works.

**[Live Allure Report](https://avicherny.github.io/infrastructure/)**

---

## What Makes This Framework Notable

- **Tests read like specs** — no URLs, no HTTP verbs, no raw dicts in test files
- **Three isolated test layers** — API, UI, and E2E, each with a clear boundary and its own marker
- **Automatic failure diagnostics** — screenshot, video, Playwright trace, and console errors attached on failure; discarded on success
- **Layered architecture** — Test → Client → Builder, each layer with a single responsibility
- **Page Object chaining** — page actions return the next page, making flows self-documenting
- **CI/CD pipeline** — GitHub Actions runs tests, generates Allure report, deploys to GitHub Pages
- **Known bugs documented, not hidden** — `xfail(strict=True)` flags real issues and breaks if they're silently fixed

---

## Targets

| Layer | Target | Purpose |
|-------|--------|---------|
| API | [AirportGap](https://airportgap.com/api) | REST API — airport data, distance calculations, input validation |
| UI | [BlazeDemo](https://blazedemo.com) | Flight booking — search, select, purchase, confirmation |
| E2E | Both | API verifies preconditions, UI asserts the user-facing result |

The targets are public demo apps. The framework design is the deliverable.

---

## Tech Stack

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

### API test flow

```
Test file            expresses intent only — what to verify, not how
  └── Client          one function per API action, owns the HTTP method
        ├── URL builder      single source of truth for all API URLs
        ├── Body builder     chainable payload construction, prevents key typos
        └── Session          shared headers + automatic Allure response logging
```

### UI test flow

```
Test file            asserts user-visible behavior
  └── Flow            composes multi-step journeys from page actions
        └── Page Object    owns selectors, returns the next page in the flow
              └── Base Page      shared navigation and wait logic
```

Each layer has one job. When a URL changes, one file changes. When a selector changes, one page class changes. Tests never break for infrastructure reasons.

> Full architecture rationale: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Project Structure

```
infrastructure/
├── api/
│   ├── clients/
│   │   ├── airports_client.py        # get_airports, get_airport
│   │   └── distances_client.py       # post_distance, distance_payload
│   └── builders/
│       ├── url_builder.py            # All API URLs — single source of truth
│       └── body_builder.py           # Chainable builder with nested support
├── ui/
│   ├── pages/
│   │   ├── base_page.py              # navigate_to, wait_for_url
│   │   ├── home_page.py              # Search flights (departure → destination)
│   │   ├── results_page.py           # Flight listing + choose_flight → PurchasePage
│   │   ├── purchase_page.py          # Passenger form + PassengerDetails dataclass
│   │   └── confirmation_page.py      # Booking ID extraction
│   └── flows.py                      # Reusable multi-step user journeys
├── tests/
│   ├── conftest.py                   # Session-scoped HTTP session + Allure hook
│   ├── api/
│   │   ├── test_airports.py          # List, validate IATA, get by ID, 404
│   │   ├── test_distances.py         # Distance calc, symmetry, validation errors
│   │   └── test_data.py              # Shared airport code constants
│   └── ui/
│       ├── conftest.py               # Browser, page context, failure diagnostics
│       ├── test_flights.py           # Search, select, purchase, variant flows
│       ├── test_api_then_ui.py       # E2E: API precondition → UI assertion
│       └── test_data.py              # Passenger factory with unique run prefix
├── config.py                         # Base URLs + Playwright config (env-overridable)
├── pytest.ini                        # Markers (api, ui, e2e), paths, log format
├── requirements.txt
└── .github/workflows/tests.yml       # CI: test → report → deploy
```

---

## Design Decisions

### Tests express intent, not implementation

```python
def test_complete_purchase_flow_returns_booking_confirmation(page, default_passenger):
    results = flows.search_flights(page, "Boston", "Rome")
    purchase = results.choose_flight(0)
    confirmation = purchase.fill_and_submit(default_passenger)

    assert "Thank you" in confirmation.get_title()
    assert confirmation.get_booking_id().strip()
```

No selectors. No URLs. No HTTP calls. The test describes a user journey — the framework handles the rest. If the API endpoint or a CSS selector changes, zero test files change.

### Automatic failure diagnostics

When a UI test fails, the `page` fixture captures everything needed to reproduce the issue — no test code required:

| Artifact | On failure | On success |
|----------|-----------|------------|
| Screenshot | Attached to Allure report | Not taken |
| Video | Attached to Allure report | Deleted |
| Playwright trace | Saved to `traces/` | Discarded |
| Console errors | Attached to Allure report | — |

Every failed test in CI includes a video replay, an interactive Playwright trace, a screenshot, and console errors. No local reproduction needed.

### Known bugs are documented, not hidden

```python
@pytest.mark.xfail(
    strict=True,
    reason="blazedemo.com bug: purchase page returns TLV→SFO defaults regardless of search input",
)
def test_select_flight_reaches_purchase_page_for_correct_trip(page):
```

`strict=True` means the test *fails* if the bug gets silently fixed — forcing the team to update the test and acknowledge the change. This is how production test suites handle known issues without polluting the results.

### Session management for performance

- **API:** One `requests.Session` per test session. Connection reuse, shared headers, and a response hook that automatically logs every HTTP call and attaches it to the Allure report
- **UI:** Browser launched once (session-scoped), fresh context per test (isolated cookies, storage, separate video recording)

### Page Object chaining

Each page action returns the next page in the flow:

```python
results = home.search_flights("Boston", "Rome")     # → ResultsPage
purchase = results.choose_flight(0)                   # → PurchasePage
confirmation = purchase.fill_and_submit(passenger)    # → ConfirmationPage
```

You can't call `choose_flight` without first having a `ResultsPage`. The code structure guides the correct usage.

### Builder pattern for payloads

```python
def distance_payload(from_airport: str, to_airport: str) -> dict:
    return BodyBuilder().set("from", from_airport).set("to", to_airport).build()
```

No `{"form": "TLV"}` typos. The builder is the documented interface for constructing payloads. Nested builders are supported for complex request bodies.

### Three test layers with clear boundaries

| Marker | Layer | Purpose | Command |
|--------|-------|---------|---------|
| `@pytest.mark.api` | API | Contract validation — status codes, response structure, data integrity | `pytest -m api` |
| `@pytest.mark.ui` | UI | Browser behavior — user flows, page transitions | `pytest -m ui` |
| `@pytest.mark.e2e` | E2E | Cross-layer — API sets up preconditions, UI verifies behavior | `pytest -m e2e` |

When a test fails, the layer tells you where to look. API contract broke? Browser behavior changed? Integration between them?

---

## Setup

**Prerequisites:** Python 3.12+

```bash
git clone https://github.com/AviCherny/infrastructure.git
cd infrastructure

python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
playwright install chromium
```

---

## Running Tests

```bash
pytest                # All tests
pytest -m api         # API tests only
pytest -m ui          # UI tests only
pytest -m e2e         # E2E tests only
```

### Environment Overrides

Base URLs default to production. Override for different environments:

```bash
API_BASE_URL=https://airportgap.com/api pytest -m api
UI_BASE_URL=https://blazedemo.com pytest -m ui
HEADED=true pytest -m ui          # Run with visible browser
```

---

## CI/CD Pipeline

Every push to `main` triggers a three-stage pipeline:

```
test → report → deploy
```

| Stage | What it does |
|-------|-------------|
| **Test** | Runs API and UI suites separately. Uploads Allure results and Playwright traces as artifacts |
| **Report** | Generates the Allure report from collected results |
| **Deploy** | Publishes the report to GitHub Pages (only on `main`, only if tests pass) |

---

## Allure Report

### Local

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

> Requires Allure CLI: `npm install -g allure-commandline`

### What's in the report

- Test results grouped by feature and story (`@allure.feature`, `@allure.story`)
- Every HTTP request/response automatically attached via session hook
- UI test failures include screenshot, video, trace, and console errors
- Page actions annotated with `@allure.step` for readable execution traces

**[View the live report →](https://avicherny.github.io/infrastructure/)**
