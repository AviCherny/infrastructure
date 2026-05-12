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
- [ ] HTTP session fixture (conftest.py)

## API Tests
- [ ] GET /airports
- [ ] GET /airports/:id
- [ ] POST /distances

## UI Layer
- [ ] home_page.py (BlazeDemo)
- [ ] results_page.py
- [ ] purchase_page.py
- [ ] confirmation_page.py

## UI Fixtures
- [ ] Browser fixture (conftest.py)
- [ ] Page fixture

## UI Tests
- [ ] Search for flight
- [ ] Select flight
- [ ] Complete purchase flow

## Reporting
- [ ] pytest markers configured
- [ ] HTML report setup (pytest-html)
