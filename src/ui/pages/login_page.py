"""
Login page object
"""

import logging

from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object representing the Swag Labs login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input = page.locator('[data-test="username"]')
        self.password_input = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error_message = page.locator('[data-test="error"]')

    def login(self, username: str, password: str) -> None:
        """Perform login with the given credentials."""
        logger.info(f"Logging in as {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Return the text of the error message displayed on the login page."""
        text = self.error_message.inner_text()
        logger.warning(f"Login error displayed: {text}")
        return text

    def is_error_displayed(self) -> bool:
        """Return True if an error message is visible."""
        visible = self.error_message.is_visible()
        logger.debug(f"Login error message visible: {visible}")
        return visible
