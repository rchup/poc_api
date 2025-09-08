# API Test Automation Framework (POC)

A minimal, extensible Python test automation framework for API and UI testing using pytest, requests, and Playwright.

## Quickstart

1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run API tests
```bash
pytest -q tests -k "not ui"
```

4. Install Playwright browsers (once)
```bash
python -m playwright install --with-deps
```

5. Run UI tests
```bash
pytest -q -m ui
```

## Structure
```
api_requests_poc/
  src/
    taf/
      __init__.py
      logger.py
      api/
        client.py
        config.py
        base_api.py
  tests/
    conftest.py
    test_health.py
    ui/
      test_example_ui.py
  .github/workflows/ci.yml
  .gitlab-ci.yml
  pyproject.toml
  requirements.txt
  README.md
```

## Features
- API: Session-based client with retries, backoff, timeouts, logging, and JSON helpers
- UI: pytest + Playwright fixtures (page/context) for browser automation

## Environment variables
- API: `API_BASE_URL`, `API_TIMEOUT`, `API_MAX_RETRIES`, `API_BACKOFF_FACTOR`, `API_VERIFY_SSL`, `API_TOKEN`, `API_DEFAULT_HEADERS`, `API_LOG_LEVEL`
- UI: `UI_BASE_URL` (default: `https://playwright.dev`)

## CI
- GitHub Actions: `.github/workflows/ci.yml`
- GitLab CI: `.gitlab-ci.yml`
  - Adjust to install Playwright browsers for UI jobs
