import pytest
from selenium import webdriver
import os
from urllib.parse import urljoin
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

SELENIUM_LOG_DIR_PATH = "~/.iotm/logs/test"


@pytest.fixture(scope="function")
def unauthed_selenium():
    sel = _get_verbose_selenium()
    yield sel
    sel.close()


def _get_verbose_selenium():
    # selenium debugging info: mind overwriting
    os.makedirs(os.path.expanduser(SELENIUM_LOG_DIR_PATH), exist_ok=True)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1420,1080")
    chrome_options.add_argument("--disable-gpu")

    # make sure chrome is running without cache
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--ignore-certificate-errors")

    # disable window pop up: change to False when debugging
    # TODO: change this to True when ran by CI
    chrome_options.headless = False

    return webdriver.Chrome(
        service_args=[
            "--verbose",
            os.path.expanduser(SELENIUM_LOG_DIR_PATH + "/selenium.log"),
        ],
        options=chrome_options
    )


@pytest.fixture(scope="module")
def make_authed_selenium(base_url):
    sel = _get_verbose_selenium()

    def _make_authed_selenium(user_name, password):
        sel.get(urljoin(base_url, "/accounts/login/"))

        sel.find_element_by_name("username").send_keys(user_name)
        sel.find_element_by_name("password").send_keys(password)

        # There should only be one button.
        submit_button = sel.find_elements_by_tag_name("button")[0]
        assert submit_button.text == "Login", "Cannot find Submit button."

        submit_button.click()
        try:
            WebDriverWait(sel, 30).until(lambda sel: "login" not in sel.current_url)
        except TimeoutException:
            pytest.fail("Does not log in successfully!")
        return sel

    return _make_authed_selenium


@pytest.fixture(scope="module")
def logout_authed_selenium(base_url):
    def _logout_authed_selenium(tenant_driver):
        sel = tenant_driver
        sel.get(urljoin(base_url, "/accounts/logout"))
        try:
            WebDriverWait(sel, 30).until(
                lambda sel: urljoin(base_url, "/accounts/login") in sel.current_url
            )
        except TimeoutException:
            pytest.fail("Does not log out successfully!")
        sel.close()

    return _logout_authed_selenium

