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
      api_client.py
      config.py
  tests/
    conftest.py
    test_health.py
  pyproject.toml
  requirements.txt
  README.md
```

## Notes
- Uses pytest for test running and fixtures.
- Uses requests with retry and timeout support.
- Ready to extend with reporting, environments, and CI.
# poc_api
