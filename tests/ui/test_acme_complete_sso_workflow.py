import os
import re
import pytest
from playwright.sync_api import expect
import sys
import logging

# Add modules to path for logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
from logger import get_logger  # type: ignore


@pytest.mark.ui
def test_acme_complete_sso_login_workflow(page) -> None:
    """
    Validates authenticated access using Playwright storage state (auth.json).
    Requires a previously saved storage state. If missing, the test is skipped
    with instructions to generate it.
    """
    logger = get_logger(__name__)

    # Ensure storage state exists; page fixture will load it automatically
    storage_path = os.getenv("AUTH_STORAGE_PATH", "auth.json")
    if not os.path.exists(storage_path):
        pytest.skip(
            f"Storage state '{storage_path}' not found. Generate it via: python tests/ui/save_auth_state.py"
        )

    # Navigate to ACME tenant home; should resolve to authenticated app
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    page.wait_for_timeout(2000)

    # Expect to be in the main app without SSO prompts
    expect(page).not_to_have_url(re.compile("okta|login", re.IGNORECASE))
    expect(page).to_have_url(re.compile("qa\\.govpro\\.ai", re.IGNORECASE))
    logger.info(f"Arrived at application: {page.url}")

    # Verify user identity visible
    user_email = os.getenv("TEST_EMAIL", "roman.chuplak-c@unanet.com")
    email_found = False
    try:
        if page.locator(f"text={user_email}").is_visible():
            email_found = True
            logger.info(f"Found user email in interface: {user_email}")
    except Exception:
        pass

    if not email_found:
        try:
            profile_name = os.getenv("TEST_PROFILE_NAME", "Roman Chuplak-C")
            user_profile = page.locator(f"text={profile_name}").first
            if user_profile.is_visible():
                parent = user_profile.locator("..")
                if user_email in (parent.text_content() or ""):
                    email_found = True
                    logger.info(f"Found user email near profile: {user_email}")
        except Exception:
            pass

    assert email_found, (
        f"User email '{user_email}' not visible. Ensure auth state is valid or regenerate auth.json"
    )

    # Sanity: presence of key app UI elements
    main_elements = ["Talk to Champ", "Capture", "Pursue", "Quote", "Write"]
    found_elements = []
    for text_value in main_elements:
        try:
            if page.locator(f"text={text_value}").is_visible():
                found_elements.append(text_value)
        except Exception:
            pass
    assert found_elements, f"Main app elements not found. Expected any of: {main_elements}"
    logger.info(f"Visible app elements: {found_elements}")


@pytest.mark.ui
def test_acme_sso_login_verification_only(page) -> None:
    """
    Quick verification test to check if user is already logged in
    by looking for user email in the interface
    """
    logger = get_logger(__name__)
    
    # Require storage state
    storage_path = os.getenv("AUTH_STORAGE_PATH", "auth.json")
    if not os.path.exists(storage_path):
        pytest.skip(
            f"Storage state '{storage_path}' not found. Generate it via: python tests/ui/save_auth_state.py"
        )

    # Navigate to ACME application
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    
    # Wait for page to load
    page.wait_for_timeout(3000)
    
    # Check if we're already logged in (redirected to main app)
    if "chat" in page.url or "app" in page.title().lower():
        logger.info("Already logged in - redirected to main application")
        
        # Verify user email is displayed
        user_email = os.getenv("TEST_EMAIL", "roman.chuplak-c@unanet.com")
        email_display = page.locator(f"text={user_email}")
        
        if email_display.is_visible():
            logger.info(f"✅ Login verification successful - email found: {user_email}")
            assert True, "User is logged in successfully"
        else:
            pytest.fail(f"User email '{user_email}' not found - not logged in")
    else:
        pytest.skip("Not logged in with storage state - regenerate auth.json")


@pytest.mark.ui
def test_acme_current_login_state(page) -> None:
    """
    Test to verify current login state by checking for user email
    in the bottom left corner of the interface
    """
    logger = get_logger(__name__)
    
    # Require storage state
    storage_path = os.getenv("AUTH_STORAGE_PATH", "auth.json")
    if not os.path.exists(storage_path):
        pytest.skip(
            f"Storage state '{storage_path}' not found. Generate it via: python tests/ui/save_auth_state.py"
        )

    # Navigate to ACME application
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    
    # Wait for page to load
    page.wait_for_timeout(3000)
    
    logger.info(f"Current URL: {page.url}")
    logger.info(f"Current title: {page.title()}")
    
    # Check for user email in various locations
    user_email = os.getenv("TEST_EMAIL", "roman.chuplak-c@unanet.com")
    email_found = False
    
    # Try to find email in the page content
    try:
        if page.locator(f"text={user_email}").is_visible():
            email_found = True
            logger.info(f"✅ Found user email in page: {user_email}")
    except:
        pass
    
    # Try to find email in user profile section
    if not email_found:
        try:
            if page.locator("text=Roman Chuplak-C").is_visible():
                # Look for email near the name
                user_section = page.locator("text=Roman Chuplak-C").first
                parent_text = user_section.locator("..").text_content()
                if user_email in parent_text:
                    email_found = True
                    logger.info(f"✅ Found user email in profile section: {user_email}")
        except:
            pass
    
    # Assert email is found (indicating successful login)
    assert email_found, f"User email '{user_email}' not found - login verification failed"
    logger.info("✅ Login state verification passed - user is logged in")
