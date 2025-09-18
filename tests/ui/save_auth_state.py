from playwright.sync_api import sync_playwright


def manual_login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://qa.govpro.ai/t/acme")

        sso_button = page.get_by_role("button", name="Sign in with SSO")
        sso_button.wait_for(state="visible")
        sso_button.click(force=True)

        print("\n⏸️ Please finish SSO login manually...")
        page.pause()

        context.storage_state(path="auth.json")
        print("✅ Auth state saved to auth.json")

        browser.close()


if __name__ == "__main__":
    manual_login_and_save_auth()


