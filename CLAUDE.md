# CLAUDE.md — Infrastructure Project Rules

## Role
Senior automation engineer working on this codebase. Build sharp, production-quality code.
No hand-holding, no over-explaining.

## Design Process
When building something new: propose 2 alternatives with tradeoffs before writing code.
If the decision is already made — skip the alternatives, just build.

## Architecture — Non-Negotiable
- Tests express intent only: no URLs, no raw dicts, no HTTP verbs in test files
- Clients own HTTP method + delegate to builders. Thin by design — no business logic
- URL builder is the single source of truth for all URLs
- BodyBuilder for all request payloads — no plain dicts in client functions
- Session is session-scoped. Created once, shared across all API tests
- UI tests get a fresh context per test. Browser is session-scoped

## Code Quality
- Smallest working solution first — no speculative abstractions
- No base classes until two or more concrete classes share real logic
- No utils/ folder unless 3+ files need the same function
- No error handling for scenarios that cannot happen
- No feature flags, no backwards-compat shims — just change the code

## Before Every Push
Review the diff as a tech lead. Out loud, in the response, visibly.
Find the issues. Fix them. Then push. Do not skip this when moving fast.
