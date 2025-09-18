import os
import sys
from playwright.sync_api import sync_playwright

# Add modules to path for logger
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'modules'))
from logger import get_logger  # type: ignore


def manual_login_and_save_auth():
    """
    Manual SSO login utility to save authentication state.
    This script opens a browser, navigates to the login page, and pauses
    for manual SSO completion, then saves the auth state to auth.json.
    """
    logger = get_logger(__name__)
    
    # Use environment variable for URL consistency with other tests
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    storage_path = os.getenv("AUTH_STORAGE_PATH", "auth.json")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            logger.info(f"Navigating to: {url}")
            page.goto(url)

            # Wait for and click SSO button
            sso_button = page.get_by_role("button", name="Sign in with SSO")
            sso_button.wait_for(state="visible", timeout=10000)
            sso_button.click(force=True)
            logger.info("Clicked SSO button")

            # Wait for SSO redirect and complete the flow
            logger.info("⏸️ Please complete SSO login manually in the browser...")
            logger.info("   Complete the full SSO flow until you reach the ACME application.")
            logger.info("   The browser will pause here for you to finish authentication.")
            page.pause()

            # Wait for the page to fully load after SSO completion
            page.wait_for_timeout(3000)
            
            # Check if we're on the correct page after SSO
            current_url = page.url
            logger.info(f"Current URL after SSO: {current_url}")
            
            # If we're still on a login page or have auth codes, wait for redirect
            if "login" in current_url.lower() or "code=" in current_url or "state=" in current_url:
                logger.info("Waiting for SSO redirect to complete...")
                page.wait_for_timeout(5000)
                current_url = page.url
                logger.info(f"URL after waiting: {current_url}")
            
            # Verify we're on the ACME application
            if "acme" not in current_url.lower():
                logger.warning(f"Not on ACME application. Current URL: {current_url}")
                logger.info("Please ensure you complete the full SSO flow to reach the ACME application.")

            # Save authentication state
            context.storage_state(path=storage_path)
            logger.info(f"✅ Authentication state saved to: {storage_path}")

            browser.close()
            
    except Exception as e:
        logger.error(f"Failed to save auth state: {e}")
        sys.exit(1)


if __name__ == "__main__":
    manual_login_and_save_auth()


