import pytest
import platform
import os

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.browsers._edgeBrowser import EdgeBrowser
from selenium_driver_updater.util.requests_getter import RequestsGetter

@pytest.fixture(scope="module")
def edge_browser_setup():
    """Setup fixture for EdgeBrowser tests."""
    driver_name = "edgedriver_test.exe" if platform.system() == 'Windows' else "edgedriver_test"
    path = os.path.join(setting["Program"]["driversPath"], driver_name)
    
    edge_browser = EdgeBrowser(path=path, check_browser=True)
    yield edge_browser

def test_get_result_by_request():
    """Test to check getting result by request."""
    url = str(setting["EdgeBrowser"]["LinkAllLatestRelease"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0

def test_get_latest_version_edge_browser(edge_browser_setup, ):
    """Test to check getting the latest version of Edge browser."""
    latest_version = edge_browser_setup._get_latest_version_edge_browser()
    assert latest_version is not None
    assert len(latest_version) > 0

def test_compare_current_version_and_latest_version_edge_browser(edge_browser_setup, ):
    """Test to compare the current version and latest version of Edge browser."""
    edge_browser_setup._compare_current_version_and_latest_version_edge_browser()

def test_if_edgebrowser_is_up_to_date(edge_browser_setup, ):
    """Test to check if Edge browser is up to date."""
    edge_browser_setup.main()