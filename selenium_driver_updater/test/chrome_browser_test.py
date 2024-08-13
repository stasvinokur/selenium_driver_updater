import pytest
import platform
import os

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.browsers._chromeBrowser import ChromeBrowser
from selenium_driver_updater.util.requests_getter import RequestsGetter

@pytest.fixture(scope="module")
def chrome_browser_setup():
    """Setup fixture for ChromeBrowser tests."""
    driver_name = "chromedriver_test.exe" if platform.system() == 'Windows' else "chromedriver_test"
    path = os.path.join(setting["Program"]["driversPath"], driver_name)
    
    chrome_browser = ChromeBrowser(path=path, check_browser=True)
    yield chrome_browser

def test_get_result_by_request():
    """Test to check getting result by request."""
    url = str(setting["ChromeBrowser"]["LinkAllLatestRelease"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0

def test_get_current_version_chrome_selenium(chrome_browser_setup, ):
    """Test to check getting the current version of Chrome using Selenium."""
    current_version = chrome_browser_setup._get_current_version_chrome_browser_selenium()
    assert current_version is not None
    assert len(current_version) > 0

def test_get_latest_version_chrome_browser(chrome_browser_setup, ):
    """Test to check getting the latest version of Chrome browser."""
    latest_version = chrome_browser_setup._get_latest_version_chrome_browser()
    assert latest_version is not None
    assert len(latest_version) > 0

def test_compare_chrome_browser_versions(chrome_browser_setup, ):
    """Test to compare the current version and latest version of Chrome browser."""
    chrome_browser_setup._compare_chrome_browser_versions()

def test_chromedriver_is_up_to_date(chrome_browser_setup, ):
    """Test to check if ChromeDriver is up to date."""
    chrome_browser_setup.main()