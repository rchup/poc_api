# UI Test Cases for ACME Federal SSO Login

This directory contains Playwright UI tests for the ACME Federal tenant SSO login workflow.

## Test Files

### `test_acme_login.py`
Basic UI tests for ACME login page:
- `test_acme_login_page_loads_and_shows_sso_options` - Verifies login page loads with SSO buttons
- `test_acme_login_click_sso_button` - Clicks SSO button and verifies redirect to Okta
- `test_acme_login_with_credentials` - Attempts credential-based login (expects to fail on SSO-only page)

### `test_acme_complete_sso_workflow.py`
Comprehensive SSO workflow tests:
- `test_acme_complete_sso_login_workflow` - Complete end-to-end SSO login process
- `test_acme_sso_login_verification_only` - Quick verification of existing login state
- `test_acme_current_login_state` - Checks for user email display to confirm login

## Environment Variables

Set these environment variables for testing:

```bash
export UI_ACME_URL="https://qa.govpro.ai/t/acme/"
export TEST_EMAIL="roman.chuplak-c@unanet.com"
export TEST_PASSWORD="pobta3-jettem-fUbbuf"
```

## Complete SSO Workflow

The complete SSO login workflow includes:

1. **Navigate to ACME login page** (`https://qa.govpro.ai/t/acme/`)
2. **Click "Sign in with SSO" button** → Redirects to Okta OAuth2
3. **Enter email address** (`roman.chuplak-c@unanet.com`)
4. **Enter password** (`pobta3-jettem-fUbbuf`)
5. **Select MFA method** (Okta Verify push notification)
6. **Wait for MFA approval** (requires user interaction)
7. **Select ACME Federal organization** from welcome page
8. **Verify successful login** by checking for user email in bottom left corner

## Running Tests

```bash
# Run all UI tests
pytest tests/ui/ -m ui -v

# Run specific test file
pytest tests/ui/test_acme_login.py -v

# Run with headed browser (visible)
pytest tests/ui/test_acme_login.py -v --headed

# Run with specific test
pytest tests/ui/test_acme_complete_sso_workflow.py::test_acme_complete_sso_login_workflow -v --headed
```

## Test Features

- **Proper logging** using the project's logger module
- **Environment variable support** for credentials and URLs
- **Multiple selector strategies** for robust element finding
- **Comprehensive assertions** to verify each step
- **Error handling** for different page states
- **Screenshot capture** for debugging failed tests

## Notes

- The complete SSO workflow requires manual MFA approval
- Tests use proper assertions to fail when login doesn't work
- All print statements have been replaced with structured logging
- Tests are designed to work with the existing pytest-playwright setup




