import platform
import pytest
import os
from pathlib import Path

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._geckoDriver import GeckoDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

@pytest.fixture(scope="module")
def gecko_driver_setup():
    """Setup fixture for GeckoDriver tests."""
    path = str(setting["Program"]["driversPath"])

    params = dict(
        driver_name='geckodriver',
        path=path,
        info_messages=True,
        filename='geckodriver_test',
        version='',
        check_browser=False
    )
    gecko_driver = GeckoDriver(**params)

    params_failure = dict(
        driver_name='geckodriver',
        path='failure',
        info_messages=True,
        filename='geckodriver1_test',
        version='blablablanotversion',
        check_browser=False
    )
    gecko_driver_failure = GeckoDriver(**params_failure)

    yield gecko_driver, gecko_driver_failure

    # Cleanup code if needed
    if Path(gecko_driver.driver_path).exists():
        Path(gecko_driver.driver_path).unlink()

@pytest.fixture()
def setup_paths(gecko_driver_setup):
    """Setup paths for the tests."""
    gecko_driver, _ = gecko_driver_setup
    path = str(setting["Program"]["driversPath"])
    geckodriver_name = "geckodriver_test.exe" if platform.system() == 'Windows' else "geckodriver_test"
    geckodriver_path = os.path.join(path, geckodriver_name)
    return gecko_driver, geckodriver_path

def test_get_current_version_geckodriver_selenium_failure(gecko_driver_setup):
    """Test to check getting current version of GeckoDriver."""
    _, gecko_driver_failure = gecko_driver_setup
    current_version = gecko_driver_failure._get_current_version_driver()
    assert len(current_version) == 0

def test_download_driver_failure(gecko_driver_setup):
    """Test downloading driver with failure."""
    _, gecko_driver_failure = gecko_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        gecko_driver_failure._download_driver(version='blablablanotversion')

def test_compare_current_version_and_latest_version_failure(gecko_driver_setup):
    """Test comparing current and latest versions with failure."""
    _, gecko_driver_failure = gecko_driver_setup
    is_driver_is_up_to_date, current_version, latest_version = gecko_driver_failure._compare_current_version_and_latest_version_github()
    assert not is_driver_is_up_to_date
    assert len(current_version) == 0
    assert len(latest_version) == 0

def test_geckodriver_is_up_to_date_failure(gecko_driver_setup):
    """Test if GeckoDriver is up to date with failure."""
    _, gecko_driver_failure = gecko_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        gecko_driver_failure.main()

def test_if_version_is_valid_failure(gecko_driver_setup):
    """Test if a specific version is valid with failure."""
    _, gecko_driver_failure = gecko_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        gecko_driver_failure._check_if_version_is_valid(url='blablablanoturl')

def test_download_driver_specific_version(setup_paths):
    """Test downloading a specific version of GeckoDriver."""
    gecko_driver, geckodriver_path = setup_paths
    gecko_driver._delete_current_driver_for_current_os()
    assert not Path(geckodriver_path).exists()

    file_name = gecko_driver._download_driver(version='0.29.1')
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(geckodriver_path).exists()

    gecko_driver._chmod_driver()

    current_version = gecko_driver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0
    assert current_version == '0.29.1'

def test_download_driver_latest_previous_version(setup_paths):
    """Test downloading the latest previous version of GeckoDriver."""
    gecko_driver, geckodriver_path = setup_paths
    gecko_driver._delete_current_driver_for_current_os()
    assert not Path(geckodriver_path).exists()

    file_name = gecko_driver._download_driver(previous_version=True)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(geckodriver_path).exists()

    gecko_driver._chmod_driver()

    current_version = gecko_driver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0

def test_get_latest_version_gecko_driver(gecko_driver_setup):
    """Test getting the latest version of GeckoDriver."""
    gecko_driver, _ = gecko_driver_setup
    latest_version = gecko_driver._get_latest_version_driver_github()
    assert latest_version is not None
    assert len(latest_version) > 0

def test_delete_current_geckodriver_for_current_os(setup_paths):
    """Test deleting the current GeckoDriver for the current OS."""
    gecko_driver, geckodriver_path = setup_paths
    gecko_driver._delete_current_driver_for_current_os()
    assert not Path(geckodriver_path).exists()

def test_download_driver(setup_paths):
    """Test downloading the latest version of GeckoDriver."""
    gecko_driver, geckodriver_path = setup_paths
    file_name = gecko_driver._download_driver()
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(geckodriver_path).exists()

    gecko_driver._chmod_driver()

def test_compare_current_version_and_latest_version(gecko_driver_setup):
    """Test comparing current and latest versions."""
    gecko_driver, _ = gecko_driver_setup
    is_driver_is_up_to_date, current_version, latest_version = gecko_driver._compare_current_version_and_latest_version_github()
    assert is_driver_is_up_to_date
    assert current_version is not None
    assert len(current_version) > 0
    assert latest_version is not None
    assert len(latest_version) > 0

def test_get_current_version_firefox_selenium(gecko_driver_setup):
    """Test getting the current version of Firefox used by Selenium."""
    gecko_driver, _ = gecko_driver_setup
    current_version = gecko_driver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0

def test_geckodriver_is_up_to_date(gecko_driver_setup):
    """Test if GeckoDriver is up to date."""
    gecko_driver, _ = gecko_driver_setup
    filename = gecko_driver.main()
    assert len(filename) > 0

def test_if_version_is_valid(gecko_driver_setup):
    """Test if a specific version of GeckoDriver is valid."""
    gecko_driver, _ = gecko_driver_setup
    url = str(setting["GeckoDriver"]["LinkLastReleasePlatform"]).format('0.29.1', '0.29.1')
    gecko_driver._check_if_version_is_valid(url=url)