"""
Base page class for the automation framework.
This class provides common functionality for all page objects
"""

import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        logger.info(f"Initialized {self.__class__.__name__} with URL: {self.page.url}")

    def navigate(self, url: str) -> None:
        """Navigate to the specified URL"""
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get the title of the current page"""
        title = self.page.title()
        logger.info(f"Current page title: {title}")
        return title
    
    def wait_for_url(self, url: str) -> None:
        """Wait for the URL to match the specified value"""
        logger.debug(f"Waiting for URL to be: {url}")
        self.page.wait_for_url(url)
