#Standart library imports
import subprocess
import re
from typing import Any
from pathlib import Path
import platform

# Selenium imports
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Local imports
from selenium_driver_updater._setting import setting

from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.logger import logger

class EdgeBrowser():
    """Class for working with Edge browser"""

    def __init__(self, **kwargs):
        self.setting : Any = setting
        self.check_browser = bool(kwargs.get('check_browser'))

        self.edgedriver_path = str(kwargs.get('path'))

        self.requests_getter = RequestsGetter

    def main(self):
        """Main function, checks for the latest version, downloads or updates edge browser"""

        if self.check_browser:
            self._compare_edge_browser_versions()

    def _get_current_version_edge_browser_selenium(self) -> str:
        """Gets current edge browser version


        Returns:
            str

            browser_version (str)   : Current edge browser version.

        Raises:
            SessionNotCreatedException: Occurs when current edgedriver could not start.

            WebDriverException: Occurs when current edgedriver could not start or critical error occured.

        """

        browser_version : str = ''

        try:

            browser_version = self._get_current_version_edge_browser_selenium_via_terminal()
            if not browser_version:
                message = 'Trying to get current version of edge browser via edgedriver'
                logger.info(message)

            if Path(self.edgedriver_path).exists() and not browser_version:

                service = Service(self.edgedriver_path)

                options = Options()

                with webdriver.Edge(service=service, options=options) as driver:
                    browser_version = str(driver.capabilities['browserVersion'])

            logger.info(f'Current version of edge browser: {browser_version}')

        except (WebDriverException, SessionNotCreatedException, OSError):
            pass #[Errno 86] Bad CPU type in executable:

        return browser_version

    def _get_latest_version_edge_browser(self) -> str:
        """Gets latest edge browser version

        Returns:
            str

            latest_version (str)    : Latest version of edge browser.

        """

        latest_version : str = ''

        url = self.setting['EdgeDriver']["LinkLastRelease"]
        json_data = self.requests_getter.get_result_by_request(url=url)

        latest_version = str(json_data).strip()

        logger.info(f'Latest version of edge browser: {latest_version}')

        return latest_version

    def _compare_edge_browser_versions(self):
        """Compares current version of edge browser to latest version"""

        current_version : str = ''
        latest_version : str = ''

        current_version = self._get_current_version_edge_browser_selenium()

        if not current_version:
            return

        latest_version = self._get_latest_version_edge_browser()

        if current_version == latest_version:
            message = f"Your existing edge browser is up to date. current_version: {current_version} latest_version: {latest_version}"
            logger.info(message)
        else:
            message = f"Your existing edge browser is outdated. current_version: {current_version} latest_version: {latest_version}"
            logger.warning(message)

    def _get_current_version_edge_browser_selenium_via_terminal(self) -> str:
        """Gets current edge browser version via command in terminal

        Returns:
            str

            browser_version (str)   : Current edge browser version.

        """

        browser_version : str = ''
        browser_version_terminal : str = ''

        edgebrowser_path = self.setting["EdgeBrowser"]["Path"]
        if edgebrowser_path:

            logger.info('Trying to get current version of edge browser via terminal')


            if platform.system() == 'Darwin':

                with subprocess.Popen([edgebrowser_path, '--version'], stdout=subprocess.PIPE) as process:
                    browser_version_terminal = process.communicate()[0].decode('UTF-8')

            elif platform.system() == 'Windows':

                with subprocess.Popen(edgebrowser_path, stdout=subprocess.PIPE) as process:
                    browser_version_terminal = process.communicate()[0].decode('UTF-8')

            find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], browser_version_terminal)
            browser_version = find_string[0] if len(find_string) > 0 else ''

        return browser_version
