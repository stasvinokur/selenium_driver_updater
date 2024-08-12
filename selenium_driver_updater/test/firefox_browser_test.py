# Standard library imports
import logging
import platform
import pytest

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.browsers._firefoxBrowser import FirefoxBrowser

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def setup_firefoxbrowser():
    """Fixture to set up FirefoxBrowser for tests."""
    driver_name = "geckodriver_test.exe" if platform.system() == 'Windows' else "geckodriver_test"

    path = str(setting["Program"]["driversPath"]) + driver_name

    firefoxbrowser = FirefoxBrowser(path=path, check_browser=True)

    yield firefoxbrowser

    del firefoxbrowser


def test_check_get_latest_version_firefox_browser(setup_firefoxbrowser):
    latest_version = setup_firefoxbrowser._get_latest_version_firefox_browser()
    assert latest_version is not None
    assert len(latest_version) > 0


def test_check_get_latest_firefox_browser_for_current_os(setup_firefoxbrowser):
    # Test the function without any assert since it's more about side effects
    setup_firefoxbrowser._get_latest_firefox_browser_for_current_os()


def test_compare_current_version_and_latest_version_firefox_browser(setup_firefoxbrowser):
    is_browser_is_up_to_date, current_version, latest_version = setup_firefoxbrowser._compare_current_version_and_latest_version_firefox_browser()

    assert is_browser_is_up_to_date is not None
    assert current_version is not None
    assert latest_version is not None

    assert is_browser_is_up_to_date in [True, False]
    assert len(current_version) > 0
    assert len(latest_version) > 0


def test_check_geckodriver_is_up_to_date(setup_firefoxbrowser):
    setup_firefoxbrowser.main()