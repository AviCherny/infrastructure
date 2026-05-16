import logging
import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright
from ui.pages.purchase_page import PassengerDetails


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=os.getenv("CI") == "true")
        logging.info("[browser] Chromium launched")
        yield browser


@pytest.fixture
def page(browser, request):
    context = browser.new_context(
        accept_downloads=True,
        record_video_dir="videos/",
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    page.set_default_timeout(15_000)
    logging.info(f"[page] New page opened for {request.node.name}")
    yield page
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    try:
        if failed:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
            os.makedirs("traces", exist_ok=True)
            trace_path = f"traces/{request.node.name}.zip"
            context.tracing.stop(path=trace_path)
            logging.info(f"[page] Trace saved → {trace_path} (open at trace.playwright.dev)")
        else:
            context.tracing.stop()
    finally:
        video = page.video
        page.close()
        context.close()
        if video:
            if failed:
                allure.attach(
                    Path(video.path()).read_bytes(),
                    name="video_on_failure",
                    attachment_type=allure.attachment_type.WEBM,
                )
            else:
                video.delete()


@pytest.fixture
def default_passenger():
    return PassengerDetails(
        name="John Doe",
        address="123 Main St",
        city="Springfield",
        state="IL",
        zip_code="62701",
        card_type="visa",
        credit_card_number="4111111111111111",
        credit_card_month="12",
        credit_card_year="2027",
        name_on_card="John Doe",
    )
