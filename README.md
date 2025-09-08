# API Test Automation Framework (POC)

A minimal, extensible Python test automation framework for API testing using pytest and requests.

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

3. Run tests
```bash
pytest -q
```

## Structure
```
api_requests_poc/
  src/
    taf/
      __init__.py
      logger.py
      api/
        __init__.py (implicit)
        client.py
        config.py
        base_api.py
  tests/
    conftest.py
    test_health.py
  .github/workflows/ci.yml
  .gitlab-ci.yml
  pyproject.toml
  requirements.txt
  README.md
```

## Features
- Session-based client with retries, backoff, and timeouts
- Request/response logging with secret redaction
- Defaults headers support and optional Bearer token
- JSON convenience helpers (`get_json`, `post_json`)

## Environment variables
- `API_BASE_URL` (default: `https://httpbin.org`)
- `API_TIMEOUT` (default: `10`)
- `API_MAX_RETRIES` (default: `2`)
- `API_BACKOFF_FACTOR` (default: `0.2`)
- `API_VERIFY_SSL` (default: `true`)
- `API_TOKEN` (optional)
- `API_DEFAULT_HEADERS` (JSON object string, e.g. `{"X-Trace":"test"}`)
- `API_LOG_LEVEL` (e.g. `DEBUG`, `INFO`)

## CI
- GitHub Actions: `.github/workflows/ci.yml`
- GitLab CI: `.gitlab-ci.yml`
  - Produces JUnit report artifact `report.xml` for MR test summaries.
