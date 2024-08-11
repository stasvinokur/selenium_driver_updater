#pylint: disable=logging-fstring-interpolation
#Standart library imports
import subprocess
import os
import re
import platform
from typing import Tuple, Any
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

from selenium_driver_updater.util.extractor import Extractor
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.logger import logger

class ChromeBrowser():
    """Class for working with Chrome browser"""

    def __init__(self, **kwargs):
        self.setting : Any = setting
        self.check_browser_is_up_to_date = bool(kwargs.get('check_browser_is_up_to_date'))

        self.chromedriver_path = str(kwargs.get('path'))
        self.extractor = Extractor
        self.requests_getter = RequestsGetter

    def main(self) -> None:
        """Main function, checks for the latest version, downloads or updates chrome browser"""

        if self.check_browser_is_up_to_date:
            self._check_if_chrome_browser_is_up_to_date()

    def _check_if_chrome_browser_is_up_to_date(self) -> None:
        """Сhecks for the latest version of chrome browser"""

        try:

            if platform.system() not in ['Darwin']:
                message = 'Chrome browser checking/updating is currently disabled for your OS. Please wait for the new releases.'
                logger.error(message)
                return

            is_browser_up_to_date, current_version, latest_version = self._compare_current_version_and_latest_version_chrome_browser()

            if not is_browser_up_to_date:

                self._get_latest_chrome_browser_for_current_os()

                is_browser_up_to_date, current_version, latest_version = self._compare_current_version_and_latest_version_chrome_browser()

                if not is_browser_up_to_date:
                    message = f'Problem with updating chrome browser current_version: {current_version} latest_version: {latest_version}'
                    logger.info(message)

        except (ValueError, FileNotFoundError):
            pass

    def _compare_current_version_and_latest_version_chrome_browser(self) -> Tuple[bool, str, str]:
        """Compares current version of chrome browser to latest version

        Returns:
            Tuple of bool, str and str

            is_browser_up_to_date (bool)    : It true the browser is up to date. Defaults to False.
            current_version (str)           : Current version of the browser.
            latest_version (str)            : Latest version of the browser.

        """
        is_browser_up_to_date : bool = False
        current_version : str = ''
        latest_version : str = ''

        current_version = self._get_current_version_chrome_browser_selenium()

        if not current_version:
            return is_browser_up_to_date, current_version, latest_version

        latest_version = self._get_latest_version_chrome_browser()

        if current_version == latest_version:
            is_browser_up_to_date = True
            message = f"Your existing chrome browser is up to date. current_version: {current_version} latest_version: {latest_version}"
            logger.info(message)

        return is_browser_up_to_date, current_version, latest_version

    def _get_current_version_chrome_browser_selenium(self) -> str:
        """Gets current chrome browser version


        Returns:
            str

            browser_version (str)   : Current chrome browser version.

        Raises:
            SessionNotCreatedException: Occurs when current chromedriver could not start.

            WebDriverException: Occurs when current chromedriver could not start or critical error occured.

            Except: If unexpected error raised.

        """

        browser_version : str = ''

        try:

            browser_version = self._get_current_version_chrome_browser_selenium_via_terminal()
            if not browser_version:
                message = 'Trying to get current version of chrome browser via chromedriver'
                logger.info(message)

            if Path(self.chromedriver_path).exists() and not browser_version:

                chrome_options = webdriver.ChromeOptions()

                chrome_options.add_argument('--headless')

                with webdriver.Chrome(executable_path = self.chromedriver_path, options = chrome_options) as driver:
                    browser_version = str(driver.capabilities['browserVersion'])

            logger.info(f'Current version of chrome browser: {browser_version}')

        except (WebDriverException, SessionNotCreatedException, OSError):
            pass #[Errno 86] Bad CPU type in executable:

        return browser_version

    def _get_current_version_chrome_browser_selenium_via_terminal(self) -> str:
        """Gets current chrome browser version via command in terminal


        Returns:
            str

            browser_version (str)   : Current chrome browser version.

        """

        browser_version : str = ''
        browser_version_terminal : str = ''

        chromebrowser_path = self.setting["ChromeBrowser"]["Path"]
        if chromebrowser_path:

            logger.info('Trying to get current version of chrome browser via terminal')

            if platform.system() == 'Windows':

                for command in chromebrowser_path:

                    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
                        browser_version_terminal = process.communicate()[0].decode('UTF-8')

                    if 'invalid' not in browser_version_terminal.lower():
                        break

            elif platform.system() == 'Linux':

                with subprocess.Popen([chromebrowser_path, '--version'], stdout=subprocess.PIPE) as process:
                    browser_version_terminal = process.communicate()[0].decode('UTF-8')

            elif platform.system() == 'Darwin':

                for path in chromebrowser_path:

                    with subprocess.Popen([path, '--version'], stdout=subprocess.PIPE) as process:
                        browser_version_terminal = process.communicate()[0].decode('UTF-8')

                    if 'no such file or directory' not in browser_version_terminal.lower():
                        break


            find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], browser_version_terminal)
            browser_version = find_string[0] if len(find_string) > 0 else ''

        return browser_version

    def _get_latest_version_chrome_browser(self, no_messages : bool = False) -> str:
        """Gets latest chrome browser version


        Returns:
            str

            latest_version (str)    : Latest version of chrome browser.

        """

        latest_version : str = ''
        latest_stable_version_element : Any = ''

        url = self.setting["ChromeBrowser"]["LinkAllLatestRelease"]
        json_data = self.requests_getter.get_result_by_request(url=url)

        soup = BeautifulSoup(json_data, 'html.parser')
        elements_news = soup.findAll('div', attrs={'class' : 'post'})
        stable_channel_header_text = 'Stable Channel Update for Desktop'

        for news in elements_news:
            if stable_channel_header_text in news.text:

                current_os = platform.system().replace('Darwin', 'Mac')
                if current_os.lower() not in news.text.lower():
                    continue

                latest_stable_version_element = news.text
                break

        if not latest_stable_version_element:
            message = f'Could not determine latest stable channel post of Chrome Browser. Maybe the text "{stable_channel_header_text}" is changed'
            logger.error(message)

            message = 'Trying to determine latest stable channel post of Chrome Browser without OS detection'
            logger.info(message)

            latest_stable_version_element = [news.text for news in elements_news if stable_channel_header_text in news.text][0]
            if not latest_stable_version_element:
                return latest_version

        latest_version = re.findall(self.setting["Program"]["wedriverVersionPattern"], latest_stable_version_element)[0]

        if not no_messages:

            logger.info(f'Latest version of chrome browser: {latest_version}')

        return latest_version

    def _get_latest_chrome_browser_for_current_os(self) -> None:
        """Trying to update chrome browser to its latest version"""

        if platform.system() not in ['Darwin']:
            message = 'Chrome browser checking/updating is currently disabled for your OS. Please wait for the new releases.'
            logger.error(message)
            return

        url_release = self.setting["ChromeBrowser"]["LinkAllLatestReleaseFile"]
        path = self.chromedriver_path.replace(self.chromedriver_path.split(os.path.sep)[-1], '') + 'selenium-driver-updater' + os.path.sep
        archive_name = url_release.split('/')[-1]

        if not Path(path).exists():
            Path(path).mkdir()

        if Path(path + archive_name).exists():
            Path(path + archive_name).unlink()

        logger.info(f'Started to download chrome browser by url: {url_release}')
        archive_path = wget.download(url=url_release, out=path + archive_name)

        logger.info(f'Chrome browser was downloaded to path: {archive_path}')

        if platform.system() == 'Darwin':

            volume_path:str = ''

            try:
                
                logger.info('Trying to kill all chrome processes')
                subprocess.Popen(r'killall Google\ Chrome', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                logger.info('Successfully killed all chrome processes')

                logger.info(f'Trying to attach image: {archive_path}')
                with subprocess.Popen(['hdiutil', 'attach', archive_path], stdout=subprocess.PIPE) as process:
                    info = process.communicate()[0].decode('UTF-8')

                volume_path = re.findall('Volumes.*', info)[0]
                volume_path = f"/{volume_path}/"

                chrome_browser_path = volume_path + 'Google Chrome.app'

                logger.info(f'Successfully attached {archive_name} at path: {volume_path}')

                chrome_browser_path_application = '/Applications/Google Chrome.app'

                try:
                    if Path(chrome_browser_path_application).exists():
                        shutil.rmtree(chrome_browser_path_application)
                except PermissionError:
                    logger.error(f'Cannot delete chromebrowser at path: {chrome_browser_path_application} abort operation')
                    return

                logger.info(f'Trying to move chrome browser from: {chrome_browser_path} to: {chrome_browser_path_application}')

                os.system(f'rsync -a "{volume_path}Google Chrome.app" /Applications/')

                logger.info(f'Successfully moved chrome browser from: {chrome_browser_path} to: {chrome_browser_path_application}')

            finally:

                with subprocess.Popen(['hdiutil', 'eject', volume_path], stdout=subprocess.PIPE) as process:
                    info = process.communicate()[0].decode('UTF-8')

                logger.info(f'Successfully ejected {archive_name} at path: {volume_path}')

                if Path(archive_path).exists():
                    Path(archive_path).unlink()
