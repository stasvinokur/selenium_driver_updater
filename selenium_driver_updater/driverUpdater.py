#Standart library imports
from dataclasses import dataclass
from pathlib import Path
import os
from typing import Any
import time
import sys
import traceback
from packaging import version
import glob

# Local imports

from selenium_driver_updater.util import ALL_DRIVERS

from selenium_driver_updater._setting import setting

from selenium_driver_updater.util.requests_getter import RequestsGetter

from selenium_driver_updater.util.logger import logger
from selenium_driver_updater.util.logger import levels

@dataclass
class _info():

    driver_name: Any = ''

    path = ''
    filename = ''
    version = ''
    system_name: Any = ''

    info_messages = False

    check_browser = False
    enable_library_update_check = True

class DriverUpdater():
    """Main class for working with all drivers"""

    #DRIVERS
    chromedriver = 'chromedriver'
    chromedriver_beta = 'chromedriver_beta'
    chromedriver_dev = 'chromedriver_dev'
    chromedriver_canary = 'chromedriver_canary'

    geckodriver = 'geckodriver'
    operadriver = 'operadriver'

    edgedriver = 'edgedriver'
    edgedriver_beta = 'edgedriver_beta'
    edgedriver_dev = 'edgedriver_dev'
    edgedriver_canary = 'edgedriver_canary'

    safaridriver = 'safaridriver'

    #OS'S
    windows = 'win64'
    windows32 = 'win32'
    windows64 = 'win64'

    linux = 'linux64'
    linux32 = 'linux32'
    linux64 = 'linux64'

    macos = 'mac64'
    macos_m1 = 'mac64_m1'

    arm = 'arm64'

    @staticmethod
    def install(driver_name, **kwargs):
        """Function for install or update Selenium driver binary

        Args:
            driver_name (Union[str, list[str]]) : Specified driver name/names which will be downloaded or updated. Like "DriverUpdater.chromedriver" or etc.
            path (str)                          : Specified path which will used for downloading or updating Selenium driver binary. Must be folder path.
            info_messages (bool)                : If false, it will disable all info messages. Defaults to True.
            filename (str)                      : Specific name for driver. If given, it will replace current name for driver. Defaults to empty string.
            version (str)                       : Specific channel version for driver (beta, dev, canary). If given, it will download given channel latest version. Defaults to empty string.
            check_browser (bool)                : If true, it will check browser version before specific driver update or upgrade. Defaults to False.
            enable_library_update_check (bool)  : If true, it will enable checking for library update while starting. Defaults to True.
            system_name (Union[str, list[str]]) : Specific OS for driver. Defaults to empty string.

        Returns:
            str

            driver_path (str)       : Path where Selenium driver binary was downloaded or updated.

        """
        
        _info.info_messages = bool(kwargs.get('info_messages', True))
        DriverUpdater.__set_logging_level()
        DriverUpdater.__initialize_info(driver_name, **kwargs)

        try:
            DriverUpdater.__check_enviroment_and_variables()
            return DriverUpdater.__process_drivers()
        except KeyboardInterrupt:
            DriverUpdater.__cleanup_tmp_files()
        except Exception:
            logger.error(f'error: {str(traceback.format_exc())}')
            return ''
    
    @staticmethod
    def __initialize_info(driver_name, **kwargs):
        """Initialize the _info dataclass with provided parameters."""
        
        if any([kwargs.get('chmod') is not None,  kwargs.get('upgrade') is not None, kwargs.get('check_driver_is_up_to_date') is not None]):
            logger.warning('You are using one of the parameters chmod, upgrade, check_driver_is_up_to_date which have been deprecated, please remove it from your code')
        elif kwargs.get('check_browser_is_up_to_date'):
            logger.warning('Parameter check_browser_is_up_to_date is now check_browser, please rename it in your code')

        _info.driver_name = driver_name
        _info.path = DriverUpdater.__get_path(kwargs.get('path'))
        _info.filename = DriverUpdater.__sanitize_filename(kwargs.get('filename'))
        _info.enable_library_update_check = bool(kwargs.get('enable_library_update_check', True))
        _info.version = DriverUpdater.__sanitize_version(kwargs.get('version'))
        _info.check_browser = bool(kwargs.get('check_browser', False))
        _info.system_name = kwargs.get('system_name', '')

    @staticmethod
    def __get_path(path):
        if not path:
            path = os.getcwd()
            logger.info('You have not specified the path - so used default folder path instead')
        return str(os.path.abspath(path) + os.path.sep)

    @staticmethod
    def __sanitize_filename(filename):
        if isinstance(filename, (list, dict, tuple)):
            return filename
        return str(filename or '').replace('.', '')

    @staticmethod
    def __sanitize_version(version):
        if isinstance(version, (list, dict, tuple)):
            return version
        return str(version or '')

    @staticmethod
    def __set_logging_level():
        if _info.info_messages:
            logger.setLevel(levels['info'])
        else:
            logger.setLevel(levels['error'])

    @staticmethod
    def __process_drivers():
        """Process the driver installation or update based on provided driver_name."""
        if isinstance(_info.driver_name, str):
            return DriverUpdater.__run_specific_driver()
        elif isinstance(_info.driver_name, list):
            return DriverUpdater.__process_multiple_drivers()

    @staticmethod
    def __process_multiple_drivers():
        """Process installation or update for multiple drivers."""
        list_of_paths = []
        for i, driver in enumerate(_info.driver_name):
            time.sleep(1)  # small sleep
            driver_path = DriverUpdater.__run_specific_driver(
                driver_name=driver,
                filename=DriverUpdater.__get_item_or_default(_info.filename, i),
                system_name=DriverUpdater.__get_item_or_default(_info.system_name, i),
                version=DriverUpdater.__get_item_or_default(_info.version, i),
                index=i
            )
            list_of_paths.append(driver_path)
        return list_of_paths

    @staticmethod
    def __get_item_or_default(lst, index, default=''):
        try:
            return str(lst[index]).replace('.', '')
        except IndexError:
            return default

    @staticmethod
    def __cleanup_tmp_files():
        """Locate and remove any .tmp files left over after an interruption."""
        tmp_files = glob.glob(os.path.join(_info.path, "*.tmp"))
        for tmp_file in tmp_files:
            try:
                os.remove(tmp_file)
            except Exception:
                pass

    @staticmethod
    def __check_all_input_parameteres() -> None:
        """Private function for checking all input parameters"""
        DriverUpdater.__check_path_validity()
        DriverUpdater.__check_driver_name_type()
        DriverUpdater.__check_filename_type()
        DriverUpdater.__check_system_name_type()
        DriverUpdater.__check_version_type()
        DriverUpdater.__validate_system_names()

    @staticmethod
    def __check_path_validity() -> None:
        if not Path(_info.path).exists() and _info.path.endswith(os.path.sep):
            message = f"The specified path does not exist. Current path is: {_info.path}. Trying to create this directory."
            logger.error(message)
            Path(_info.path).mkdir()
            logger.info(f'Successfully created new directory at path: {_info.path}')

        if not Path(_info.path).is_dir():
            message = f"The specified path is not a directory. Current path is: {_info.path}"
            raise NotADirectoryError(message)

    @staticmethod
    def __check_driver_name_type() -> None:
        if not isinstance(_info.driver_name, (list, str)):
            message = f'The type of "driver_name" must be a list or str. Current type is: {type(_info.driver_name)}'
            raise ValueError(message)

    @staticmethod
    def __check_filename_type() -> None:
        if _info.filename:
            if isinstance(_info.driver_name, list) and isinstance(_info.filename, str):
                _info.filename = [_info.filename]
            DriverUpdater.__check_parameter_type_is_valid(_info.filename, type(_info.driver_name), 'filename')

    @staticmethod
    def __check_system_name_type() -> None:
        if _info.system_name:
            DriverUpdater.__check_parameter_type_is_valid(_info.system_name, type(_info.driver_name), 'system_name')

    @staticmethod
    def __check_version_type() -> None:
        valid_versions = {
            'chromedriver_beta', 
            'chromedriver_dev', 
            'chromedriver_canary',
            'edgedriver_beta', 
            'edgedriver_dev', 
            'edgedriver_canary'
        }

        if _info.version and _info.version not in valid_versions:
            message = f"Invalid version specified: {_info.version}. Must be one of {', '.join(valid_versions)}."
            raise ValueError(message)

    @staticmethod
    def __validate_system_names() -> None:
        if _info.system_name:
            if isinstance(_info.driver_name, str):
                DriverUpdater.__check_system_name_is_valid(system_name=_info.system_name)
            elif isinstance(_info.driver_name, list):
                for os_system in _info.system_name:
                    DriverUpdater.__check_system_name_is_valid(system_name=os_system)

    @staticmethod
    def __check_parameter_type_is_valid(parameter, needed_type, parameter_name) -> None:
        if not isinstance(parameter, needed_type):
            message = f'The type of {parameter_name} must be a {needed_type}. Current type is: {type(parameter)}'
            raise TypeError(message)

    @staticmethod
    def __check_system_name_is_valid(system_name) -> None:
        """Private function for checking if the specified system_name exists and is valid"""
        system_name_check = system_name in [DriverUpdater.__dict__[item] for item in DriverUpdater.__dict__]
        if not system_name_check:
            message = f'Unknown system name was specified. Current system_name is: {system_name}'
            raise ValueError(message)


    @staticmethod
    def __check_library_is_up_to_date() -> None:
        """Private function for comparing latest version and current version of program"""

        url : str = str(setting["PyPi"]["urlProjectJson"])

        if 'b' not in str(setting["Program"]["version"]).lower():

            json_data = RequestsGetter.get_result_by_request(url=url, is_json=True)

            current_version = str(setting["Program"]["version"])
            latest_version = json_data.get('info').get('version')

            if version.parse(latest_version) > version.parse(current_version):
                message = ('Your selenium-driver-updater library is out of date,'
                        'please update it via "pip install selenium-driver-updater --upgrade" '
                        f'current_version: {current_version} latest_version: {latest_version} ')
                logger.warning(message)

            elif version.parse(latest_version) == version.parse(current_version):
                message = 'Your selenium-driver-updater library is up to date.'
                logger.info(message)

            else:
                message = 'Unable to compare the latest version and the current version of the library.'
                logger.error(message)

        else:

            message = ('Thanks for participating in beta releases for selenium-driver-updater library,'
                        f'you are using the beta version {str(setting["Program"]["version"])}')
            logger.info(message)
            message = 'Note that beta version does not guarantee errors avoiding. If something goes wrong - please create an issue on github repository'
            logger.info(message)

            message = 'Github repository link: https://github.com/Svinokur/selenium_driver_updater'
            logger.info(message)

    @staticmethod
    def __check_is_python_version_compatible_for_library() -> None:
        """Private function for checking if python version if compatible with python version 3+"""

        major = str(sys.version_info[0])
        minor = str(sys.version_info[1])
        patch = str(sys.version_info[2])

        python_version = f"{major}.{minor}.{patch}"

        if major != "3":
            message = (f"selenium-driver-updater works only on Python 3, you are using {python_version} which is unsupported by this library, "
                        f"you may have some troubles or errors if you will proceed.")
            logger.warning(message)

    @staticmethod
    def __check_enviroment_and_variables() -> None:
        """Private function for checking all input parameters and enviroment"""

        DriverUpdater.__check_is_python_version_compatible_for_library()

        if _info.enable_library_update_check:

            DriverUpdater.__check_library_is_up_to_date()

        DriverUpdater.__check_all_input_parameteres()

    @staticmethod
    def __run_specific_driver(**kwargs) -> str:
        """Private function for running download or update for a specific driver."""

        driver_name, filename, version, system_name = DriverUpdater.__extract_parameters(kwargs)
        DriverUpdater.__set_driver_file_format(system_name, kwargs.get('index', None))

        try:
            driver = ALL_DRIVERS[driver_name](**DriverUpdater.__create_parameters(driver_name, filename, version, system_name))
        except KeyError:
            DriverUpdater.__handle_invalid_driver_name(driver_name, kwargs.get('index', None))

        driver_path = driver.main()
        return driver_path

    @staticmethod
    def __extract_parameters(kwargs):
        driver_name = kwargs.get('driver_name', _info.driver_name)
        filename = kwargs.get('filename', _info.filename)
        version = kwargs.get('version', _info.version)
        system_name = kwargs.get('system_name', _info.system_name)
        return driver_name, filename, version, system_name

    @staticmethod
    def __set_driver_file_format(system_name, index=None):
        if _info.system_name:
            if index is not None:
                setting['Program']['DriversFileFormat'] = '.exe' if 'win' in _info.system_name[index] or 'arm' in _info.system_name[index] else ''
            else:
                setting['Program']['DriversFileFormat'] = '.exe' if 'win' in _info.system_name or 'arm' in _info.system_name else ''

    @staticmethod
    def __create_parameters(driver_name, filename, version, system_name):
        return dict(
            driver_name=driver_name,
            path=_info.path,
            filename=filename,
            version=version,
            check_browser=_info.check_browser,
            info_messages=_info.info_messages,
            system_name=system_name
        )

    @staticmethod
    def __handle_invalid_driver_name(driver_name, index=None):
        if index:
            message = f'Unknown driver name at index: {index} was specified. Current driver_name is: {driver_name}'
        else:
            message = f'Unknown driver name was specified. Current driver_name is: {driver_name}'
        raise NameError(message)

    @staticmethod
    def __check_system_name_is_valid(system_name) -> None:
        """Private function for checking if specified system_name is exists and valid"""

        system_name_check = system_name in [DriverUpdater.__dict__[item] for item in DriverUpdater.__dict__]

        if not system_name_check:
            message = f'Unknown system name was specified current system_name is: {system_name}'
            raise ValueError(message)

    @staticmethod
    def __check_parameter_type_is_valid(parameter, needed_type, parameter_name) -> None:

        if not isinstance(parameter, needed_type):
            message = f'The type of {parameter_name} must be a {needed_type} current type is: {type(parameter)}'
            raise TypeError(message)
