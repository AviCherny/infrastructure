# Build Checklist

## Foundation
- [x] Folder structure
- [x] config.py (base URLs)
- [x] requirements.txt
- [x] pytest.ini
- [x] .gitignore

## API Layer
- [x] url_builder.py
- [x] body_builder.py
- [x] airports_client.py
- [x] distances_client.py

## API Fixtures
- [x] HTTP session fixture (conftest.py)

## API Tests
- [x] GET /airports
- [x] GET /airports/:id
- [x] POST /distances

## UI Layer
- [x] home_page.py (BlazeDemo)
- [x] results_page.py
- [x] purchase_page.py
- [x] confirmation_page.py

## UI Fixtures
- [x] Browser fixture (conftest.py)
- [x] Page fixture

## UI Tests
- [x] Search for flight
- [x] Select flight
- [x] Complete purchase flow

## Reporting
- [x] pytest markers configured
- [x] Allure Report setup
- [x] Screenshots on UI test failure

## Documentation
- [ ] README.md (setup, how to run tests, how to view Allure report)

## CI/CD
- [x] GitHub Actions workflow (runs tests + publishes Allure report)

## Environment Support
- [ ] Discuss: how to scale env config beyond current `os.getenv()` pattern
  - Current: `UI_BASE_URL` / `API_BASE_URL` env vars with hardcoded defaults (covers single-env use)
  - Next step: `--env=staging` CLI flag + `environments/` folder with per-env config files
  - Or: `.env.staging` / `.env.prod` files loaded via `python-dotenv`
  - Interview angle: tradeoffs between env vars, config files, and pytest fixtures for environment switching
