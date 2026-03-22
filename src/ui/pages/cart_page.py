"""
shopping cart page object
"""

import logging

from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Page object representing the Swag Labs shopping cart page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def get_cart_items(self) -> list:
        """Return a list of item names currently in the cart."""
        items = self.page.locator(".inventory_item_name").all()
        result = [item.inner_text() for item in items]
        logger.debug(f"Cart items: {result}")
        return result

    def remove_item(self, item_name: str) -> None:
        """Remove the specified item from the cart."""
        logger.info(f"Removing item from cart: '{item_name}'")
        item = self.page.locator(f'.cart_item:has-text("{item_name}")')
        item.locator('button[id^="remove"]').click()

    def get_cart_item_count(self) -> int:
        """Return the number of items in the cart."""
        count = self.cart_items.count()
        logger.debug(f"Cart item count: {count}")
        return count

    def proceed_to_checkout(self) -> None:
        """Click the Checkout button to proceed to checkout."""
        logger.info("Proceeding to checkout")
        self.checkout_button.click()
