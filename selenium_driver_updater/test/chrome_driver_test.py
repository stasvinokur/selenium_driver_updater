import platform
import pytest
import os
from pathlib import Path

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._chromeDriver import ChromeDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

@pytest.fixture(scope="module")
def chrome_driver_setup():
    """Setup fixture for ChromeDriver tests."""
    path = str(setting["Program"]["driversPath"])

    params = dict(
        driver_name='chromedriver',
        path=path,
        info_messages=True,
        filename='chromedriver_test',
        version='',
        check_browser=False
    )
    chrome_driver = ChromeDriver(**params)

    params_failure = dict(
        driver_name='chromedriver',
        path='failure',
        info_messages=True,
        filename='chromedriver1_test',
        version='blablabla',
        check_browser=False
    )
    chrome_driver_failure = ChromeDriver(**params_failure)

    yield chrome_driver, chrome_driver_failure

    # Cleanup code if needed
    if Path(chrome_driver.driver_path).exists():
        Path(chrome_driver.driver_path).unlink()

@pytest.fixture()
def setup_paths(chrome_driver_setup):
    """Setup paths for the tests."""
    chrome_driver, _ = chrome_driver_setup
    path = str(setting["Program"]["driversPath"])
    chromedriver_name = "chromedriver_test.exe" if platform.system() == 'Windows' else "chromedriver_test"
    chromedriver_path = os.path.join(path, chromedriver_name)
    return chrome_driver, chromedriver_path

def test_get_current_version_chrome_selenium_failure(chrome_driver_setup):
    """Test to check getting current version of ChromeDriver."""
    _, chrome_driver_failure = chrome_driver_setup
    current_version = chrome_driver_failure._get_current_version_driver()
    assert len(current_version) == 0

def test_download_driver_failure(chrome_driver_setup):
    """Test downloading driver with failure."""
    _, chrome_driver_failure = chrome_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        chrome_driver_failure._download_driver(version='blablablanotversion')

def test_compare_current_version_and_latest_version_failure(chrome_driver_setup):
    """Test comparing current and latest versions with failure."""
    _, chrome_driver_failure = chrome_driver_setup
    is_driver_is_up_to_date, current_version, latest_version = chrome_driver_failure._compare_current_version_and_latest_version()
    assert not is_driver_is_up_to_date
    assert len(current_version) == 0
    assert len(latest_version) == 0

def test_chromedriver_is_up_to_date_failure(chrome_driver_setup):
    """Test if ChromeDriver is up to date with failure."""
    _, chrome_driver_failure = chrome_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        chrome_driver_failure.main()

def test_if_version_is_valid_failure(chrome_driver_setup):
    """Test if a specific version is valid with failure."""
    _, chrome_driver_failure = chrome_driver_setup
    with pytest.raises(DriverVersionInvalidException):
        chrome_driver_failure._check_if_version_is_valid(url='blablablanoturl')

def test_get_result_by_request(chrome_driver_setup):
    """Test getting the result by request."""
    _, _ = chrome_driver_setup
    url = str(setting["ChromeDriver"]["LinkLastRelease"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0

def test_get_latest_version_driver(chrome_driver_setup):
    """Test getting the latest version of ChromeDriver."""
    chrome_driver, _ = chrome_driver_setup
    latest_version = chrome_driver._get_latest_version_driver()
    assert latest_version is not None
    assert len(latest_version) > 0

    latest_previous_version = latest_version.split(".", maxsplit=1)[0]

    url = str(setting["ChromeDriver"]["LinkLatestReleaseSpecificVersion"]).format(latest_previous_version)
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0

def test_download_driver_specific_version(setup_paths):
    """Test downloading a specific version of ChromeDriver."""
    chrome_driver, chromedriver_path = setup_paths
    chrome_driver._delete_current_driver_for_current_os()
    assert not Path(chromedriver_path).exists()

    file_name = chrome_driver._download_driver(version='115.0.5763.0')
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(chromedriver_path).exists()

    chrome_driver._chmod_driver()

    current_version = chrome_driver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0
    assert current_version == '115.0.5763.0'

def test_download_driver_latest_previous_version(setup_paths):
    """Test downloading the latest previous version of ChromeDriver."""
    chrome_driver, chromedriver_path = setup_paths
    chrome_driver._delete_current_driver_for_current_os()
    assert not Path(chromedriver_path).exists()

    file_name = chrome_driver._download_driver(previous_version=True)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(chromedriver_path).exists()

    chrome_driver._chmod_driver()

    current_version = chrome_driver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0

def test_download_driver(setup_paths):
    """Test downloading the latest version of ChromeDriver."""
    chrome_driver, chromedriver_path = setup_paths
    latest_version = chrome_driver._get_latest_version_driver()
    assert latest_version is not None
    assert len(latest_version) > 0

    file_name = chrome_driver._download_driver()
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(chromedriver_path).exists()

    chrome_driver._chmod_driver()

def test_compare_current_version_and_latest_version(chrome_driver_setup):
    """Test comparing current and latest versions."""
    chrome_driver, _ = chrome_driver_setup
    is_driver_is_up_to_date, current_version, latest_version = chrome_driver._compare_current_version_and_latest_version()
    assert is_driver_is_up_to_date
    assert current_version is not None
    assert len(current_version) > 0
    assert latest_version is not None
    assert len(latest_version) > 0

def test_chromedriver_is_up_to_date(chrome_driver_setup):
    """Test if ChromeDriver is up to date."""
    chrome_driver, _ = chrome_driver_setup
    filename = chrome_driver.main()
    assert len(filename) > 0

def test_if_version_is_valid(chrome_driver_setup):
    """Test if a specific version of ChromeDriver is valid."""
    chrome_driver, _ = chrome_driver_setup
    url = str(setting["ChromeDriver"]["LinkLastReleaseFile"]).format('115.0.5763.0')
    chrome_driver._check_if_version_is_valid(url=url)