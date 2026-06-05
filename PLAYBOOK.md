# PLAYBOOK.md — How to Build a New Automation Framework

One step at a time. Complete the gate before moving to the next step.
Each prompt is ready to paste to Claude — replace `[placeholders]` with your project details.

---

## Step 1: Skeleton

**What to build:**
- Folder structure
- `config.py` — base URLs, environment config
- `requirements.txt`
- `pytest.ini` — markers, default flags
- `.gitignore`

**Prompt:**
```
Build the project skeleton for a new automation framework.
Target: [describe your app — e.g. "a REST API at [base URL] and a UI at [UI URL]"]
Create: folder structure, config.py with base URLs, requirements.txt with pytest/requests/playwright/allure,
pytest.ini with markers for api/ui, and .gitignore.
No logic, no tests — structure only. Follow CLAUDE.md.
```

**Gate:**
- [x] Folders exist, nothing else
- [x] `config.py` has base URLs only — no logic
- [x] `pytest.ini` has markers defined
- [x] No test files, no client files, no builders yet

---

## Step 2: Architecture Decision

**What to build:**
- `ARCHITECTURE.md` — layer diagram, key decisions, fixture scoping

**Prompt:**
```
Write ARCHITECTURE.md for this project.
API target: [describe API]
UI target: [describe UI]
Document: layer diagram (test → client → builder), fixture scoping decisions (why session vs function),
and key design decisions (why builders, why POM, why static test data).
Base it on our CLAUDE.md architecture rules.
```

**Gate:**
- [x] Layer diagram is explicit and correct
- [x] Fixture scoping is documented with reasoning
- [x] Key decisions have "why" written down — not just "what"

---

## Step 3: Project Rules

**What to build:**
- `CLAUDE.md` for the new project (based on this one)
- `PLAYBOOK.md` (this file, copied over)

**Prompt:**
```
Create CLAUDE.md for this project.
Copy the structure from our infrastructure CLAUDE.md:
- Layer ownership diagram
- Naming conventions for this project's resources: [list your resources, e.g. flights, hotels]
- Fixture scoping rules
- "When you add a new endpoint" checklist
- Code quality rules
- Git workflow
```

**Gate:**
- [x] Naming conventions match the actual resources in this project
- [x] Layer diagram is updated for this project's clients/builders
- [x] Git workflow is present

---

## Step 4: Fixtures + Allure + Logging

**What to build:**
- `conftest.py` — API session fixture, browser fixture, context fixture
- Allure wired into session hook (logs every HTTP call automatically)
- Screenshot + video + trace on UI failure
- `allure-categories.json` — defines failure categories (product bugs, test bugs, etc.)

**Prompt:**
```
Build conftest.py for this project.
API: session-scoped HTTP session fixture with base URL from config.py.
     Add a response hook that logs every request/response and attaches it to Allure automatically.
UI:  session-scoped browser fixture (Playwright, Chromium).
     function-scoped context fixture — fresh per test, with video and trace recording.
     On failure: attach screenshot, video, and trace to Allure. On success: discard them.
Also create allure-categories.json with failure categories: product bugs, test bugs, and known issues.
Follow CLAUDE.md fixture scoping rules.
```

**Gate:**
- [x] API session is session-scoped — not created per test
- [x] UI context is function-scoped — fresh per test
- [x] Every HTTP call is logged and attached to Allure without any test needing to call a logger
- [x] Failure artifacts (screenshot, video, trace) attach automatically — no test calls this manually
- [x] `allure-categories.json` exists in project root (auto-detected by Allure — no pytest.ini reference needed)

---

## Step 5: Builders

**What to build:**
- `url_builder.py` — all URLs for all resources
- `body_builder.py` — chainable builder for all request payloads

**Prompt:**
```
Build the URL and body builders for this project.
Resources: [list endpoints — e.g. GET /flights, POST /bookings/:id]
UrlBuilder: one method per endpoint, base URL from config.py. No URL string exists anywhere else.
BodyBuilder: chainable methods for each payload field. No plain dicts passed to client functions.
Follow CLAUDE.md architecture rules.
```

