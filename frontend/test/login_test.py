from urllib.parse import urljoin
import time

import pytest
from selenium.common.exceptions import TimeoutException


@pytest.mark.nondestructive
def test_index(unauthed_selenium, base_url):
    unauthed_selenium.get(urljoin(base_url, "/"))

    # Assert that we are redirected to /login
    assert urljoin(base_url, "/accounts/login/") in unauthed_selenium.current_url, \
        "/ doesn't redirect to /login"


@pytest.mark.parametrize("user_name, password", [
    ("testuser", "12345"), ("testuser2", "1234")
])
@pytest.mark.nondestructive
def test_login_invalid_user(unauthed_selenium, base_url, user_name, password):
    sel = unauthed_selenium

    sel.get(urljoin(base_url, "/accounts/login/"))

    sel.find_element_by_name("username").send_keys(user_name)
    sel.find_element_by_name("password").send_keys(password)
    time.sleep(3)

    # There should only be one button.
    submit_button = sel.find_elements_by_tag_name("button")[0]
    assert submit_button.text == "Login", "Cannot find Submit button."

    submit_button.click()
    try:
        sel.find_element_by_class_name("text-danger")
    except TimeoutException:
        pytest.fail("Does not see error message!")
