#Standart library imports
import time
from pathlib import Path
from typing import Tuple
from packaging import version

# Local imports
from selenium_driver_updater.browsers._chromeBrowser import ChromeBrowser

from selenium_driver_updater.util.logger import logger
from selenium_driver_updater.driver_base import DriverBase

from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

class ChromeDriver(DriverBase):
    """Class for working with Selenium chromedriver binary"""

    _tmp_folder_path = 'tmp'

    def __init__(self, **kwargs):

        DriverBase.__init__(self, **kwargs)

        self.system_name = ''

        #assign of specific os
        specific_system = str(kwargs.get('system_name', ''))
        specific_system = specific_system.replace('linux32', 'linux64')
        specific_system = specific_system.replace('mac64_m1', 'mac-arm64')
        specific_system = specific_system.replace('mac64', 'mac-x64')
        if specific_system:
            self.system_name = f"chromedriver-{specific_system}.zip"
            self.specific_system = specific_system

        self.chromedriver_path = self.driver_path

        kwargs.update(path=self.chromedriver_path)
        self.chromebrowser = ChromeBrowser(**kwargs)

    def main(self) -> str:
        """Main function, checks for the latest version, downloads or updates chromedriver binary or
        downloads specific version of chromedriver.

        Returns:
            str

            driver_path (str) : Path where chromedriver was downloaded or updated.

        """
        driver_path : str = ''

        self.chromebrowser.main()

        if not self.version:

            #additional checking for main versions to equal - for example, chromedriver version main is 90 and chrome browser is still 89
            is_equal, latest_version_driver, latest_version_browser = self._compare_latest_version_main_chromedriver_and_latest_version_main_chrome_browser()

            if is_equal:

                driver_path = self._check_if_chromedriver_is_up_to_date()

            if not is_equal:

                message = (f' Problem with chromedriver latest_version_driver:'
                    f'{latest_version_driver} latest_version_browser: {latest_version_browser}\n'
                    ' It often happen when new version of chromedriver released, but new version of chrome browser is not\n'
                    ' Trying to download the latest previous version of chromedriver')
                logger.error(message)

                driver_path = self._download_driver(previous_version=True)

        else:

            driver_path = self._download_driver(version=self.version)

        return driver_path
    
    def _get_latest_version_driver(self, no_messages: bool = False) -> str:
        """Gets the latest driver version based on the specified channel.

        Returns:
            str: Latest version of the specific driver.
        """

        latest_version: str = ''

        channel_suffix = self.version.split('_')[1] if '_' in self.version else 'stable'

        channel = channel_suffix.capitalize()  # 'Beta', 'Dev', 'Canary'

        url = self.setting["ChromeDriver"]["LinkLastRelease"]

        json_data = self.requests_getter.get_result_by_request(url=url, is_json=True)

        latest_version = json_data.get('channels', {}).get(channel, {}).get('version', '')

        if not no_messages:
            logger.info(f'Latest version of chromedriver {self.version}: {latest_version}')

        return latest_version

    def _compare_latest_version_main_chromedriver_and_latest_version_main_chrome_browser(self) -> Tuple[bool, str, str]:
        """Compares latest main version of chromedriver and latest main version of chrome browser"""
        is_equal : bool = False

        latest_version_chromedriver = self._get_latest_version_driver(no_messages=True)

        latest_version_browser = self.chromebrowser._get_latest_version_chrome_browser(no_messages=True)

        if version.parse(latest_version_chromedriver).major <= version.parse(latest_version_browser).major:
            is_equal = True

        return is_equal, latest_version_chromedriver, latest_version_browser

    def _check_if_chromedriver_is_up_to_date(self) -> str:
        """Сhecks for the latest version, downloads or updates chromedriver binary

        Returns:
            str

            driver_path (str) : Path where chromedriver was downloaded or updated.

        """
        driver_path : str = ''

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version()

            if is_driver_up_to_date:
                return self.chromedriver_path

        driver_path = self._download_driver()

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version()

            if not is_driver_up_to_date:

                message = (f'Problem with updating chromedriver'
                        f'current_version: {current_version} latest_version: {latest_version}')
                logger.error(message)
                message = 'Trying to download previous latest version of chromedriver'
                logger.info(message)

                driver_path = self._download_driver(previous_version=True)

        return driver_path

    def _get_latest_previous_version_chromedriver_via_requests(self) -> str:
        """Gets previous latest chromedriver version


        Returns:
            str

            latest_version_previous (str)   : Latest previous version of chromedriver.

        """

        latest_version_previous : str = ''

        latest_version = self._get_latest_version_driver()
        latest_version_main = version.parse(latest_version).major

        latest_version_main_previous = int(latest_version_main) - 1

        url = self.setting["ChromeDriver"]["LinkLatestReleaseSpecificVersion"].format(latest_version_main_previous)
        json_data = self.requests_getter.get_result_by_request(url=url)

        latest_version_previous = str(json_data)

        logger.info(f'Latest previous version of chromedriver: {latest_version_previous}')

        return latest_version_previous

    def _download_driver(self, version : str = '', previous_version : bool = False) -> str:
        """Function to download, delete or upgrade current chromedriver

        Args:
            version (str)               : Specific chromedriver version to download. Defaults to empty string.
            previous_version (boll)     : If true, chromedriver latest previous version will be downloaded. Defaults to False.

        Returns:
            str

            driver_path (str) : Path to unzipped driver.

        """

        url : str = ''
        latest_previous_version : str = ''
        latest_version : str = ''
        driver_path : str = ''

        super()._delete_current_driver_for_current_os()

        if previous_version:

            latest_previous_version = self._get_latest_previous_version_chromedriver_via_requests()

            url = self.setting["ChromeDriver"]["LinkLastReleaseFile"].format(latest_previous_version)
            logger.info(f'Started download chromedriver latest_previous_version: {latest_previous_version}')

        else:

            latest_version = self._get_latest_version_driver()

            url = self.setting["ChromeDriver"]["LinkLastReleaseFile"].format(latest_version)
            channel = 'stable' if '_' not in self.version else self.version.split('_')[1]
            logger.info(f'Started download chromedriver {channel} latest_version: {latest_version}')

        if self.system_name:
            url = url.replace(url.split("/")[-1], self.system_name)
            url = url.replace(url.split("/")[-2], self.specific_system)
            
            logger.info(f'Started downloading chromedriver for specific system: {self.system_name}')

        if any([version, self.system_name ,latest_previous_version]):
            super()._check_if_version_is_valid(url=url)

        archive_name = url.split("/")[-1]
        out_path = self.path + archive_name

        if Path(out_path).exists():
            Path(out_path).unlink()

        logger.info(f'Started download chromedriver by url: {url}')
        archive_path = super()._wget_download_driver(url, out_path)
        time.sleep(2)

        logger.info(f'\r\nChromedriver was downloaded to path: {archive_path}')

        out_path : str = self.path

        parameters = dict(archive_path=archive_path, out_path=out_path)

        if not self.filename:

            self.extractor.extract_and_detect_archive_format(**parameters)

        else:

            filename = self.setting['ChromeDriver']['LastReleasePlatform']
            parameters.update(dict(filename=filename, filename_replace=self.filename))

            self.extractor.extract_all_zip_archive_with_specific_name(**parameters)

        if Path(archive_path).exists():
            Path(archive_path).unlink()

        driver_path = self.chromedriver_path

        logger.info(f'Chromedriver was successfully unpacked by path: {driver_path}')

        super()._chmod_driver()

        return driver_path
