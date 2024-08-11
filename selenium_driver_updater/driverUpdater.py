#pylint: disable=logging-fstring-interpolation, protected-access, broad-except
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

    check_browser_is_up_to_date = False
    enable_library_update_check = True

class DriverUpdater():
    """Main class for working with all drivers"""

    #DRIVERS
    chromedriver = 'chromedriver'
    geckodriver = 'geckodriver'
    operadriver = 'operadriver'
    edgedriver = 'edgedriver'
    phantomjs = 'phantomjs'
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
            version (str)                       : Specific version for driver. If given, it will downloads given version. Defaults to empty string.
            check_browser_is_up_to_date (bool)  : If true, it will check browser version before specific driver update or upgrade. Defaults to False.
            enable_library_update_check (bool)  : If true, it will enable checking for library update while starting. Defaults to True.
            system_name (Union[str, list[str]]) : Specific OS for driver. Defaults to empty string.

        Returns:
            str

            driver_path (str)       : Path where Selenium driver binary was downloaded or updated.

        """

        #Initialize all variables
        message_run:str = ''

        driver_path = ''

        _info.driver_name = driver_name

        _info.info_messages = bool(kwargs.get('info_messages', True))

        if _info.info_messages:
            logger.setLevel(levels['info'])
        else:
            logger.setLevel(levels['error'])

        path = kwargs.get('path')
        if not path:
            path = os.getcwd()
            logger.info('You have not specified the path - so used default folder path instead')

        _info.path = str(os.path.abspath(path) + os.path.sep)

        _info.filename = str(kwargs.get('filename', '')).replace('.', '') if type(kwargs.get('filename', '')) not in [list, dict, tuple] else kwargs.get('filename', '')

        _info.enable_library_update_check = bool(kwargs.get('enable_library_update_check', True))

        _info.version = str(kwargs.get('version', '')) if type(kwargs.get('version', '')) not in [list, dict, tuple] else kwargs.get('version', '')

        _info.check_browser_is_up_to_date = bool(kwargs.get('check_browser_is_up_to_date', False))

        _info.system_name = kwargs.get('system_name', '')

        if any([kwargs.get('chmod') is not None,  kwargs.get('upgrade') is not None, kwargs.get('check_driver_is_up_to_date') is not None]):
            logger.warning('You are using one of the parameters chmod, upgrade, check_driver_is_up_to_date which have been deprecated, please remove it from your code')
            
        try:

            DriverUpdater.__check_enviroment_and_variables()

            if isinstance(_info.driver_name, str):

                driver_path = DriverUpdater.__run_specific_driver()

            elif isinstance(_info.driver_name, list):

                list_of_paths : list[str] = []

                for i, driver in enumerate(_info.driver_name):

                    time.sleep(1) #small sleep

                    try:
                        filename_driver = str(_info.filename[i])
                        filename_driver = filename_driver.replace('.', '')
                    except IndexError:
                        filename_driver = ''

                    try:
                        system_name_driver = str(_info.system_name[i])
                    except IndexError:
                        system_name_driver = ''

                    try:
                        version_driver = str(_info.version[i])
                    except IndexError:
                        version_driver = ''

                    driver_path = DriverUpdater.__run_specific_driver(driver_name=driver, filename=filename_driver, system_name=system_name_driver, version=version_driver, index=i)
                    list_of_paths.append(driver_path)

                    driver_path = list_of_paths

        except KeyboardInterrupt:
            # Locating paths of .tmp files
            tmp_files = glob.glob(os.path.join(_info.path, "*.tmp"))
            
            # Removing of .tmp files
            for tmp_file in tmp_files:
                try:
                    os.remove(tmp_file)
                except Exception: pass

        except Exception:

            message_run = f'error: {str(traceback.format_exc())}'
            logger.error(message_run)

        return driver_path

    @staticmethod
    def __check_all_input_parameteres() -> None:
        """Private function for checking all input parameters"""


        if not Path(_info.path).exists() and _info.path.endswith(os.path.sep):
            message = f"The specified path does not exist current path is: {_info.path}, trying to create this directory"
            logger.error(message)
            Path(_info.path).mkdir()
            logger.info(f'Successfully created new directory at path: {_info.path}')

        if not Path(_info.path).is_dir():
            message = f"The specified path is not a directory current path is: {_info.path}"
            raise NotADirectoryError(message)

        if isinstance(_info.driver_name,(list, str)):

            if _info.filename:

                if isinstance(_info.driver_name,list) and isinstance(_info.filename, str):
                    _info.filename = [_info.filename]

                DriverUpdater.__check_parameter_type_is_valid(_info.filename, type(_info.driver_name), 'filename')

            if _info.system_name:

                DriverUpdater.__check_parameter_type_is_valid(_info.system_name, type(_info.driver_name), 'system_name')

            if _info.version:
                DriverUpdater.__check_parameter_type_is_valid(_info.version, type(_info.driver_name), 'version')

            if _info.system_name:
                if isinstance(_info.driver_name, str):
                    DriverUpdater.__check_system_name_is_valid(system_name=_info.system_name)
                elif isinstance(_info.driver_name, list):
                    for os_system in _info.system_name:
                        DriverUpdater.__check_system_name_is_valid(system_name=os_system)

        else:

            message = f'The type of "driver_name" must be a list or str current type is: {type(_info.driver_name)}'
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
        """Private function for run download or update for specific driver

        Args:
            driver_name (Union[str, list[str]]) : Specified driver name/names which will be downloaded or updated. Like "DriverUpdater.chromedriver" or etc.
            filename (str)                      : Specific name for chromedriver. If given, it will replace name for chromedriver. Defaults to empty string.
            version (str)                       : Specific version for chromedriver. If given, it will downloads given version. Defaults to empty string.
            system_name (Union[str, list[str]]) : Specific OS for driver. Defaults to empty string.

        Returns:
            str

            driver_path (str) : Path where specific driver located

        """

        driver_path: str = ''
        index:str = ''

        driver_name = kwargs.get('driver_name', _info.driver_name)
        filename = kwargs.get('filename', _info.filename)
        version = kwargs.get('version', _info.version)
        system_name = kwargs.get('system_name', _info.system_name)

        parametres = dict(  driver_name=driver_name, path=_info.path,
                            filename=filename, version=version,
                            check_browser_is_up_to_date=_info.check_browser_is_up_to_date,
                            info_messages=_info.info_messages,
                            system_name=system_name )

        if _info.system_name:
            index = kwargs.get('index', None)
            if index is not None:
                setting['Program']['DriversFileFormat'] = '.exe' if 'win' in _info.system_name[index] or 'arm' in _info.system_name[index] else ''
            else:
                setting['Program']['DriversFileFormat'] = '.exe' if 'win' in _info.system_name or 'arm' in _info.system_name else ''
        try:
            driver = ALL_DRIVERS[driver_name](**parametres)
        except KeyError:
            index = kwargs.get('index', None)
            if index:
                message = f'Unknown driver name at index: {index} was specified current driver_name is: {driver_name}'
            else:
                message = f'Unknown driver name was specified current driver_name is: {driver_name}'
            raise NameError(message)

        driver_path = driver.main()

        return driver_path

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
