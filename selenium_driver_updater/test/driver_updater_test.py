import os.path
import pytest

# Local imports
from selenium_driver_updater.driverUpdater import DriverUpdater, _info
from selenium_driver_updater._setting import setting
from selenium_driver_updater.util.requests_getter import RequestsGetter

base_dir = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="module")
def driver_updater_setup():
    """Setup fixture for DriverUpdater tests."""
    return DriverUpdater

@pytest.fixture()
def setup_info():
    """Setup fixture for _info."""
    _info.path = base_dir
    _info.driver_name = 'chromedriver'
    _info.system_name = 'linux64'
    _info.filename = ''
    _info.version = ''
    _info.check_browser = False
    _info.enable_library_update_check = True
    yield _info

def test_check_all_input_parameteres_failure(driver_updater_setup, setup_info):
    # Set incorrect values in the _info object to simulate failure
    setup_info.driver_name = 123  # Invalid type, should be str or list
    setup_info.filename = 67890  # Invalid type, should be str
    setup_info.system_name = 'invalid_system_name'  # Invalid system name

    with pytest.raises(ValueError):
        driver_updater_setup._DriverUpdater__check_all_input_parameteres()

def test_check_enviroment_and_variables_failure(driver_updater_setup, setup_info):
    # Set incorrect values in the _info object to simulate failure
    setup_info.driver_name = 123  # Invalid type, should be str or list
    setup_info.filename = 67890  # Invalid type, should be str
    setup_info.system_name = 'invalid_system_name'  # Invalid system name
    with pytest.raises(ValueError):
        driver_updater_setup._DriverUpdater__check_enviroment_and_variables()

def test_check_system_name_is_valid_failure(driver_updater_setup, setup_info):
    invalid_system_name = 'linux6412312'
    with pytest.raises(ValueError):
        driver_updater_setup._DriverUpdater__check_system_name_is_valid(system_name=invalid_system_name)

def test_check_parameter_type_is_valid(driver_updater_setup, setup_info):
    with pytest.raises(TypeError):
        driver_updater_setup._DriverUpdater__check_parameter_type_is_valid(parameter='aboba', needed_type=list, parameter_name='driver_name')

def test_check_get_result_by_request():
    url = str(setting["PyPi"]["urlProjectJson"])
    json_data = RequestsGetter.get_result_by_request(url=url)
    assert len(json_data) > 0

def test_check_library_is_up_to_date(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_library_is_up_to_date()

def test_check_is_python_version_compatible_for_library(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_is_python_version_compatible_for_library()

def test_check_all_input_parameteres(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_all_input_parameteres()

def test_check_enviroment_and_variables(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_enviroment_and_variables()

def test_check_system_name_is_valid(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_system_name_is_valid(system_name=_info.system_name)

def test_check_parameter_type_is_valid(driver_updater_setup, setup_info):
    driver_updater_setup._DriverUpdater__check_parameter_type_is_valid(parameter=_info.driver_name, needed_type=str, parameter_name='driver_name')

def test_install_driver(driver_updater_setup, setup_info):
    driver_path = driver_updater_setup.install('chromedriver', path=base_dir, system_name='linux64')
    assert driver_path is not None
    assert isinstance(driver_path, str)

def test_install_multiple_drivers(driver_updater_setup, setup_info):
    driver_names = ['chromedriver', 'geckodriver']
    driver_paths = driver_updater_setup.install(driver_names, path=base_dir)
    
    assert isinstance(driver_paths, list)
    assert all(isinstance(path, str) for path in driver_paths)

    # Cleanup: Delete the downloaded drivers
    for driver_path in driver_paths:
        if os.path.exists(driver_path):
            os.remove(driver_path)
            assert not os.path.exists(driver_path)  # Ensure the file was deleted