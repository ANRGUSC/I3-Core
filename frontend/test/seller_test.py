import secrets
import pytest
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SELLER_USER_NAME = "testuser"
SELLER_USER_PSWD = "1234"

EXIST_HUB_NAME = "anime"
NEW_HUB_NAME = "testHub"
NEW_PRODUCT_NAME = "testProduct"
NEW_DEVICE_NAME = "testDevice"
NEW_DEVICE_PSWD = "123456"


@pytest.fixture(scope="module")
def seller_user_browser(make_authed_selenium, logout_authed_selenium):
    seller_driver = make_authed_selenium(
        # TODO: auto-create credentials
        SELLER_USER_NAME, SELLER_USER_PSWD
    )
    yield seller_driver
    logout_authed_selenium(seller_driver)


@pytest.fixture(autouse=True)
def seller_user_sel(seller_user_browser, base_url):
    time.sleep(3)
    seller_user_browser.get(base_url)
    return seller_user_browser


def user_create_hub(seller_user_sel):
    assert '/hubs' in seller_user_sel.current_url

    create_hub_key = seller_user_sel.find_element_by_xpath("//div[@class='container']//button")
    create_hub_key.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/hubs/create" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find create hub key")

    hub_name_input = seller_user_sel.find_element_by_xpath("//input[@id='id_name']")
    hub_name_input.send_keys(NEW_HUB_NAME)
    hub_name_input.send_keys(Keys.ENTER)

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "create" not in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not create hub")

    seller_user_sel.find_element_by_xpath(f"//a[.='{SELLER_USER_NAME}/{NEW_HUB_NAME}']")

    return NEW_HUB_NAME


def user_delete_hub(seller_user_sel, created_hub_name=None):
    if created_hub_name is None:
        pytest.fail("Should not delete non-specified hub")

    assert '/hubs' in seller_user_sel.current_url

    created_hub = seller_user_sel.find_element_by_xpath(f"//a[.='{SELLER_USER_NAME}/{created_hub_name}']")
    created_hub.click()

    # TODO: how to delete a hub


# assume this action only happens after hub has been successfully created
def user_create_product(seller_user_sel, parent_hub_name=None, new_product_name=NEW_PRODUCT_NAME):
    if parent_hub_name is None:
        pytest.fail("Should not create product under non-specified hub")

    create_product = seller_user_sel.find_element_by_xpath("//button[contains(text(),'Create Product')]")
    create_product.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/products/create" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find create product button")

    product_title_input = seller_user_sel.find_element_by_xpath("//input[@id='id_title']")
    product_title_input.send_keys(new_product_name)

    parent_hub_input = seller_user_sel.find_element_by_xpath("//input[@id='id_hub']")
    parent_hub_input.send_keys(parent_hub_name)

    parent_hub_input = seller_user_sel.find_element_by_xpath("//textarea[@id='id_description']")
    random_description = secrets.token_urlsafe(16)
    parent_hub_input.send_keys(random_description)

    submit_create_product = seller_user_sel.find_element_by_xpath("//button[contains(text(),'Create')]")
    submit_create_product.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: f"/products/{SELLER_USER_NAME}{parent_hub_name}{new_product_name}".lower() in sel.current_url
        )
    except TimeoutException:
        return "Could not create and show product!"

    # TODO: add more UI checks here
    seller_user_sel.find_element_by_xpath(f"//p[contains(text(), '{random_description}')]")
    return new_product_name


# assume this action only happens after product has been successfully created
def user_delete_product(seller_user_sel, parent_hub_name=None, product_name=None):
    if parent_hub_name is None or product_name is None:
        pytest.fail("Should not delete product under non-specified hub")

    delete_product = seller_user_sel.find_element_by_xpath(
        f"//h4[a/text()='{SELLER_USER_NAME}/{parent_hub_name}/{product_name}']//button[contains(text(),'Delete Product')]"
    )
    delete_product.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/products/delete" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not delete product!")

    # TODO: add more UI checks here


