import os
import pytest


@pytest.mark.ui
def test_example_ui_homepage(page) -> None:
    base_url = os.getenv("UI_BASE_URL", "https://playwright.dev")
    page.goto(base_url)
    assert page.title()
    # Click on Get Started link
    page.get_by_role("link", name="Get started").click()
    assert "intro" in page.url.lower()
