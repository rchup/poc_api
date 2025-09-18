import os
import re
import pytest
from playwright.sync_api import expect
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
from logger import get_logger


@pytest.mark.ui
def test_acme_login_page_loads_and_shows_sso_options(page) -> None:
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)

    expect(page).to_have_title(re.compile("Login with SSO|Unanet", re.IGNORECASE))

    expect(page.get_by_role("button", name="Sign in with Google")).to_be_visible()
    expect(page.get_by_role("button", name="Sign in with Microsoft")).to_be_visible()
    expect(page.get_by_role("button", name="Sign in with SSO")).to_be_visible()


@pytest.mark.ui
def test_acme_login_click_sso_button(page) -> None:
    logger = get_logger(__name__)
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    
    # Wait for page to load
    expect(page).to_have_title(re.compile("Login with SSO|Unanet", re.IGNORECASE))
    
    # Click the SSO button
    sso_button = page.get_by_role("button", name="Sign in with SSO")
    expect(sso_button).to_be_visible()
    sso_button.click()
    logger.info("Clicked SSO button")
    
    # Wait for navigation or modal to appear
    page.wait_for_timeout(2000)
    
    # Log what happened
    logger.info(f"URL after SSO click: {page.url}")
    logger.info(f"Page title after SSO click: {page.title()}")
    
    # Check if we're still on the same page or navigated somewhere
    assert "qa.govpro.ai" in page.url or "unanet" in page.url.lower()


@pytest.mark.ui
def test_acme_login_with_credentials(page) -> None:
    logger = get_logger(__name__)
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    
    # Wait for page to load
    expect(page).to_have_title(re.compile("Login with SSO|Unanet", re.IGNORECASE))
    
    # Look for email/username field (try different selectors)
    email_field = None
    try:
        email_field = page.get_by_placeholder("Email").first
        if not email_field.is_visible():
            email_field = page.get_by_placeholder("Username").first
    except:
        try:
            email_field = page.locator("input[type='email']").first
        except:
            email_field = page.locator("input[name='email']").first
    
    # Assert email field is found and visible
    assert email_field is not None, "Email field not found on page"
    assert email_field.is_visible(), "Email field is not visible"
    
    email_field.fill("roman.chuplak-c@unanet.com")
    logger.info("Filled email field")
    
    # Look for password field
    password_field = None
    try:
        password_field = page.get_by_placeholder("Password").first
    except:
        try:
            password_field = page.locator("input[type='password']").first
        except:
            password_field = page.locator("input[name='password']").first
    
    # Assert password field is found and visible
    assert password_field is not None, "Password field not found on page"
    assert password_field.is_visible(), "Password field is not visible"
    
    password_field.fill("!@12345678QWerty")
    logger.info("Filled password field")
    
    # Look for login button
    login_button = None
    try:
        login_button = page.get_by_role("button", name="Login").first
    except:
        try:
            login_button = page.get_by_role("button", name="Sign In").first
        except:
            try:
                login_button = page.locator("button[type='submit']").first
            except:
                login_button = page.locator("input[type='submit']").first
    
    # Assert login button is found and visible
    assert login_button is not None, "Login button not found on page"
    assert login_button.is_visible(), "Login button is not visible"
    
    login_button.click()
    logger.info("Clicked login button")
    
    # Wait for navigation or error message
    page.wait_for_timeout(3000)
    
    logger.info(f"URL after login attempt: {page.url}")
    logger.info(f"Page title after login: {page.title()}")
    
    # Assert login was successful - check for redirect away from login page
    assert page.url != url, f"Still on login page after login attempt. Current URL: {page.url}"
    
    # Assert we're not on an error page
    assert "error" not in page.url.lower(), f"Login failed - redirected to error page: {page.url}"
    assert "invalid" not in page.url.lower(), f"Login failed - invalid credentials page: {page.url}"
    
    # Assert we're on a success page (dashboard, home, or main app)
    success_indicators = ["dashboard", "home", "main", "app", "unanet"]
    url_lower = page.url.lower()
    title_lower = page.title().lower()
    
    success_found = any(indicator in url_lower or indicator in title_lower for indicator in success_indicators)
    assert success_found, f"Login status unclear - not redirected to expected success page. URL: {page.url}, Title: {page.title()}"
    
    logger.info("Login appears successful - redirected to expected page")