# assume this action only happens after hub has been successfully created
def user_create_device_api_key(
        seller_user_sel, parent_hub_name=None,
        new_device_name=NEW_DEVICE_NAME, new_device_pswd=NEW_DEVICE_PSWD
):
    if parent_hub_name is None:
        pytest.fail("Should not create product under non-specified hub")

    create_product = seller_user_sel.find_element_by_xpath("//button[contains(text(),'Create Device')]")
    create_product.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/devices/create" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find create device button")

    hub_name_input = seller_user_sel.find_element_by_xpath("//input[@id='id_hub_name']")
    hub_name_input.send_keys(parent_hub_name)

    device_name_input = seller_user_sel.find_element_by_xpath("//input[@id='id_name']")
    device_name_input.send_keys(new_device_name)

    # select API keys

    device_password_input = seller_user_sel.find_element_by_xpath("//input[@id='id_password']")
    device_password_input.send_keys(new_device_pswd)

    submit_create_product = seller_user_sel.find_element_by_xpath("//button[contains(text(),'Create')]")
    submit_create_product.click()

    # TODO: more UI tests here
    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/hubs" in sel.current_url
        )
    except TimeoutException:
        return "Could not create device!"
    return new_device_name


# assume this action only happens after device has been successfully created
def user_delete_device(seller_user_sel, parent_hub_name=None, device_name=None):
    if parent_hub_name is None or device_name is None:
        pytest.fail("Should not delete device under non-specified hub")

    delete_product = seller_user_sel.find_element_by_xpath(
        f"//h4[contains(text(), '{SELLER_USER_NAME}${parent_hub_name}${device_name}')]//button[contains(text(),'Delete Device')]"
    )
    delete_product.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/devices/delete" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not delete product!")

    # TODO: add more UI checks here


def go_to_hub_page(seller_user_sel):
    # Click on 'Hub' Option
    WebDriverWait(seller_user_sel, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[.='Hubs']"))
    )
    hub_key = seller_user_sel.find_element_by_xpath("//a[.='Hubs']")
    hub_key.click()

    try:
        WebDriverWait(seller_user_sel, 5).until(
            lambda sel: "/hubs" in sel.current_url
        )
    except TimeoutException:
        pytest.fail("Could not find Hub Page")


def go_to_hub_specific_page(seller_user_sel, hub_name=None):
    if hub_name is None:
        pytest.fail("Please specify hub name!")
    go_to_hub_page(seller_user_sel)
    hub_link = seller_user_sel.find_element_by_xpath(f"//a[.='{SELLER_USER_NAME}/{hub_name}']")
    hub_link.click()


@pytest.mark.nondestructive
@pytest.mark.parametrize("hub_name, new_product_name", [
    (EXIST_HUB_NAME, NEW_PRODUCT_NAME), (EXIST_HUB_NAME, "test_invalid_name")
])
def test_user_crud_product(seller_user_sel, hub_name, new_product_name):
    go_to_hub_page(seller_user_sel)

    # go to created hub page
    go_to_hub_specific_page(seller_user_sel, hub_name=hub_name)

    product_name = user_create_product(
        seller_user_sel, parent_hub_name=hub_name, new_product_name=new_product_name
    )

    if "invalid" in new_product_name:
        # TODO: add more checks for invalid product name input
        assert product_name != new_product_name, f"Error message is {product_name}"
        return
    else:
        assert product_name == new_product_name

    go_to_hub_specific_page(seller_user_sel, hub_name=hub_name)

    user_delete_product(seller_user_sel, parent_hub_name=hub_name, product_name=product_name)


@pytest.mark.nondestructive
@pytest.mark.parametrize("hub_name, new_device_name, new_device_pswd", [
    (EXIST_HUB_NAME, NEW_DEVICE_NAME, NEW_DEVICE_PSWD),
    (EXIST_HUB_NAME, "invalid_device_name", NEW_DEVICE_PSWD),
    (EXIST_HUB_NAME, NEW_DEVICE_NAME, "pswd")
])
def test_user_crud_device(seller_user_sel, hub_name, new_device_name, new_device_pswd):
    go_to_hub_page(seller_user_sel)

    # go to created hub page
    go_to_hub_specific_page(seller_user_sel, hub_name=hub_name)

    device_name = user_create_device_api_key(
        seller_user_sel, parent_hub_name=hub_name,
        new_device_name=new_device_name, new_device_pswd=new_device_pswd
    )

    if "invalid" in new_device_name or len(new_device_pswd) < 6:
        # TODO: add more checks for invalid product name input
        assert device_name != new_device_name, f"Error message is {device_name}"
        return
    else:
        assert device_name == new_device_name

    go_to_hub_specific_page(seller_user_sel, hub_name=hub_name)

    user_delete_device(seller_user_sel, parent_hub_name=hub_name, device_name=device_name)









