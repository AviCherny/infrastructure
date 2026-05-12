# Project Context

## Purpose
- Learning automation architecture
- Interview preparation
- Reusable framework foundation

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
│   └── pages/
├── tests/
│   ├── ui/
│   └── api/
├── conftest.py
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
One client class per API resource group (e.g., `airports_client.py`, `distances_client.py`). Wraps `requests`, returns raw responses. No test logic here.
Useful immediately — AirportGap has multiple endpoints.

**`tests/ui/` and `tests/api/`**
The actual test files. Separated so you can run `pytest tests/ui` or `pytest tests/api` independently.
Useful immediately.

**`conftest.py`** (root level)
Pytest fixtures: browser setup, base URL injection, HTTP session setup. The single place for shared setup/teardown.
Useful immediately — every test needs a browser or HTTP client.

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
| `base/` classes (BasePage, BaseClient) | Only create when 2+ pages/clients share real logic. Don't pre-build inheritance. |
| `models/` or `schemas/` | Only needed when validating complex response shapes. |
| `data/` or `fixtures/json/` | Only when test data management becomes a real problem. |
| `components/` inside `ui/` | Only if a UI element is used across 3+ pages. |
| `reporters/` | Pytest plugins handle this. Don't build a custom layer. |

### The Rule
Every folder here will contain a file within the first hour of building. Nothing is "for later."
When you find yourself copy-pasting the same logic across 2-3 files, that's the signal to add the next abstraction — not before.
