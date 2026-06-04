# Design Rationale

Architectural decisions, tradeoffs, and reasoning behind this framework.
This is the document to read before touching the code.

---

## What this is

A reusable automation framework targeting two real-world services:
- **AirportGap** — REST API for airport data and distance calculations
- **BlazeDemo** — web flight booking app

Designed as a portfolio project and interview reference. Every decision here reflects how this would be built on a real team — production-minded.

---

## Technology choices

**Python + pytest**
Test code reads like English. pytest fixtures are the cleanest dependency injection model in any language. Developers reviewing tests don't need a QA background to understand them.

**Playwright**
Every action waits for the element to be ready — no manual waits. `expect()` assertions retry until the condition is met. Traces, videos, and screenshots are built in. The sync API keeps test code linear and readable.

**requests**
Explicit, no magic, battle-tested. The `Session` object gives us shared headers and a natural home for the response logging hook. Async would add complexity with no benefit for sequential contract tests.

**Allure**
When a test fails, the report shows the screenshot, video, console errors, and full API response — all in one place, without digging through CI logs. GitHub Pages makes it accessible to anyone with the link.

---

## Architecture

### Layers

```
API:  test → client → url_builder / body_builder
UI:   test → [flow →] page object → base_page
```

Each layer has one job:

| Layer | Owns | Does NOT own |
|---|---|---|
| Test | Intent, assertions | URLs, HTTP verbs, selectors, navigation |
| Client | HTTP method, endpoint routing | Payload shape, business logic |
| Builder | URL construction, payload construction | HTTP calls |
| Flow | Multi-step user journeys | Selectors, assertions |
| Page | Selectors, page-specific actions | Assertions, business logic |
| BasePage | Shared navigation + wait utilities | Page-specific behavior |

### URL builder as single source of truth

All API endpoints live in `api/builders/url_builder.py`. If the same endpoint were referenced in two places, a URL change would silently break one of them. One definition, zero drift.

### BodyBuilder for all request payloads

`BodyBuilder` wraps every payload. `{"form": "TLV"}` (wrong key) passes Python silently and produces a 422 at runtime — `BodyBuilder().set("from", "TLV")` makes the intent explicit and is easy to grep. The recursive `.build()` handles nested payloads correctly.

---

## Fixture design

### Session scope for API, function scope for UI contexts

Launching Chromium is slow (~1s). Browsers are session-scoped — one per worker process, reused across all UI tests in that worker.

Browser contexts are function-scoped — fresh cookies, storage, and history per test. This gives isolation without paying the browser launch cost per test.

API `requests.Session` is session-scoped because API tests are stateless. Shared headers are set once.

---

## Stability

Every wait is condition-based:
- Playwright auto-waits on every action (click, fill, select_option)
- `expect()` assertions retry until the condition is met or timeout
- `networkidle` on page load — JS has finished rendering before we interact
- Fresh context per test — no state leak between tests
- `data-test` attributes where available — survive CSS refactors

---

## Failure diagnostics

On any test failure, four artifacts are automatically captured:

1. **Screenshot** — attached to Allure
2. **Video** — attached to Allure (deleted on pass to save CI storage)
3. **Playwright trace** — attached to Allure and saved to `traces/<test_name>.zip`
4. **Console errors** — attached to Allure

The trace is the most powerful: step-by-step DOM snapshots, network requests, and console output. When a test fails, download the zip from Allure and open it with `playwright show-trace trace.zip` — or upload to [trace.playwright.dev](https://trace.playwright.dev) — no installation required. You see exactly what the browser saw at every step, without re-running.

`test_failure_demo.py` is an intentional `xfail(strict=True)` test that guarantees this pipeline runs on every CI push. If it somehow passes (which it never should), `strict=True` breaks the CI build — the diagnostic pipeline is tested continuously, not just when a real test happens to fail.

---

## Parallel execution

`pytest-xdist` runs tests across multiple worker processes. Worker count is controlled by `WORKERS` in `config.py` (env-overridable: `WORKERS=4 pytest ...`).

Each worker gets its own browser instance and API session — no shared state across workers. UI tests are isolated by fresh browser context per test. API tests are stateless.

CI splits API and UI into separate parallel jobs. The API job doesn't install Playwright browsers; the UI job doesn't run API tests. Wall-clock CI time is determined by the slower job, not their sum.

---

## CI/CD design

```
api-tests ──┐
            ├──→ report (always) ──→ deploy (always, main only)
ui-tests  ──┘
```

Key decisions:

**Report always runs.** `if: always()` on the report job means Allure generates and deploys even when tests fail. This is when you need the report most — debugging a CI failure without a report is painful.

**Deploy always runs on main.** The report is published regardless of pass/fail status. The test job exit code correctly signals failure in CI; the report is an artifact, not a quality gate.

**Allure categories** classify failures automatically: product defects (AssertionError), infrastructure problems (other exceptions), known issues (xfail). This makes triage faster when multiple tests fail.


**E2E tests run in the UI job.** They need Playwright installed; the API job does not install it. Tests marked `e2e` run alongside `ui` tests.

---

## Scope decisions

**Docker**
Solo project, no team environment consistency problem to solve. `pip install -r requirements.txt && playwright install` is sufficient. Docker would add image maintenance overhead with no benefit.

**Cross-browser testing**
BlazeDemo doesn't expose browser-specific bugs. Parametrizing over Chromium/Firefox/WebKit would triple UI test count and CI time for zero defect signal at this scope.

**pytest-rerunfailures (automatic retry)**
Flaky tests get fixed, not retried. Automatic retry masks the root cause.

**Pydantic for schema validation**
TypedDict is the right tool for asserting API response shape in contract tests. Pydantic's value (parsing, coercion, nested validation, error formatting) belongs in application code that consumes and transforms data — not in test assertions that check structure.
