"""
products page object
"""

import logging

from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductInventoryPage(BasePage):
    """
    Page object representing the Swag Labs inventory/products page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.page_title = page.locator(".title")
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')

    def get_page_title(self) -> str:
        """Return the title text displayed on the inventory page."""
        title = self.page_title.inner_text()
        logger.debug(f"Inventory page title: {title}")
        return title

    def add_item_to_cart(self, item_name: str) -> None:
        """Add the specified item to the shopping cart by name."""
        logger.info(f"Adding item to cart: {item_name}")
        item = self.page.locator(f'.inventory_item:has-text("{item_name}")')
        item.locator('button[id^="add-to-cart"]').click()

    def remove_item_from_cart(self, item_name: str) -> None:
        """Remove the specified item from the shopping cart by name."""
        logger.info(f"Removing item from cart: {item_name}")
        item = self.page.locator(f'.inventory_item:has-text("{item_name}")')
        item.locator('button[id^="remove"]').click()

    def get_cart_badge_count(self) -> int:
        """Return the number shown in the cart badge."""
        if self.cart_badge.is_visible():
            count = int(self.cart_badge.inner_text())
            logger.debug(f"Cart badge count: {count}")
            return count
        logger.debug("Cart badge not visible, returning 0")
        return 0

    def go_to_cart(self) -> None:
        """Click the shopping cart icon to navigate to the cart page."""
        logger.info("Navigating to cart")
        self.cart_link.click()

    def sort_by(self, option_value: str) -> None:
        """Sort products using the sort dropdown by selecting an option value."""
        logger.info(f"Sorting products by {option_value}")
        self.sort_dropdown.select_option(option_value)

    def get_item_prices(self) -> list:
        """Return a list of item prices as floats."""
        prices = self.page.locator(".inventory_item_price").all()
        result = [float(p.inner_text().replace("$", "")) for p in prices]
        logger.debug(f"Item prices: {result}")
        return result

    def get_item_names(self) -> list:
        """Return a list of item names."""
        names = self.page.locator(".inventory_item_name").all()
        result = [n.inner_text() for n in names]
        logger.debug(f"Item names: {result}")
        return result
