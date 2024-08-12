# edgeDriverTest.py

# Standard library imports
from pathlib import Path
import logging
import pytest

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._edgeDriver import EdgeDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def setup_edgedriver():
    """Fixture to set up EdgeDriver for tests."""
    setting_local = setting

    path = str(setting_local["Program"]["driversPath"])

    # Correct parameters
    params_correct = dict(
        driver_name='edgedriver',
        path=path,
        info_messages=True,
        filename='edgedriver_test',
        version='',
        check_browser=False
    )

    edgedriver = EdgeDriver(**params_correct)

    # Incorrect parameters
    params_incorrect = params_correct.copy()
    params_incorrect.update(path='failure', filename='edgedriver1_test', version='blablabla')

    edgedriver_failure = EdgeDriver(**params_incorrect)

    return edgedriver, edgedriver_failure, setting_local


def test_check_get_current_version_edge_selenium_failure(setup_edgedriver):
    _, edgedriver_failure, _ = setup_edgedriver
    current_version = edgedriver_failure._get_current_version_driver()
    assert len(current_version) == 0, f"Unexpected current version: {current_version}"


def test_check_download_driver_failure(setup_edgedriver):
    _, edgedriver_failure, _ = setup_edgedriver
    with pytest.raises(DriverVersionInvalidException):
        edgedriver_failure._download_driver(version="blablablanotversion")


def test_compare_current_version_and_latest_version_failure(setup_edgedriver):
    _, edgedriver_failure, _ = setup_edgedriver
    with pytest.raises(DriverVersionInvalidException):
        is_driver_up_to_date, current_version, latest_version = edgedriver_failure._compare_current_version_and_latest_version()
        assert not is_driver_is_up_to_date
        assert len(current_version) == 0
        assert len(latest_version) == 0


def test_check_if_edgedriver_is_up_to_date_failure(setup_edgedriver):
    _, edgedriver_failure, _ = setup_edgedriver
    with pytest.raises(DriverVersionInvalidException):
        filename = edgedriver_failure.main()
        assert len(filename) == 0


def test_check_if_version_is_valid_failure(setup_edgedriver):
    _, edgedriver_failure, _ = setup_edgedriver
    with pytest.raises(DriverVersionInvalidException):
        edgedriver_failure._check_if_version_is_valid(url='blablablanoturl')


def test_check_get_result_by_request(setup_edgedriver):
    _, _, setting_local = setup_edgedriver
    url = str(setting_local["EdgeDriver"]["LinkLastRelease"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) >= 0


def test_check_download_driver_specific_version(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    edgedriver._delete_current_driver_for_current_os()
    edgedriver_path = edgedriver.driver_path
    assert not Path(edgedriver_path).exists()

    specific_version = '90.0.818.49'
    file_name = edgedriver._download_driver(version=specific_version)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(edgedriver_path).exists()

    edgedriver._chmod_driver()

    current_version = edgedriver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0
    assert current_version == specific_version


def test_download_driver_latest_previous_version(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    edgedriver._delete_current_driver_for_current_os()
    edgedriver_path = edgedriver.driver_path
    assert not Path(edgedriver_path).exists()

    file_name = edgedriver._download_driver(previous_version=True)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(edgedriver_path).exists()

    edgedriver._chmod_driver()

    current_version = edgedriver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0


def test_get_latest_version_edge_driver(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    latest_version = edgedriver._get_latest_version_driver()
    assert latest_version is not None
    assert len(latest_version) > 0


def test_delete_current_edgedriver_for_current_os(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    edgedriver._delete_current_driver_for_current_os()
    edgedriver_path = edgedriver.driver_path
    assert not Path(edgedriver_path).exists()


def test_download_driver(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    latest_version = edgedriver._get_latest_version_driver()
    assert latest_version is not None
    assert len(latest_version) > 0

    file_name = edgedriver._download_driver()
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(edgedriver.driver_path).exists()

    edgedriver._chmod_driver()


def test_compare_current_version_and_latest_version(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    is_driver_is_up_to_date, current_version, latest_version = edgedriver._compare_current_version_and_latest_version()
    assert is_driver_is_up_to_date is not None
    assert current_version is not None
    assert latest_version is not None
    assert is_driver_is_up_to_date
    assert len(current_version) > 0
    assert len(latest_version) > 0


def test_check_if_edgedriver_is_up_to_date(setup_edgedriver):
    edgedriver, _, _ = setup_edgedriver
    filename = edgedriver.main()
    assert len(filename) > 0


def test_check_if_version_is_valid(setup_edgedriver):
    edgedriver, _, setting_local = setup_edgedriver
    specific_version = '90.0.818.49'
    url = str(setting_local["EdgeDriver"]["LinkLastReleaseFile"]).format(specific_version)

    if 'mac64_m1' in url:
        try:
            edgedriver._check_if_version_is_valid(url=url)
        except Exception:
            url = url.replace('mac64_m1', 'mac64')
            edgedriver._check_if_version_is_valid(url=url)
    else:
        edgedriver._check_if_version_is_valid(url=url)