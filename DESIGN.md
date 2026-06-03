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

**Playwright (over Selenium)**
Auto-waits on every action eliminate the `time.sleep(2)` anti-pattern. `expect()` assertions retry until the condition is met. Traces, videos, and screenshots are built in — not bolt-ons. The sync API keeps test code linear and readable.

**requests (over httpx, aiohttp)**
Explicit, no magic, battle-tested. The `Session` object gives us shared headers and a natural home for the response logging hook. Async would add complexity with no benefit for sequential contract tests.

**Allure (over pytest-html)**
Rich attachment support: screenshots, videos, traces, and response bodies all land in the report with zero test-level boilerplate. The step decorator makes reports read like a user story. GitHub Pages deployment makes the report accessible without downloading artifacts.

---

## Architecture

### Layers

```
API:  test → client → url_builder + body_builder
UI:   test → flow → page object → base_page
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

**Why this matters:** When the API base URL changes, you change `url_builder.py`. When a selector breaks, you change one page object. Tests never need to change for infrastructure reasons.

### URL builder as single source of truth

All API endpoints live in `api/builders/url_builder.py`. If the same endpoint were referenced in two places, a URL change would silently break one of them. One definition, zero drift.

### BodyBuilder for all request payloads

No plain dicts in client functions. `{"form": "TLV"}` (wrong key) passes Python silently and produces a 422 at runtime. `BodyBuilder().set("from", "TLV")` makes the intent explicit and is easy to grep. The recursive `.build()` handles nested payloads correctly.

---

## Fixture design

### Session scope for API, function scope for UI contexts

Launching Chromium is slow (~1s). Browsers are session-scoped — one per worker process, reused across all UI tests in that worker.

Browser contexts are function-scoped — fresh cookies, storage, and history per test. This gives isolation without paying the browser launch cost per test.

API `requests.Session` is session-scoped because API tests are stateless. Shared headers are set once.

### home_page: pre-navigated starting point

Tests that start at the BlazeDemo home page don't repeat `home = HomePage(page); home.open()` boilerplate. The `home_page` fixture wraps the function-scoped `page` fixture — full isolation is maintained. Each test gets its own fresh browser context; the fixture just handles the navigation.

---

## Anti-flakiness strategy

Zero `time.sleep()`. Every wait is condition-based:
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
3. **Playwright trace** — saved to `traces/<test_name>.zip`, open at [trace.playwright.dev](https://trace.playwright.dev)
4. **Console errors** — attached to Allure

The trace is the most powerful: step-by-step DOM snapshots, network requests, and console output. When a test fails in CI, you can open the trace and see exactly what the browser saw at every step without re-running.

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

**Traces uploaded separately** for direct download from the CI artifacts panel, bypassing the Allure report.

**E2E tests run in the UI job.** They need Playwright installed; the API job does not install it. Tests marked `e2e` run alongside `ui` tests.

---

## What was intentionally not built

**Docker**
Solo project, no team environment consistency problem to solve. `pip install -r requirements.txt && playwright install` is sufficient. Docker would add image maintenance overhead with no benefit.

**Cross-browser testing**
BlazeDemo doesn't expose browser-specific bugs. Parametrizing over Chromium/Firefox/WebKit would triple UI test count and CI time for zero defect signal at this scope.

**pytest-rerunfailures (automatic retry)**
Automatic retry hides flakiness. A flaky test should be fixed, not retried silently. If a test is genuinely non-deterministic (network, timing), the root cause needs addressing — not masking. The only exception would be tests that exercise external services with known unreliability, and those should be explicitly marked.

**Pydantic for schema validation**
TypedDict is the right tool for asserting API response shape in contract tests. Pydantic's value (parsing, coercion, nested validation, error formatting) belongs in application code that consumes and transforms data — not in test assertions that check structure.

**Base class for clients**
Both API clients are 5–12 lines each. They share no logic that would justify a base class. Adding one would be ceremony: a parent class with no methods, existing only to be inherited. Base classes earn their place when two or more concrete classes share real, non-trivial behavior.

**Data factories (factory_boy)**
19 tests, 2 data shapes. `make_passenger()` in `test_data.py` does the job. Factory classes add a dependency, a learning curve, and an abstraction layer for something that doesn't need one at this scale.

---

## What Next

**CRUD endpoint tests**
The `register_cleanup` fixture is already in place — register the cleanup before the action that creates state, so teardown runs even if the test fails mid-way. Waiting for a writable endpoint to test against.

**Cookie injection for auth flows**
Create an auth session via API, inject the token directly into the browser context. Skips the login UI for tests that don't test authentication — faster and more reliable than navigating through the form.

**TypedDict schema assertions**
Assert API response shape structurally, not just field-by-field. A dedicated schema file catches contract breaks without adding a Pydantic dependency.

**`--env` flag**
`API_BASE_URL` and `UI_BASE_URL` are already env-overridable. One CLI option (`--env staging`) mapping to a URL set would make environment switching clean.

---

## What changes at 10x scale

**Test data ownership**
Each test creates its own user/resource via API and deletes it on teardown. Shared hardcoded IDs become a serialization bottleneck in parallel runs and a pollution risk if cleanup fails.

**Cookie injection**
Create auth sessions via API, inject the token into the browser context. Skips the login UI entirely for tests that don't test authentication. Faster, more reliable than UI-based login.

**Contract testing layer**
A dedicated suite using TypedDict schemas as the source of truth for API response shape. E2E tests are too slow and too dependent on the full stack to serve as the first line of defense against API contract breaks.

**Multiple environments**
Staging, UAT, production. `API_BASE_URL` and `UI_BASE_URL` are already env-overridable. Adding a `--env` CLI option with a mapping (staging → URLs, prod → URLs) would make environment switching ergonomic.

**Flakiness visibility**
Track pass rates over time with Allure history trends. Flag tests that fail intermittently across runs. At scale, a 1% flake rate across 1000 tests means 10 false failures per run — unacceptable.
