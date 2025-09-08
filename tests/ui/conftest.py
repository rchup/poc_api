import os
import pathlib
import pytest
from datetime import datetime
from playwright.sync_api import Browser


@pytest.fixture(scope="session")
def ui_artifacts_dir() -> str:
    base = os.getenv("UI_REPORTS_DIR", os.path.join("reports", "ui"))
    path = pathlib.Path(base).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Make test outcome info available on item for fixtures
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def page(browser: Browser, request: pytest.FixtureRequest, ui_artifacts_dir: str):
    # Create a new context per test with video recording
    context = browser.new_context(record_video_dir=ui_artifacts_dir)
    # Enable tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    # Teardown: save artifacts
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    trace_path = os.path.join(ui_artifacts_dir, f"{test_name}-{timestamp}-trace.zip")
    context.tracing.stop(path=trace_path)

    # If test failed, save a screenshot
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        screenshot_path = os.path.join(ui_artifacts_dir, f"{test_name}-{timestamp}.png")
        try:
            page.screenshot(path=screenshot_path, full_page=True)
        except Exception:
            pass

    context.close()
