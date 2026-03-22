"""UI tests for Swag Labs (https://www.saucedemo.com/)."""

import allure
import pytest

from src.ui.pages.cart_page import CartPage
from src.ui.pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from src.ui.pages.inventory_page import ProductInventoryPage
from src.ui.pages.login_page import LoginPage
from tests.ui.conftest import attach_screenshot

PRODUCT_NAME = "Sauce Labs Backpack"


@allure.feature("Authentication")
@pytest.mark.ui
class TestLogin:
    """Tests covering the login functionality."""

    @allure.story("Valid Credentials Login")
    @allure.title("User can log in with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login_with_valid_credentials(self, page, config):
        """Scenario 1: Successful login with valid credentials."""
        with allure.step("Given the user is on the Swag Labs login page"):
            login_page = LoginPage(page)
            login_page.navigate(config["base_url"])

        with allure.step("When the user enters valid standard_user credentials and clicks Login"):
            login_page.login(
                config["credentials"]["standard_user"]["username"],
                config["credentials"]["standard_user"]["password"],
            )

        with allure.step("Then the user is redirected to the Products inventory page"):
            page.wait_for_url("**/inventory.html")
            inventory_page = ProductInventoryPage(page)
            assert inventory_page.get_page_title() == "Products"
            attach_screenshot(page, "inventory_page_after_login")

    @allure.story("Invalid Credentials Login")
    @allure.title("Login with invalid credentials shows an error message")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_failed_login_with_invalid_credentials(self, page, config):
        """Scenario 2: Failed login with invalid credentials — verify error message."""
        with allure.step("Given the user is on the Swag Labs login page"):
            login_page = LoginPage(page)
            login_page.navigate(config["base_url"])

        with allure.step("When the user enters invalid credentials and clicks Login"):
            login_page.login(
                config["credentials"]["invalid_user"]["username"],
                config["credentials"]["invalid_user"]["password"],
            )

        with allure.step("Then an error message is displayed indicating the credentials are wrong"):
            assert login_page.is_error_displayed(), "Error message should be visible"
            error_text = login_page.get_error_message()
            assert "Username and password do not match" in error_text or "do not match" in error_text
            attach_screenshot(page, "invalid_credentials_error")


@allure.feature("Shopping Cart")
@pytest.mark.ui
class TestShoppingCart:
    """Tests covering shopping cart functionality."""

    @allure.story("Add Item to Cart")
    @allure.title("Product can be added to the shopping cart from the inventory page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_product_to_cart(self, logged_in_page, config):
        """Scenario 3: Add a product to the shopping cart."""
        with allure.step("Given the user is logged in and on the inventory page"):
            inventory_page = ProductInventoryPage(logged_in_page)
            initial_count = inventory_page.get_cart_badge_count()

        with allure.step(f'When the user adds "{PRODUCT_NAME}" to the cart'):
            inventory_page.add_item_to_cart(PRODUCT_NAME)

        with allure.step("Then the cart badge count increases by one"):
            assert inventory_page.get_cart_badge_count() == initial_count + 1
            attach_screenshot(logged_in_page, "product_added_to_cart")

    @allure.story("Remove Item from Cart")
    @allure.title("Product can be removed from the shopping cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_product_from_cart(self, logged_in_page):
        """Scenario 4: Remove a product from the shopping cart."""
        with allure.step("Given the user has added a product to the cart"):
            inventory_page = ProductInventoryPage(logged_in_page)
            inventory_page.add_item_to_cart(PRODUCT_NAME)
            assert inventory_page.get_cart_badge_count() == 1

        with allure.step(f'When the user removes "{PRODUCT_NAME}" from the cart'):
            inventory_page.remove_item_from_cart(PRODUCT_NAME)

        with allure.step("Then the cart badge is no longer displayed"):
            assert inventory_page.get_cart_badge_count() == 0
            attach_screenshot(logged_in_page, "product_removed_from_cart")

    @allure.story("Cart Badge Update")
    @allure.title("Cart badge count reflects the number of items in the cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_badge_updates_correctly(self, logged_in_page):
        """Scenario 7 (optional): Verify cart badge updates correctly."""
        with allure.step("Given the user is logged in and the cart is empty"):
            inventory_page = ProductInventoryPage(logged_in_page)
            item_names = inventory_page.get_item_names()
            assert len(item_names) >= 2, "Expected at least two items in the inventory"

        with allure.step("When the user adds two items to the cart"):
            inventory_page.add_item_to_cart(item_names[0])
            assert inventory_page.get_cart_badge_count() == 1
            inventory_page.add_item_to_cart(item_names[1])

        with allure.step("Then the cart badge shows 2"):
            assert inventory_page.get_cart_badge_count() == 2

        with allure.step("And when the user removes one item, the cart badge shows 1"):
            inventory_page.remove_item_from_cart(item_names[0])
            assert inventory_page.get_cart_badge_count() == 1
            attach_screenshot(logged_in_page, "cart_badge_after_removal")


@allure.feature("Checkout Process")
@pytest.mark.ui
class TestCheckout:
    """Tests covering the end-to-end checkout flow."""

    @allure.story("End-to-End Purchase")
    @allure.title("User can complete the full checkout process")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_checkout_process(self, logged_in_page):
        """Scenario 5: Complete checkout process (end-to-end)."""
        with allure.step(f'Given the user has added "{PRODUCT_NAME}" to the cart'):
            inventory_page = ProductInventoryPage(logged_in_page)
            inventory_page.add_item_to_cart(PRODUCT_NAME)
            inventory_page.go_to_cart()

        with allure.step("And the product is confirmed in the cart"):
            cart_page = CartPage(logged_in_page)
            assert PRODUCT_NAME in cart_page.get_cart_items()
            attach_screenshot(logged_in_page, "cart_with_product")

        with allure.step("When the user proceeds to checkout and fills in customer information"):
            cart_page.proceed_to_checkout()
            checkout_step_one = CheckoutStepOnePage(logged_in_page)
            checkout_step_one.fill_customer_info("John", "Doe", "12345")
            checkout_step_one.continue_to_step_two()

        with allure.step("And the order summary is confirmed and the purchase is finished"):
            checkout_step_two = CheckoutStepTwoPage(logged_in_page)
            assert PRODUCT_NAME in checkout_step_two.get_summary_items()
            attach_screenshot(logged_in_page, "checkout_order_summary")
            checkout_step_two.finish_checkout()

        with allure.step("Then the order confirmation page is displayed with a thank-you message"):
            checkout_complete = CheckoutCompletePage(logged_in_page)
            assert checkout_complete.is_order_complete()
            assert "Thank you" in checkout_complete.get_confirmation_header()
            attach_screenshot(logged_in_page, "order_confirmation")


@allure.feature("Product Catalogue")
@pytest.mark.ui
class TestProductSorting:
    """Tests covering product sorting functionality."""

    @allure.story("Sort by Price")
    @allure.title("Products can be sorted by price from lowest to highest")
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_products_by_price_low_to_high(self, logged_in_page):
        """Scenario 6 (optional): Verify product sorting by price low-to-high."""
        with allure.step("Given the user is on the inventory page"):
            inventory_page = ProductInventoryPage(logged_in_page)

        with allure.step('When the user selects "Price (low to high)" from the sort dropdown'):
            inventory_page.sort_by("lohi")

        with allure.step("Then the products are displayed in ascending price order"):
            prices = inventory_page.get_item_prices()
            assert prices == sorted(prices), f"Prices should be sorted low-to-high, got: {prices}"
            attach_screenshot(logged_in_page, "products_sorted_price_low_to_high")

    @allure.story("Sort by Price")
    @allure.title("Products can be sorted by price from highest to lowest")
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_products_by_price_high_to_low(self, logged_in_page):
        """Verify product sorting by price high-to-low."""
        with allure.step("Given the user is on the inventory page"):
            inventory_page = ProductInventoryPage(logged_in_page)

        with allure.step('When the user selects "Price (high to low)" from the sort dropdown'):
            inventory_page.sort_by("hilo")

        with allure.step("Then the products are displayed in descending price order"):
            prices = inventory_page.get_item_prices()
            assert prices == sorted(prices, reverse=True), f"Prices should be sorted high-to-low, got: {prices}"
            attach_screenshot(logged_in_page, "products_sorted_price_high_to_low")

    @allure.story("Sort by Name")
    @allure.title("Products can be sorted alphabetically from A to Z")
    @allure.severity(allure.severity_level.MINOR)
    def test_sort_products_by_name_a_to_z(self, logged_in_page):
        """Verify product sorting by name A-to-Z."""
        with allure.step("Given the user is on the inventory page"):
            inventory_page = ProductInventoryPage(logged_in_page)

        with allure.step('When the user selects "Name (A to Z)" from the sort dropdown'):
            inventory_page.sort_by("az")

        with allure.step("Then the products are displayed in alphabetical order"):
            names = inventory_page.get_item_names()
            assert names == sorted(names), f"Names should be sorted A-Z, got: {names}"
            attach_screenshot(logged_in_page, "products_sorted_name_a_to_z")
