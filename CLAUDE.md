# CLAUDE.md — Infrastructure Project Rules

## Design Process
When building something new: propose 2 alternatives with tradeoffs before writing code.
If the decision is already made — skip the alternatives, just build.

---

## Architecture — Non-Negotiable

### Layer ownership (test → client → builder)

```
test file
  └── calls client method  (e.g. airports_client.get_airport("TLV"))
        └── client owns HTTP verb + constructs request via builders
              ├── UrlBuilder  — single source of truth for all URLs
              └── BodyBuilder — single source of truth for all request payloads
```

Each layer owns exactly one thing. Nothing leaks across boundaries:
- **Test files**: express intent only. No URLs, no HTTP verbs, no raw dicts, no status codes.
- **Clients**: own the HTTP method. Thin by design — zero business logic. Delegate everything to builders.
- **UrlBuilder**: builds every URL. No URL string exists anywhere else.
- **BodyBuilder**: builds every request payload. No plain dict is passed to a client function.

### Naming conventions (no decisions needed when adding a resource)
- `<Resource>Client` — e.g. `AirportsClient`, `DistancesClient`
- `<Resource>UrlBuilder` — e.g. `AirportsUrlBuilder`
- `<Resource>BodyBuilder` — e.g. `AirportsBodyBuilder`
- Test file: `test_<resource>.py` — e.g. `test_airports.py`

### Fixture scoping
- **Session** — API session (auth, base URL). Created once, shared across all API tests.
- **Function** — UI browser context. Fresh per test, browser itself is session-scoped.
- Don't create a new session per test. Don't reuse UI context across tests. These are not preferences.

### When you add a new endpoint
1. Add the URL to the relevant `UrlBuilder`
2. Add the payload (if any) to the relevant `BodyBuilder`
3. Add the method to the relevant `Client`
4. Write the test — it should read like a sentence, nothing else

---

## Code Quality
- Smallest working solution first — no speculative abstractions
- No `utils/` folder unless 3+ files need the same function
- No error handling for scenarios that cannot happen
- No feature flags, no backwards-compat shims — just change the code

---

## Before Every Push
Review the diff as a tech lead. Out loud, in the response, visibly.
Find the issues. Fix them. Then push. Do not skip this when moving fast.

---

## Git Workflow — Non-Negotiable

Every task gets its own branch. No exceptions.

1. **Create the branch first** — before writing any code
2. Commit any pending work on current branch first
3. `git checkout -b feat/<short-description>` (or `fix/` / `experiment/`)
4. Build the thing
5. Commit when done
6. **Push the branch** — do not wait to be asked
7. **Merge to main** — after pushing:
   ```
   git checkout main
   git pull origin main
   git merge <branch-name>
   git push origin main
   git checkout <branch-name>
   ```
8. **Delete the branch** — after merging:
   ```
   git branch -d <branch-name>
   git push origin --delete <branch-name>
   ```

Branch naming: `feat/`, `fix/`, `experiment/` prefix. Kebab-case. 2–4 words max.
Never work directly on `main`.
