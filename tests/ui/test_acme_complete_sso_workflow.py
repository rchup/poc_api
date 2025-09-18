import os
import re
import pytest
from playwright.sync_api import expect
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
from logger import get_logger


@pytest.mark.ui
def test_acme_complete_sso_login_workflow(page) -> None:
    """
    Complete SSO login workflow for ACME Federal tenant:
    1. Navigate to ACME login page
    2. Click "Sign in with SSO" button
    3. Enter email address
    4. Enter password
    5. Select MFA method (Okta Verify push)
    6. Wait for MFA approval
    7. Select ACME Federal organization
    8. Verify successful login with email display
    """
    logger = get_logger(__name__)
    
    # Step 1: Navigate to ACME login page
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)
    logger.info(f"Navigated to ACME login page: {url}")
    
    # Verify page loaded correctly
    expect(page).to_have_title(re.compile("Login with SSO|Unanet", re.IGNORECASE))
    logger.info("ACME login page loaded successfully")
    
    # Step 2: Click "Sign in with SSO" button
    sso_button = page.get_by_role("button", name="Sign in with SSO")
    expect(sso_button).to_be_visible()
    sso_button.click()
    logger.info("Clicked 'Sign in with SSO' button")
    
    # Wait for redirect to Okta
    page.wait_for_timeout(2000)
    expect(page).to_have_url(re.compile(".*okta\.com.*"))
    logger.info(f"Redirected to Okta: {page.url}")
    
    # Step 3: Enter email address
    email = os.getenv("TEST_EMAIL", "roman.chuplak-c@unanet.com")
    username_field = page.get_by_role("textbox", name="Username")
    expect(username_field).to_be_visible()
    username_field.fill(email)
    logger.info(f"Entered email: {email}")
    
    # Click Next button
    next_button = page.get_by_role("button", name="Next")
    expect(next_button).to_be_visible()
    next_button.click()
    logger.info("Clicked Next button")
    
    # Step 4: Enter password
    password = os.getenv("TEST_PASSWORD", "pobta3-jettem-fUbbuf")
    password_field = page.get_by_role("textbox", name="Password")
    expect(password_field).to_be_visible()
    password_field.fill(password)
    logger.info("Entered password")
    
    # Click Verify button
    verify_button = page.get_by_role("button", name="Verify")
    expect(verify_button).to_be_visible()
    verify_button.click()
    logger.info("Clicked Verify button")
    
    # Step 5: Select MFA method (Okta Verify push)
    page.wait_for_timeout(2000)
    expect(page).to_have_title(re.compile("Sign In|Unanet", re.IGNORECASE))
    
    # Look for MFA options
    mfa_push_option = page.get_by_role("link", name=re.compile("Select to get a push notification", re.IGNORECASE))
    if mfa_push_option.is_visible():
        mfa_push_option.click()
        logger.info("Selected Okta Verify push notification for MFA")
        
        # Wait for push notification to be sent
        page.wait_for_timeout(3000)
        expect(page.locator("text=Push notification sent")).to_be_visible()
        logger.info("Push notification sent - waiting for approval")
        
        # Wait for MFA approval (this would normally require user interaction)
        # In a real test, you might need to mock this or use a test account
        page.wait_for_timeout(5000)  # Wait for potential auto-approval or timeout
    else:
        logger.warning("MFA push option not found, continuing with other MFA methods")
    
    # Step 6: Wait for redirect to welcome page
    page.wait_for_timeout(3000)
    
    # Check if we're on the welcome page
    if "passport" in page.url or "welcome" in page.title().lower():
        logger.info("Reached welcome page after MFA")
        
        # Step 7: Select ACME Federal organization
        acme_federal_option = page.locator("div").filter(has_text=re.compile("Acme.*FEDERAL", re.IGNORECASE))
        if acme_federal_option.is_visible():
            acme_federal_option.click()
            logger.info("Selected ACME Federal organization")
        else:
            # Try alternative selector
            acme_button = page.get_by_role("button", name=re.compile("Acme.*FEDERAL", re.IGNORECASE))
            if acme_button.is_visible():
                acme_button.click()
                logger.info("Selected ACME Federal organization (alternative selector)")
            else:
                pytest.fail("ACME Federal organization option not found")
    else:
        logger.warning("Welcome page not reached, continuing to check for login success")
    
    # Step 8: Verify successful login
    page.wait_for_timeout(3000)
    
    # Check if we're in the main application
    expect(page).to_have_url(re.compile(".*qa\.govpro\.ai.*"))
    logger.info(f"Reached main application: {page.url}")
    
    # Verify user email is displayed (login confirmation)
    user_email = os.getenv("TEST_EMAIL", "roman.chuplak-c@unanet.com")
    email_display = page.locator(f"text={user_email}")
    
    # Try multiple ways to find the email display
    email_found = False
    try:
        if email_display.is_visible():
            email_found = True
            logger.info(f"Found user email in interface: {user_email}")
    except:
        pass
    
    # Alternative: look for email in user profile section
    if not email_found:
        try:
            user_profile = page.locator("text=Roman Chuplak-C").first
            if user_profile.is_visible():
                # Check if email is near the name
                parent = user_profile.locator("..")
                if user_email in parent.text_content():
                    email_found = True
                    logger.info(f"Found user email in profile section: {user_email}")
        except:
            pass
    
    # Assert login was successful
    assert email_found, f"User email '{user_email}' not found in interface - login may have failed"
    
    # Additional verification: check for main application elements
    main_elements = [
        "Talk to Champ",
        "Capture",
        "Pursue", 
        "Quote",
        "Write"
    ]
    
    found_elements = []
    for element_text in main_elements:
        try:
            if page.locator(f"text={element_text}").is_visible():
                found_elements.append(element_text)
        except:
            pass
    
    assert len(found_elements) > 0, f"Main application elements not found. Expected: {main_elements}"
    logger.info(f"Found main application elements: {found_elements}")
    
    logger.info("✅ Complete SSO login workflow test passed - user successfully logged in to ACME Federal")


@pytest.mark.ui
def test_acme_sso_login_verification_only(page) -> None:
    """
    Quick verification test to check if user is already logged in
    by looking for user email in the interface
    """
    logger = get_logger(__name__)
    
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
        pytest.skip("Not logged in - would need to run full login workflow")


@pytest.mark.ui
def test_acme_current_login_state(page) -> None:
    """
    Test to verify current login state by checking for user email
    in the bottom left corner of the interface
    """
    logger = get_logger(__name__)
    
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
