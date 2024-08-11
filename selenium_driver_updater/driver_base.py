#Standart library imports
from typing import Any, Tuple
from pathlib import Path
import os
import stat
import subprocess
import re
import wget

#Local imports
from selenium_driver_updater._setting import setting

from selenium_driver_updater.util.extractor import Extractor
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.github_viewer import GithubViewer
from selenium_driver_updater.util.logger import logger
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

#pylint: disable=logging-fstring-interpolation
class DriverBase():
    "Base class for all drivers classes in selenium_driver_updater"

    def __init__(self, **kwargs):

        self.driver_name = str(kwargs.get('driver_name'))

        self.driver_name_setting = str(kwargs.get('driver_name'))
        self.driver_name_setting = self.driver_name_setting.title().replace('driver', 'Driver').replace('js', 'JS')

        #Default variables
        self.filename = ''

        self.setting : Any = setting

        self.path : str = str(kwargs.get('path'))

        self.version = str(kwargs.get('version'))

        self.info_messages = bool(kwargs.get('info_messages'))

        self.extractor = Extractor
        self.requests_getter = RequestsGetter
        self.github_viewer = GithubViewer

        specific_filename = str(kwargs.get('filename'))
        if specific_filename:
            self.filename = specific_filename + self.setting['Program']['DriversFileFormat']

        driver_name = 'ms' + self.driver_name if self.driver_name == 'edgedriver' else self.driver_name
        self.setting[self.driver_name_setting]['LastReleasePlatform'] = driver_name

        self.setting[self.driver_name_setting]['LastReleasePlatform'] += self.setting['Program']['DriversFileFormat']

        self.driver_path = self.path + self.setting[self.driver_name_setting]['LastReleasePlatform'] if not self.filename else self.path + self.filename

        self.repo_name = str(kwargs.get('repo_name'))

    def _get_latest_version_driver(self, no_messages : bool = False) -> str:
        """Gets latest driver version

        Returns:
            str

            latest_version (str)  : Latest version of specific driver.

        """

        latest_version : str = ''

        url = self.setting[self.driver_name_setting]["LinkLastRelease"]
        json_data = self.requests_getter.get_result_by_request(url=url)

        latest_version = str(json_data).strip()

        if not no_messages:

            logger.info(f'Latest version of {self.driver_name}: {latest_version}')

        return latest_version

    def _get_latest_version_driver_github(self) -> str:
        """Gets latest driver version via github api / site


        Returns:
            str

            latest_version (str)    : Latest version of driver

        """

        latest_version : str = ''

        latest_version = self.github_viewer.get_release_version_by_repo_name(repo_name=self.repo_name)

        logger.info(f'Latest version of {self.driver_name}: {latest_version}')

        return latest_version

    def _chmod_driver(self) -> None:
        """Tries to give specific driver needed permissions"""

        if Path(self.driver_path).exists():

            logger.info(f'Trying to give {self.driver_name} needed permissions')

            file_st = os.stat(self.driver_path)
            os.chmod(self.driver_path, file_st.st_mode | stat.S_IEXEC)

            logger.info(f'Needed rights for {self.driver_name} were successfully issued')

    def _delete_current_driver_for_current_os(self) -> None:
        """Deletes specific driver from folder if parameter "upgrade" is True"""

        if Path(self.driver_path).exists():

            logger.info(f'Deleted existing {self.driver_name} {self.driver_name}_path: {self.driver_path}')
            Path(self.driver_path).unlink()

    def _get_current_version_driver(self) -> str:
        """Gets current driver version via command in terminal

        Returns:
            str

            driver_version (str) : Current driver version.

        Raises:

            OSError: Occurs when driver made for another CPU type

        """

        driver_version : str = ''
        driver_version_terminal : str = ''

        try:

            if Path(self.driver_path).exists():

                with subprocess.Popen([self.driver_path, '--version'], stdout=subprocess.PIPE) as process:
                    driver_version_terminal = process.communicate()[0].decode('UTF-8')

                find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], driver_version_terminal)
                driver_version = find_string[0] if len(find_string) > 0 else ''

                logger.info(f'Current version of {self.driver_name}: {driver_version}')

        except OSError:
            pass #[Errno 86] Bad CPU type in executable:

        return driver_version

    def _compare_current_version_and_latest_version(self) -> Tuple[bool, str, str]:
        """Compares current version of driver to latest version

        Returns:
            Tuple of bool, str and str

            is_driver_up_to_date (bool) : It true the driver is up to date. Defaults to False.
            current_version (str)       : Current version of the driver.
            latest_version (str)        : Latest version of the driver.

        """

        is_driver_up_to_date : bool = False
        current_version : str = ''
        latest_version : str = ''

        current_version = self._get_current_version_driver()

        if not current_version:
            return is_driver_up_to_date, current_version, latest_version

        latest_version = self._get_latest_version_driver()

        if current_version == latest_version:
            is_driver_up_to_date = True
            message = (f'Your existing {self.driver_name} is up to date. '
                        f'current_version: {current_version} latest_version: {latest_version}')
            logger.info(message)

        return is_driver_up_to_date, current_version, latest_version

    def _compare_current_version_and_latest_version_github(self) -> Tuple[bool, str, str]:
        """Compares current version of driver to latest version

        Returns:
            Tuple of bool, str and str

            is_driver_up_to_date (bool) : It true the driver is up to date. Defaults to False.
            current_version (str)       : Current version of the driver.
            latest_version (str)        : Latest version of the driver.

        """

        is_driver_up_to_date : bool = False
        current_version : str = ''
        latest_version : str = ''

        current_version = self._get_current_version_driver()

        if not current_version:
            return is_driver_up_to_date, current_version, latest_version

        latest_version = self._get_latest_version_driver_github()

        if current_version == latest_version:
            is_driver_up_to_date = True
            message = (f'Your existing {self.driver_name} is up to date. '
                       f'current_version: {current_version} latest_version: {latest_version}')
            logger.info(message)

        return is_driver_up_to_date, current_version, latest_version

    def _check_if_version_is_valid(self, url : str) -> None:
        """Checks the specified version for existence."""

        archive_name : str = url.split("/")[len(url.split("/"))-1]

        find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], url)
        driver_version = find_string[0] if len(find_string) > 0 else ''

        if 'chromedriver' in archive_name:
            url_test_valid = self.setting[self.driver_name_setting]["LinkCheckVersionIsValid"]
            archive_platform = archive_name.split('-', maxsplit=1)[1].split('.')[0]

            version_valid : str = f"{driver_version}/{archive_platform}/{archive_name}"
        else:
            url_test_valid = self.setting[self.driver_name_setting]["LinkCheckVersionIsValid"].format(driver_version)
            version_valid : str = f"{driver_version}/{archive_name}"

        json_data = self.requests_getter.get_result_by_request(url=url_test_valid)

        if version_valid not in json_data or not driver_version:
            message = ('Wrong version or system_name was specified.'
                        f'version_valid: {version_valid} driver_version: {driver_version} url: {url}')
            raise DriverVersionInvalidException(message)
        
    def _custom_bar(self, current, total, width=80):
        return wget.bar_adaptive(round(current/1024/1024, 2), round(total/1024/1024, 2), width) + ' MB' + " "
    
    def _wget_download_driver(self, url, path):
        bar = self._custom_bar if self.info_messages else None

        archive_path = wget.download(url=url, out=path, bar=bar)
        return archive_path
