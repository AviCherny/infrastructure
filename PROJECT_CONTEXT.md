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

## Key Design Decisions

**URL builder owns all endpoints**
No client constructs a URL inline. If an endpoint changes, there's one place to change it.

**Session-scoped HTTP session, function-scoped browser context**
The HTTP session lives for the entire run — shared headers, one connection pool. Every UI test gets a clean browser context — no leftover state. Each layer gets what it needs.

**Response logging is in the session, not in tests**
`_log_response` hooks into the session. Every request auto-logs to Allure — tests don't touch it.

**Artifacts only on failure**
Screenshots, video, traces — only when a test fails. Passing tests clean up after themselves.

**Tests have no HTTP details**
No URLs, no methods, no raw dicts in test files. That lives in clients and builders. Tests say what, not how.
