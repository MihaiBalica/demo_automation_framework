"""
UI pytest fixtures
"""

import logging

import allure
import pytest
from playwright.sync_api import Page

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def attach_screenshot_on_failure(request, page):
    """Attach a browser screenshot to the Allure report when a UI test fails."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        logger.warning(f"Test {request.node.nodeid} failed — attaching screenshot")
        allure.attach(
            page.screenshot(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )


def attach_screenshot(page: Page, name: str) -> None:
    """Capture a browser screenshot and attach it to the Allure report as a checkpoint."""
    logger.debug(f"Attaching screenshot: '{name}'")
    allure.attach(
        page.screenshot(full_page=True),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
