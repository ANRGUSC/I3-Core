import pytest
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BUYER_USER_NAME = "test_buyer"
BUYER_USER_PSWD = "1234"

SELLER_USER_NAME = "xinting"
EXIST_HUB_NAME = "anime"
EXIST_PRODUCT_NAME = "Fullmetal"


@pytest.fixture(scope="module")
def buyer_user_browser(make_authed_selenium, logout_authed_selenium):
    buyer_driver = make_authed_selenium(
        # TODO: auto-create credentials
        BUYER_USER_NAME, BUYER_USER_PSWD
    )
    yield buyer_driver
    logout_authed_selenium(buyer_driver)


@pytest.fixture(autouse=True)
def buyer_user_sel(buyer_user_browser, base_url):
    time.sleep(3)
    buyer_user_browser.get(base_url)
    return buyer_user_browser


def go_to_product_page(buyer_user_sel):
    # Click on 'Hub' Option
    WebDriverWait(buyer_user_sel, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[.='Products']"))
    )
    hub_key = buyer_user_sel.find_element_by_xpath("//a[.='Products']")
    hub_key.click()

    try:
        WebDriverWait(buyer_user_sel, 5).until(
            lambda sel: "/products" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find Product Page")


def go_to_product_detail_page(buyer_user_sel, seller_user_name, hub_name, product_name):
    try:
        product_detail_button = buyer_user_sel.find_element_by_xpath(
            f"//a[contains(text(),'{seller_user_name}/{hub_name}/{product_name}')]"
        )
        product_detail_button.click()
    except NoSuchElementException:
        return "Could not find Product Detail Page"

    try:
        WebDriverWait(buyer_user_sel, 5).until(
            lambda sel: f"/{seller_user_name}{hub_name}{product_name}".lower() in sel.current_url
        )
        return product_name
    except TimeoutException:
        pytest.fail("Could not find Product Detail Page")


@pytest.mark.nondestructive
@pytest.mark.parametrize("seller_user_name, hub_name, product_name", [
    (SELLER_USER_NAME, EXIST_HUB_NAME, EXIST_PRODUCT_NAME),
    (SELLER_USER_NAME, "invalid_hub_name", EXIST_PRODUCT_NAME),
    (SELLER_USER_NAME, EXIST_HUB_NAME, "invalid_product_name")
])
def test_buyer_non_restricted(buyer_user_sel, seller_user_name, hub_name, product_name):
    go_to_product_page(buyer_user_sel)

    product_msg = go_to_product_detail_page(buyer_user_sel, seller_user_name, hub_name, product_name)
    if "invalid" in hub_name or "invalid" in product_name:
        assert product_name != product_msg
        return
    else:
        assert product_name == product_msg

    # add the product to cart and check out
    # TODO: add to test such as quantity increase etc
    add_to_cart_button = buyer_user_sel.find_element_by_xpath(
        "//td[div[@class='input-qty']]/button"
    )
    add_to_cart_button.click()

    try:
        WebDriverWait(buyer_user_sel, 5).until(
            lambda sel: "/cart" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find Cart Page")

    checkout_button = buyer_user_sel.find_element_by_xpath("//button[text()='Checkout']")
    checkout_button.click()

    try:
        WebDriverWait(buyer_user_sel, 5).until(
            lambda sel: "/dashboard/transactions" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not finish transactions!")

    # TODO: add more checks here


@pytest.mark.nondestructive
def test_buyer_restricted(buyer_user_sel):
    pass
