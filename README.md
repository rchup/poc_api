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

## Environment Variables

The project uses environment variables for configuration. Copy the template and customize as needed:

```bash
cp env.template .env
```

### API Testing Variables
- `API_BASE_URL` - Base URL for API testing (default: `https://httpbin.org`)
- `API_TOKEN` - API authentication token
- `API_TIMEOUT` - Request timeout in seconds (default: `10`)
- `API_MAX_RETRIES` - Maximum retry attempts (default: `2`)
- `API_BACKOFF_FACTOR` - Backoff factor for retries (default: `0.2`)
- `API_VERIFY_SSL` - Enable SSL verification (default: `true`)
- `API_DEFAULT_HEADERS` - Default headers as JSON string
- `API_LOG_LEVEL` - Logging level (default: `INFO`)

### UI Testing Variables
- `UI_ACME_URL` - ACME application URL (default: `https://qa.govpro.ai/t/acme/`)
- `AUTH_STORAGE_PATH` - Path to save authentication state (default: `auth.json`)
- `TEST_EMAIL` - Test user email (default: `roman.chuplak-c@unanet.com`)
- `TEST_PROFILE_NAME` - Test user profile name (default: `Roman Chuplak-C`)
- `HEADLESS` - Run browser in headless mode (default: `false`)

### Reporting Variables
- `REPORTS_DIR` - Base reports directory (default: `reports`)
- `UI_REPORTS_DIR` - UI-specific reports directory (default: `reports/ui`)

## CI
- GitHub Actions: `.github/workflows/ci.yml`
- GitLab CI: `.gitlab-ci.yml`
  - Adjust to install Playwright browsers for UI jobs
