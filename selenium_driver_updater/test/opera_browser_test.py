# Standard library imports
import logging
import platform
import pytest

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.browsers._operaBrowser import OperaBrowser
from selenium_driver_updater.util.requests_getter import RequestsGetter

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def setup_operabrowser():
    """Fixture to set up OperaBrowser for tests."""
    driver_name = "operadriver_test.exe" if platform.system() == 'Windows' else "operadriver_test"
    path = str(setting["Program"]["driversPath"]) + driver_name

    operabrowser = OperaBrowser(path=path, check_browser=True)
    yield operabrowser

    del operabrowser


def test_get_result_by_request(setup_operabrowser):
    """Test to check if the request getter works."""
    url = str(setting["OperaBrowser"]["LinkAllLatestRelease"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0


def test_get_latest_version_opera_browser(setup_operabrowser):
    """Test to check if the latest version of Opera browser can be retrieved."""
    latest_version = setup_operabrowser._get_latest_version_opera_browser()
    assert latest_version is not None
    assert len(latest_version) > 0

def test_compare_opera_browser_versions(setup_operabrowser):
    """Test to compare the current version of Opera browser with the latest version."""
    setup_operabrowser._compare_opera_browser_versions()


def test_check_operadriver_is_up_to_date(setup_operabrowser):
    """Test to check if Opera browser driver is up to date."""
    setup_operabrowser.main()