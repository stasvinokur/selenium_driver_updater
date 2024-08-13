import pytest
import logging

from selenium_driver_updater._safari_driver import SafariDriver
from selenium_driver_updater._setting import setting

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def safari_driver():
    """Fixture for initializing the SafariDriver."""
    path = str(setting["Program"]["driversPath"])
    params = dict(
        driver_name='safaridriver',
        path=path,
        info_messages=True,
        version='',
        check_browser=False
    )
    return SafariDriver(**params)

@pytest.fixture(scope="module")
def safari_driver_failure():
    """Fixture for initializing SafariDriver with failure settings."""
    params = dict(
        driver_name='safaridriver',
        path='failure',
        info_messages=True,
        version='blablabla',
        check_browser=False
    )
    return SafariDriver(**params)

def test_get_current_version_safari_driver_failure(safari_driver_failure):
    current_version = safari_driver_failure._get_current_version_driver()
    assert len(current_version) == 0

def test_compare_current_version_and_latest_version_safaridriver(safari_driver):
    safari_driver._compare_current_version_and_latest_version_safaridriver()

def test_get_latest_version_safaridriver(safari_driver):
    latest_version = safari_driver._get_latest_version_safaridriver()
    assert latest_version is not None
    assert len(latest_version) > 0

def test_safaridriver_main(safari_driver):
    try:
        driver_path = safari_driver.main()
        assert driver_path is not None
        assert len(driver_path) > 0
    except OSError: pass