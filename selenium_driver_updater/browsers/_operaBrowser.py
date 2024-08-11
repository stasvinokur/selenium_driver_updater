#pylint: disable=logging-fstring-interpolation
#Standart library imports
import subprocess
import os
import re
import platform
from typing import Tuple,Any
from pathlib import Path
import shutil

# Third party imports
from bs4 import BeautifulSoup
import wget

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException

# Local imports
from selenium_driver_updater._setting import setting

from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.extractor import Extractor
from selenium_driver_updater.util.logger import logger

class OperaBrowser():
    """Class for working with Opera browser"""

    def __init__(self, **kwargs):
        self.setting : Any = setting
        self.check_browser_is_up_to_date = bool(kwargs.get('check_browser_is_up_to_date'))

        self.operadriver_path = str(kwargs.get('path'))

        self.requests_getter = RequestsGetter
        self.extractor = Extractor
        self.system_name = ''
        self.url_release = ''

    def main(self) -> None:
        """Main function, checks for the latest version, downloads or updates opera browser"""

        if self.check_browser_is_up_to_date:
            self._check_if_opera_browser_is_up_to_date()

    def _check_if_opera_browser_is_up_to_date(self) -> None:
        """Сhecks for the latest version of opera browser

        Raises:
            Except: If unexpected error raised.

        """

        try:

            if platform.system() not in ['Darwin', 'Windows']:
                message = 'Opera browser checking/updating is currently disabled for your OS. Please wait for the new releases.'
                logger.error(message)
                return

            is_browser_up_to_date, current_version, latest_version = self._compare_current_version_and_latest_version_opera_browser()

            if not is_browser_up_to_date:

                self._get_latest_opera_browser_for_current_os()

                is_browser_up_to_date, current_version, latest_version = self._compare_current_version_and_latest_version_opera_browser()

                if not is_browser_up_to_date:
                    message = f'Problem with updating opera browser current_version: {current_version} latest_version: {latest_version}'
                    logger.info(message)

        except (ValueError, FileNotFoundError):
            pass

    def _get_current_version_opera_browser_selenium(self) -> str:
        """Gets current opera browser version


        Returns:
            str

            browser_version (str)   : Current opera browser version.

        Raises:
            SessionNotCreatedException: Occurs when current operadriver could not start.

            WebDriverException: Occurs when current operadriver could not start or critical error occured.

        """

        browser_version : str = ''

        try:

            browser_version = self._get_current_version_opera_browser_selenium_via_terminal()
            if not browser_version:
                message = 'Trying to get current version of opera browser via operadriver'
                logger.info(message)

            if Path(self.operadriver_path).exists() and not browser_version:

                with webdriver.Opera(executable_path = self.operadriver_path) as driver:
                    browser_version = driver.execute_script("return navigator.userAgent")

                find_string = re.findall('OPR/' + self.setting["Program"]["wedriverVersionPattern"], browser_version)
                browser_version = find_string[0] if len(find_string) > 0 else ''

            logger.info(f'Current version of opera browser: {browser_version}')

        except (WebDriverException, SessionNotCreatedException, OSError):
            pass #[Errno 86] Bad CPU type in executable:

        return browser_version

    def _get_latest_version_opera_browser(self) -> str:
        """Gets latest opera browser version


        Returns:
            str

            latest_version (str)    : Latest version of opera browser.

        Raises:
            Except: If unexpected error raised.

        """

        latest_version : str = ''
        version : str = ''

        url = self.setting["OperaBrowser"]["LinkAllLatestRelease"]
        json_data = self.requests_getter.get_result_by_request(url=url)

        soup = BeautifulSoup(json_data, 'html.parser')

        system_name = platform.system()
        system_name = system_name.replace('Darwin', 'mac')
        system_name = system_name.replace('Windows', 'win')
        self.system_name = system_name.lower() + '/' #mac -> mac/ or Linux -> linux/

        elements = soup.findAll('a')
        for i,_ in enumerate(elements, 1):
            version = elements[-i].attrs.get('href')
            self.url_release = url + version

            json_data = self.requests_getter.get_result_by_request(url=self.url_release)

            if self.system_name not in json_data:
                continue

            else:
                break

        latest_version = version.replace('/', '')

        logger.info(f'Latest version of opera browser: {latest_version}')

        return latest_version

    def _get_latest_opera_browser_for_current_os(self) -> None:
        """Trying to update opera browser to its latest version"""

        if platform.system() not in ['Darwin', 'Windows']:
            message = 'Opera browser checking/updating is currently disabled for your OS. Please wait for the new releases.'
            logger.error(message)
            return

        latest_version = self._get_latest_version_opera_browser()

        url_full_release = self.url_release + self.system_name
        if platform.system() == 'Darwin':
            if 'arm' in str(os.uname().machine) and platform.system() == 'Darwin':

                url_full_release = url_full_release + f'Opera_{latest_version}_Autoupdate_arm64.tar.xz'

            else:
                url_full_release = url_full_release + f'Opera_{latest_version}_Autoupdate.tar.xz'

        elif platform.system() == 'Windows':
            if self.setting['Program']['OSBitness'] == '64':

                url_full_release = url_full_release + f'Opera_{latest_version}_Setup_x64.exe'

            else:

                url_full_release = url_full_release + f'Opera_{latest_version}_Setup.exe'

        logger.info(f'Started download operabrowser by url: {url_full_release}')

        path = self.operadriver_path.replace(self.operadriver_path.split(os.path.sep)[-1], '') + 'selenium-driver-updater' + os.path.sep
        archive_name = url_full_release.split('/')[-1]

        if not Path(path).exists():
            Path(path).mkdir()

        if Path(path + archive_name).exists():
            Path(path + archive_name).unlink()

        logger.info(f'Started to download opera browser by url: {url_full_release}')
        archive_path = wget.download(url=url_full_release, out=path + archive_name)

        logger.info(f'Opera browser was downloaded to path: {archive_path}')

        if platform.system() == 'Darwin':

            logger.info('Trying to kill all opera processes')
            subprocess.Popen('killall Opera', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.Popen('killall Opera', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info('Successfully killed all opera processes')

            self.extractor.extract_all_tar_xz_archive(archive_path=archive_path, delete_archive=True, out_path=path)

            opera_browser_path = path + 'Opera.app'
            opera_browser_path_application = '/Applications/Opera.app'

            if Path(opera_browser_path_application).exists():
                shutil.rmtree(opera_browser_path_application)
            shutil.move(opera_browser_path, opera_browser_path_application)

            logger.info(f'Successfully moved opera browser from: {opera_browser_path} to: {opera_browser_path_application}')

            if Path(archive_path).exists():
                Path(archive_path).unlink()

        elif platform.system() == 'Windows':

            logger.info('Trying to kill all opera.exe processes')
            subprocess.Popen('taskkill /F /IM "opera.exe" /T', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logger.info('Successfully killed all opera.exe processes')

            logger.info('Trying to install new opera browser')
            os.system(f'{archive_path} /install /silent /launchopera=no /desktopshortcut=no /pintotaskbar=no /setdefaultbrowser=0')
            logger.info('Successfully updated current opera browser')

    def _compare_current_version_and_latest_version_opera_browser(self) -> Tuple[bool, str, str]:
        """Compares current version of opera browser to latest version

        Returns:
            Tuple of bool, str and str

            is_browser_up_to_date (bool)    : It true the browser is up to date. Defaults to False.
            current_version (str)           : Current version of the browser.
            latest_version (str)            : Latest version of the browser.

        Raises:
            Except: If unexpected error raised.

        """

        is_browser_up_to_date : bool = False
        current_version : str = ''
        latest_version : str = ''

        current_version = self._get_current_version_opera_browser_selenium()

        if not current_version:
            return is_browser_up_to_date, current_version, latest_version

        latest_version = self._get_latest_version_opera_browser()

        if current_version == latest_version:
            is_browser_up_to_date = True
            message = f"Your existing opera browser is up to date. current_version: {current_version} latest_version: {latest_version}"
            logger.info(message)

        return is_browser_up_to_date, current_version, latest_version

    def _get_current_version_opera_browser_selenium_via_terminal(self) -> str:
        """Gets current opera browser version via command in terminal


        Returns:
            str

            browser_version (str)   : Current opera browser version.

        Raises:

            Except: If unexpected error raised.

        """

        browser_version : str = ''
        browser_version_terminal : str = ''

        operabrowser_path = self.setting["OperaBrowser"]["Path"]
        if operabrowser_path:

            logger.info('Trying to get current version of opera browser via terminal')

            if platform.system() == 'Windows':

                with subprocess.Popen(operabrowser_path, stdout=subprocess.PIPE) as process:
                    browser_version_terminal = process.communicate()[0].decode('UTF-8')

                find_string_terminal = re.findall("Opera.*", browser_version_terminal)

                browser_version_terminal = find_string_terminal[0] if len(find_string_terminal) > 0 else ''

            elif platform.system() == 'Darwin':

                with subprocess.Popen([operabrowser_path, '--version'], stdout=subprocess.PIPE) as process:
                    browser_version_terminal = process.communicate()[0].decode('UTF-8')

            find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], browser_version_terminal)
            browser_version = find_string[0] if len(find_string) > 0 else ''

        return browser_version
