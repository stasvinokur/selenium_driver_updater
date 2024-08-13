# Standard library imports
import os.path
import time
import platform
import logging
from pathlib import Path
import pytest

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._operaDriver import OperaDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def setup_operadriver():
    """Fixture to set up OperaDriver for tests."""
    setting_local = setting
    path = str(setting_local["Program"]["driversPath"])

    params_correct = dict(
        driver_name='operadriver',
        path=path,
        info_messages=True,
        filename='operadriver_test',
        version='',
        check_browser=False
    )

    operadriver = OperaDriver(**params_correct)

    params_incorrect = params_correct.copy()
    params_incorrect.update(path='failure', filename='operadriver1_test', version='blablabla')

    operadriver_failure = OperaDriver(**params_incorrect)

    return operadriver, operadriver_failure


def test_get_current_version_operadriver_selenium_failure(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    with pytest.raises(DriverVersionInvalidException):
        operadriver_failure._get_current_version_driver()


def test_download_driver_failure(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    with pytest.raises(DriverVersionInvalidException):
        operadriver_failure._download_driver(version="blablablanotversion")


def test_compare_current_version_and_latest_version_failure(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    with pytest.raises(DriverVersionInvalidException):
        operadriver_failure._compare_current_version_and_latest_version_github()


def test_check_if_operadriver_is_up_to_date_failure(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    with pytest.raises(DriverVersionInvalidException):
        operadriver_failure.main()


def test_check_if_version_is_valid_failure(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    with pytest.raises(DriverVersionInvalidException):
        operadriver_failure._check_if_version_is_valid(url='blablablanoturl')


def test_download_driver_specific_version(setup_operadriver):
    operadriver, _ = setup_operadriver
    operadriver._delete_current_driver_for_current_os()
    operadriver_path = operadriver.driver_path
    assert not Path(operadriver_path).exists()

    specific_version = '89.0.4389.82'
    file_name = operadriver._download_driver(version=specific_version)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(operadriver_path).exists()

    operadriver._chmod_driver()

    current_version = operadriver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0
    assert current_version == specific_version


def test_download_driver_latest_previous_version(setup_operadriver):
    operadriver, _ = setup_operadriver
    operadriver._delete_current_driver_for_current_os()
    operadriver_path = operadriver.driver_path
    assert not Path(operadriver_path).exists()

    file_name = operadriver._download_driver(previous_version=True)
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(operadriver_path).exists()

    operadriver._chmod_driver()

    current_version = operadriver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0


def test_get_latest_version_operadriver(setup_operadriver):
    operadriver, _ = setup_operadriver
    latest_version = operadriver._get_latest_version_driver_github()
    assert latest_version is not None
    assert len(latest_version) > 0


def test_delete_current_operadriver_for_current_os(setup_operadriver):
    operadriver, _ = setup_operadriver
    operadriver._delete_current_driver_for_current_os()
    operadriver_path = operadriver.driver_path
    assert not Path(operadriver_path).exists()


def test_download_driver(setup_operadriver):
    operadriver, _ = setup_operadriver
    file_name = operadriver._download_driver()
    assert file_name is not None
    assert len(file_name) > 0
    assert Path(operadriver.driver_path).exists()

    operadriver._chmod_driver()


def test_compare_current_version_and_latest_version(setup_operadriver):
    operadriver, _ = setup_operadriver
    is_driver_is_up_to_date, current_version, latest_version = operadriver._compare_current_version_and_latest_version_github()
    assert is_driver_is_up_to_date is not None
    assert current_version is not None
    assert latest_version is not None
    assert is_driver_is_up_to_date
    assert len(current_version) > 0
    assert len(latest_version) > 0


def test_get_current_version_operadriver_selenium(setup_operadriver):
    operadriver, _ = setup_operadriver
    current_version = operadriver._get_current_version_driver()
    assert current_version is not None
    assert len(current_version) > 0


def test_check_if_operadriver_is_up_to_date(setup_operadriver):
    operadriver, _ = setup_operadriver
    filename = operadriver.main()
    assert len(filename) > 0


def test_check_if_version_is_valid(setup_operadriver):
    _, operadriver_failure = setup_operadriver
    specific_version = '89.0.4389.82'
    url = str(setting["OperaDriver"]["LinkLastReleasePlatform"]).format(specific_version)
    operadriver_failure._check_if_version_is_valid(url=url)