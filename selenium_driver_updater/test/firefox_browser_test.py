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


def test_compare_firefox_browser_versions(setup_firefoxbrowser):
    setup_firefoxbrowser._compare_firefox_browser_versions()


def test_check_geckodriver_is_up_to_date(setup_firefoxbrowser):
    setup_firefoxbrowser.main()