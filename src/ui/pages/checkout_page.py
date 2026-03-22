"""
Checkout page objects
"""

import logging

from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutStepOnePage(BasePage):
    """Page object for checkout step one — customer information form."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill in the customer information form."""
        logger.info(
            f"Filling customer info: first_name='{first_name}', last_name='{last_name}', postal_code='{postal_code}'"
        )
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_step_two(self) -> None:
        """Click Continue to proceed to checkout step two."""
        logger.info("Continuing to checkout step two")
        self.continue_button.click()


class CheckoutStepTwoPage(BasePage):
    """Page object for checkout step two — order overview."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.finish_button = page.locator('[data-test="finish"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.summary_items = page.locator(".cart_item")

    def finish_checkout(self) -> None:
        """Click Finish to complete the purchase."""
        logger.info("Finishing checkout")
        self.finish_button.click()

    def get_summary_items(self) -> list:
        """Return list of item names in the order summary."""
        items = self.page.locator(".inventory_item_name").all()
        result = [item.inner_text() for item in items]
        logger.debug(f"Order summary items: {result}")
        return result


class CheckoutCompletePage(BasePage):
    """Page object for the checkout confirmation/complete page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.confirmation_header = page.locator(".complete-header")
        self.confirmation_text = page.locator(".complete-text")
        self.back_button = page.locator('[data-test="back-to-products"]')

    def get_confirmation_header(self) -> str:
        """Return the text of the confirmation header."""
        header = self.confirmation_header.inner_text()
        logger.info(f"Order confirmation: '{header}'")
        return header

    def is_order_complete(self) -> bool:
        """Return True if the order confirmation header is displayed."""
        complete = self.confirmation_header.is_visible()
        logger.debug(f"Order complete page visible: {complete}")
        return complete
