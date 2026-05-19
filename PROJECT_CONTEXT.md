# Project Context

## Purpose
- Interview preparation and home assignment submission
- Reusable framework foundation
- Demonstration of real-world automation patterns

## Tech Stack
- Python
- Pytest
- Playwright (UI)
- requests (API)

## Targets
- UI: BlazeDemo
- API: AirportGap API

## Design Principles
- Scalable but simple
- Maintainable
- Interview-friendly
- Clean UI/API separation
- Real-world patterns without overengineering
- No enterprise complexity
- No unnecessary abstractions
- No generic utility classes

---

## Step 1: Folder Structure

```
infrastructure/
├── api/
│   ├── clients/
│   └── builders/
├── ui/
│   ├── pages/
│   └── flows.py
├── tests/
│   ├── ui/
│   │   └── conftest.py
│   └── api/
│       └── conftest.py
├── config.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

### Folder Responsibilities

**`ui/pages/`**
Page Object classes. One file per page (e.g., `home_page.py`, `results_page.py`). Holds locators and page-specific actions. No assertions here — tests assert, pages act.
Useful immediately — BlazeDemo has at least 3 distinct pages.

**`api/clients/`**
One module per API resource group (e.g., `airports_client.py`, `distances_client.py`). Wraps `requests`, returns raw responses. No test logic here.
Useful immediately — AirportGap has multiple endpoints.

**`tests/ui/` and `tests/api/`**
The actual test files. Separated so you can run `pytest tests/ui` or `pytest tests/api` independently.
Useful immediately.

**`tests/api/conftest.py`**
API fixtures: session-scoped `requests.Session` with shared headers and Allure response hook.

**`tests/ui/conftest.py`**
UI fixtures: session-scoped browser, per-test page context with failure-only video/trace/screenshot capture.

**`config.py`**
Base URLs, environment settings, any top-level constants. A flat file, not a class hierarchy.
Useful immediately — referenced in both clients and fixtures.

**`pytest.ini`**
Markers, test paths, output format. Keeps CLI commands short.
Useful immediately.

### What NOT to Add Yet

| What | Why not |
|---|---|
| `utils/` or `helpers/` | Generic utility folders become dumping grounds. Add only when 3+ files need the same function. |
| `BaseClient` | No shared logic across clients yet — add only when two clients repeat the same pattern. |
| `models/` or `schemas/` | Only needed when validating complex response shapes. |
| `data/` or `fixtures/json/` | Only when test data management becomes a real problem. |
| `components/` inside `ui/` | Only if a UI element is used across 3+ pages. |
| `reporters/` | Pytest plugins handle this. Don't build a custom layer. |

### The Rule
Every folder here will contain a file within the first hour of building. Nothing is "for later."
When you find yourself copy-pasting the same logic across 2-3 files, that's the signal to add the next abstraction — not before.
