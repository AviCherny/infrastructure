# Architecture

## What this framework does

Runs automated tests against two targets:
- **API:** [AirportGap](https://airportgap.com/api) — a REST API for airport data and distance calculations
- **UI:** [BlazeDemo](https://blazedemo.com) — a flight booking web app

The goal isn't the targets — they're throwaway. The goal is the framework structure: how tests are organized, how requests are built, how failures are reported. That structure is what transfers to any real project.

---

## Layers

```
Test file
   └── Client function       (airports_client, distances_client)
         └── URL builder     (single source of truth for all URLs)
         └── Body builder    (constructs request payloads via chaining)
         └── requests.Session (shared headers, response hooks)
```

**Test file** — expresses intent only. No URLs, no raw dicts, no HTTP verbs. A test should read like a spec.

**Client** — one function per API action. Owns the HTTP method and delegates URL and body construction. Thin by design: no business logic, no assertions.

**URL builder** — all URLs live here. If the base URL or path changes, one file changes, not every test file.

**Body builder** — chainable builder that constructs request payloads. Prevents key name typos and makes test intent explicit. Nested builders are supported for complex payloads.

**Session** — created once per test session via a pytest fixture. Shared headers (e.g. `Content-Type`) are set once. A response hook automatically logs every HTTP call and attaches it to the Allure report — without any test needing to call a logger.

---

## Key decisions

**Why a session fixture scoped to the test session, not per test?**
Creating an HTTP session per test adds overhead and means headers must be configured repeatedly. The session fixture is created once, shared across all API tests, and torn down automatically by pytest.

**Why static `@pytest.mark.parametrize` for airport IDs?**
Testing against a fixed set of well-known airports (KIX, SYD, JFK, LHR) gives deterministic, readable tests. Dynamic discovery at collection time adds complexity and makes failures harder to diagnose — if the API changes its airport list, test behavior changes silently. Static IDs make the contract explicit: these specific airports must always be reachable and return valid data.

**Why BodyBuilder instead of plain dicts?**
`{"form": "TLV"}` is a silent bug — wrong key, no error until runtime. `BodyBuilder().set("from", "TLV")` is the same dict, but the builder is the documented interface. Future validation or serialization logic has one place to live.

**Why Page Object Model for UI?**
Tests that contain Playwright selectors break every time the UI changes. Page Objects absorb the change — the selector is updated in one place, and all tests that use that page continue to work.

**Why retain video and trace only on failure?**
Video and trace are always recorded during the test. On success they are discarded — video is deleted, trace is stopped without saving. On failure they are attached to the Allure report, so every failed test in CI has everything needed to reproduce the issue: a video replay, a Playwright trace, a screenshot, and console errors.

---

## Test isolation

- **API tests** share one session (fast, stateless calls)
- **UI tests** get a fresh browser context per test (isolated state, separate video recording)
- The browser itself is session-scoped (launching Chromium is slow; reusing it is not a risk since contexts are isolated)
