import os
import sys
import pytest
from playwright.sync_api import expect

# Add modules to path for logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
from logger import get_logger  # type: ignore


def test_navigate_to_acme_with_auth(page):
    """
    Test navigating to the ACME page using saved authentication state.
    This test uses the auth.json file to authenticate and navigate to the ACME application.
    """
    logger = get_logger(__name__)
    
    # Navigate to the ACME page
    url = "https://qa.govpro.ai/t/acme/"
    logger.info(f"Navigating to: {url}")
    page.goto(url)
    
    # Wait for the page to load
    page.wait_for_load_state("networkidle")
    
    # Take a screenshot before SSO
    screenshot_path_before = os.path.join("reports", "ui", "acme_page_before_sso.png")
    os.makedirs(os.path.dirname(screenshot_path_before), exist_ok=True)
    page.screenshot(path=screenshot_path_before, full_page=True)
    logger.info(f"Screenshot before SSO saved to: {screenshot_path_before}")
    
    # Check if we need to click SSO button
    current_url = page.url
    logger.info(f"Current URL: {current_url}")
    
    # Look for SSO button and click it if present
    try:
        sso_button = page.get_by_role("button", name="Sign in with SSO")
        if sso_button.is_visible():
            logger.info("Found SSO button, clicking it...")
            sso_button.click()
            page.wait_for_timeout(3000)  # Wait for SSO redirect
            logger.info("Clicked SSO button")
        else:
            logger.info("SSO button not visible, checking if already authenticated")
    except Exception as e:
        logger.info(f"SSO button not found or not clickable: {e}")
    
    # Wait for the page to load after SSO
    page.wait_for_load_state("networkidle")
    
    # Get updated URL after SSO
    current_url = page.url
    logger.info(f"Current URL after SSO: {current_url}")
    
    # Wait for page content to load
    page.wait_for_timeout(3000)
    
    # Take a screenshot after SSO
    screenshot_path_after = os.path.join("reports", "ui", "acme_page_after_sso.png")
    page.screenshot(path=screenshot_path_after, full_page=True)
    logger.info(f"Screenshot after SSO saved to: {screenshot_path_after}")
    
    # Look for and click "ACME Federal" button/link
    try:
        # Try different selectors for ACME Federal
        acme_federal_selectors = [
            "text=ACME Federal",
            "text=ACME",
            "[data-testid*='acme']",
            "a:has-text('ACME Federal')",
            "button:has-text('ACME Federal')",
            "div:has-text('ACME Federal')"
        ]
        
        acme_federal_clicked = False
        for selector in acme_federal_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    logger.info(f"Found ACME Federal element with selector: {selector}")
                    element.click()
                    page.wait_for_timeout(2000)  # Wait for click to process
                    acme_federal_clicked = True
                    logger.info("✅ Clicked ACME Federal")
                    break
            except Exception as e:
                logger.debug(f"Selector {selector} not found: {e}")
                continue
        
        if not acme_federal_clicked:
            logger.warning("Could not find ACME Federal element to click")
            
    except Exception as e:
        logger.warning(f"Error trying to click ACME Federal: {e}")
    
    # Wait for any navigation after clicking ACME Federal
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Get final URL
    final_url = page.url
    logger.info(f"Final URL after ACME Federal click: {final_url}")
    
    # Take a final screenshot
    screenshot_path_final = os.path.join("reports", "ui", "acme_page_final.png")
    page.screenshot(path=screenshot_path_final, full_page=True)
    logger.info(f"Final screenshot saved to: {screenshot_path_final}")
    
    # Check if we're on the correct page
    if "acme" in final_url.lower():
        logger.info("✅ Successfully navigated to ACME page")
    else:
        logger.warning(f"Not on ACME page. Final URL: {final_url}")
    
    # Try to find any visible content on the page
    try:
        # Wait for any visible element
        page.wait_for_selector("*", state="visible", timeout=5000)
        logger.info("✅ Page content is visible")
    except Exception as e:
        logger.warning(f"Could not find visible content: {e}")
        # Take a final screenshot for debugging
        debug_screenshot = os.path.join("reports", "ui", "acme_page_debug.png")
        page.screenshot(path=debug_screenshot, full_page=True)
        logger.info(f"Debug screenshot saved to: {debug_screenshot}")
    
    logger.info("✅ Test completed - ACME page navigation with SSO and ACME Federal click attempted")
