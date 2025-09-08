import os
import re
import pytest
from playwright.sync_api import expect


@pytest.mark.ui
def test_acme_login_page_loads_and_shows_sso_options(page) -> None:
    url = os.getenv("UI_ACME_URL", "https://qa.govpro.ai/t/acme/")
    page.goto(url)

    expect(page).to_have_title(re.compile("Login with SSO|Unanet", re.IGNORECASE))

    expect(page.get_by_role("button", name="Sign in with Google")).to_be_visible()
    expect(page.get_by_role("button", name="Sign in with Microsoft")).to_be_visible()
    expect(page.get_by_role("button", name="Sign in with SSO")).to_be_visible()


