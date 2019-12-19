## Install
* Pytest and pytest-base-url(plugin):
    * `pip install pytest`
    * `pip install pytest-base-url`
    * Pytest documentation is [here](https://docs.pytest.org/en/latest/)
* Selenium:
    * `pip install selenium`
    * Selenium documentation is [here](https://selenium-python.readthedocs.io/)
* Chromedriver:
    * See [this](https://sites.google.com/a/chromium.org/chromedriver/downloads) for more details
        * Mac Users: `brew cask install chromedriver`
        * Linux Users: 
            * `wget -N http://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip`
            * `unzip chromedriver_linux64.zip`
            * `chmod +x chromedriver`
            * `sudo mv -f chromedriver /usr/local/share/chromedriver`
            * `sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver`
            * `sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver`

## Run
* Run `pytest frontend/test/login_test.py --base-url http://18.219.4.146:8000`
* To select a specific fucntion: use `-k pattern`
* To drop into debugger upon error: use `--pdb`

## Task List on I3 UI Tests
- [ ] Create seller user
- [ ] Create buyer user
- [x] Create hub
- [x] Create product under hub
- [x] Create invalid product name
- [x] Create repeat product name
- [ ] Create product under invalid hub name
- [x] Create device under hub -> keep password
- [x] Create invalid device name
- [x] Create repeat device name
- [ ] Create device under invalid hub name
- [x] Buy product (non-restricted)
- [x] Delete product
- [x] Delete device
- [ ] Delete hub (Note: this functionality is not exposed)

## Other TODOs
* Test environment dependencies should be configured via pipenv or alike
* Tests are running on Chrome only as of now: it can be extended to Firefox etc by installing other web drivers.
* Tests for creating users through UI
* Create automated tests for API and MQTT endpoints 

