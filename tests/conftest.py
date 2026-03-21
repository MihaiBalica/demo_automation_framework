"""
Pytest fixtures for the test suite.
"""

import logging

import pytest
from playwright.sync_api import sync_playwright

from src.utils.helpers import get_credentials, load_config

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config():
    """Load and return the test configuration."""
    logger.info("Loading test configuration")
    return load_config()


@pytest.fixture(scope="session")
def browser_instance(config):
    """Launch a browser instance for the test session."""
    browser_name = config.get("browser", "chromium")
    headless = config.get("headless", True)
    logger.info(f"Launching {browser_name} browser (headless={headless})")
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=headless)
        yield browser
        logger.info("Closing browser")
        browser.close()


@pytest.fixture(scope="function")
def browser_context(browser_instance, config):
    """Create a fresh browser context for each test function."""
    timeout = config.get("timeout", 30000)
    logger.debug("Creating new browser context (timeout=%sms)", timeout)
    context = browser_instance.new_context()
    context.set_default_timeout(timeout)
    yield context
    logger.debug("Closing browser context")
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    """Create a new page in the browser context."""
    logger.debug("Opening new page")
    p = browser_context.new_page()
    yield p
    logger.debug("Closing page")
    p.close()


@pytest.fixture(scope="function")
def logged_in_page(page, config):
    """Provide a page already logged in as standard_user."""
    from src.pages.login_page import LoginPage

    logger.info("Setting up logged-in page for standard_user")
    login_page = LoginPage(page)
    login_page.navigate(config["base_url"])
    username, password = get_credentials(config, "standard_user")
    login_page.login(username, password)
    page.wait_for_url("**/inventory.html")
    logger.info("Login complete — on inventory page")
    yield page