**Gate:**
- [x] Every URL in the project lives in `url_builder.py` — nowhere else
- [x] No plain dict is constructed outside of `body_builder.py`
- [x] Builder methods are chainable

---

## Step 6: Clients

**What to build:**
- One client file per resource (e.g. `flights_client.py`, `bookings_client.py`)

**Prompt:**
```
Build the API clients for this project.
Resources: [list resources]
Each client: one function per API action. Owns the HTTP method. Delegates URL to UrlBuilder, body to BodyBuilder.
No business logic. No assertions. Thin by design.
Follow CLAUDE.md architecture rules.
```

**Gate:**
- [x] Each client function is under ~5 lines
- [x] No URL string in any client file
- [x] No plain dict in any client function
- [x] No assertions or business logic in any client

---

## Step 7: Page Objects

**What to build:**
- One page object per page (e.g. `home_page.py`, `results_page.py`)

**Prompt:**
```
Build page objects for this project.
UI target: [describe the app and its pages]
Pages: [list pages and their actions — e.g. HomePage: search for flight, select origin/destination]
Each page object: encapsulates selectors and actions. No selectors in test files.
Follow CLAUDE.md architecture rules and Playwright best practices.
```

**Gate:**
- [x] No Playwright selector exists outside of a page object
- [x] Each page object method describes an action, not a technical step
- [x] Test files can read like plain English using these methods

---

## Step 8: Flows (optional)

**What to build:**
- `flows.py` — reusable multi-step UI sequences that combine page objects

**When to add this:**
Add a flows layer when a sequence of steps is reused across multiple tests. If every test has a unique flow — skip it.

**Prompt:**
```
Build a flows layer for this project.
Identify sequences that repeat across UI tests (e.g. "search and select a flight").
Create flows.py with one function per reusable sequence.
Each function takes page objects as arguments and calls their methods — no selectors, no Playwright calls directly.
Tests call flows, not page objects directly, for shared sequences.
```

**Gate:**
- [x] No duplicated page-object call sequences across test files
- [x] Flows call page object methods only — no raw selectors
- [x] Tests that share a flow use it — they don't repeat the steps inline

---

## Step 9: Tests

**What to build:**
- API test files (one per resource)
- UI test files (one per flow)

**Prompt:**
```
Write tests for this project.
API tests: [describe what to test — e.g. GET /flights returns list, POST /bookings creates a booking]
UI tests: [describe flows — e.g. search for flight, select result, complete booking]
Tests must express intent only: no URLs, no HTTP verbs, no raw dicts, no selectors.
Use pytest markers: @pytest.mark.api / @pytest.mark.ui
Follow CLAUDE.md architecture rules.
```

**Gate:**
- [x] No URL, HTTP verb, raw dict, or selector in any test file
- [x] Each test reads like a spec — what it does is clear without reading the implementation
- [x] All tests pass locally before pushing
- [x] Allure report shows correct steps and attachments on failure

---

## Step 10: CI/CD

**What to build:**
- `.github/workflows/tests.yml` — runs tests on push/PR, publishes Allure report

**Prompt:**
```
Build a GitHub Actions workflow for this project.
On every push and pull request:
  1. Install Python dependencies from requirements.txt
  2. Install Playwright browsers
  3. Run pytest with allure results output
  4. Publish Allure report to GitHub Pages
Separate API and UI jobs if they have different dependencies or run times.
```

**Gate:**
- [x] Workflow triggers on push and PR
- [x] Allure report is published and accessible after each run
- [x] Tests pass in CI — not just locally

---

## Final Gate — Before Pushing Anything

- [x] Ran full test suite locally — all green
- [x] Reviewed diff as a tech lead — out loud, visibly
- [x] README updated with setup instructions and how to run tests
- [x] Branch created from the start — never worked on main
