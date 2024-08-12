#Standart library imports
import time
from pathlib import Path
from packaging import version


# Local imports

from selenium_driver_updater.browsers._edgeBrowser import EdgeBrowser

from selenium_driver_updater.util.logger import logger

from selenium_driver_updater.driver_base import DriverBase

class EdgeDriver(DriverBase):
    """Class for working with Selenium edgedriver binary"""

    _tmp_folder_path = 'tmp'

    def __init__(self, **kwargs):

        DriverBase.__init__(self, **kwargs)

        self.system_name = ''

        #assign of specific os
        specific_system = str(kwargs.get('system_name', ''))
        if specific_system:
            self.system_name = f"edgedriver_{specific_system}.zip"

        self.edgedriver_path = self.driver_path
        kwargs.update(path=self.edgedriver_path)
        self.edgebrowser = EdgeBrowser(**kwargs)

    def main(self) -> str:
        """Main function, checks for the latest version, downloads or updates edgedriver binary

        Returns:
            str

            driver_path (str)       : Path where edgedriver was downloaded or updated.

        """

        driver_path : str = ''
        self.edgebrowser.main()

        if not self.version:

            driver_path = self.__check_if_edgedriver_is_up_to_date()

        else:

            driver_path = self._download_driver(version=self.version)

        return driver_path

    def __check_if_edgedriver_is_up_to_date(self) -> str:
        """Checks for the latest version, downloads or updates edgedriver binary

        Returns:
            str

            driver_path (str)       : Path where edgedriver was downloaded or updated.

        """
        driver_path : str = ''

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version()

            if is_driver_up_to_date:
                return self.edgedriver_path

        driver_path = self._download_driver()

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version()

            if not is_driver_up_to_date:
                message = ('Problem with updating edgedriver'
                            f'current_version: {current_version} latest_version: {latest_version}')
                logger.error(message)

                message = 'Trying to download previous latest version of edgedriver'
                logger.info(message)

                driver_path = self._download_driver(previous_version=True)

        return driver_path

    def _get_latest_previous_version_edgedriver_via_requests(self) -> str:
        """Gets previous latest edgedriver version


        Returns:
            str

            latest_version_previous (str)   : Latest previous version of edgedriver.

        """

        latest_previous_version : str = ''

        latest_version = super()._get_latest_version_driver()

        latest_version_main = version.parse(latest_version).major
        latest_previous_version_main = str(latest_version_main-1)

        if 'arm64' in self.setting["EdgeDriver"]["LinkLastReleaseFile"] or 'win' in  self.setting["EdgeDriver"]["LinkLastReleaseFile"]:
            platform_url = 'WINDOWS'
        elif 'mac64' in self.setting["EdgeDriver"]["LinkLastReleaseFile"]:
            platform_url = 'MACOS'
        else:
            platform_url = 'LINUX'

        url = self.setting["EdgeDriver"]["LinkLatestReleaseSpecificVersion"].format(latest_previous_version_main, platform_url)
        json_data = self.requests_getter.get_result_by_request(url=url)
        latest_previous_version = json_data.strip()
        logger.info(f'Latest previous version of edgedriver: {latest_previous_version}')

        return latest_previous_version

    def _download_driver(self, version : str = '', previous_version : bool = False) -> str:
        """Function to download, delete or upgrade current chromedriver

        Args:
            version (str)               : Specific chromedriver version to download. Defaults to empty string.
            previous_version (boll)     : If true, chromedriver latest previous version will be downloaded. Defaults to False.

        Returns:
            str

            file_name (str)         : Path to unzipped driver.

        """

        url : str = ''
        latest_previous_version : str = ''
        latest_version : str = ''

        driver_path : str = ''

        super()._delete_current_driver_for_current_os()

        if version:

            url = str(self.setting["EdgeDriver"]["LinkLastReleaseFile"]).format(version)
            logger.info(f'Started download edgedriver specific_version: {version}')

        elif previous_version:

            latest_previous_version = self._get_latest_previous_version_edgedriver_via_requests()

            url = str(self.setting["EdgeDriver"]["LinkLastReleaseFile"]).format(latest_previous_version)
            logger.info(f'Started download edgedriver latest_previous_version: {latest_previous_version}')

        else:

            latest_version = super()._get_latest_version_driver()

            url = str(self.setting["EdgeDriver"]["LinkLastReleaseFile"]).format(latest_version)
            logger.info(f'Started download edgedriver latest_version: {latest_version}')

        if self.system_name:
            url = url.replace(url.split("/")[-1], '')
            url = url + self.system_name

            logger.info(f'Started downloading edgedriver for specific system: {self.system_name}')

        if any([version, self.system_name ,latest_previous_version]):
            if 'mac64_m1' in url:
                try:
                    super()._check_if_version_is_valid(url=url)
                except Exception:
                    logger.warning('Could not find binary with mac64_m1 name, trying to download standart mac binary')
                    url = url.replace('mac64_m1', 'mac64')
                    super()._check_if_version_is_valid(url=url)
            else:
                super()._check_if_version_is_valid(url=url)

        archive_name = url.split("/")[-1]
        out_path = self.path + archive_name

        if Path(out_path).exists():
            Path(out_path).unlink()

        logger.info(f'Started download edgedriver by url: {url}')
        archive_path = super()._wget_download_driver(url, out_path)
        time.sleep(2)

        logger.info(f'Edgedriver was downloaded to path: {archive_path}')

        out_path = self.path

        parameters = dict(archive_path=archive_path, out_path=out_path)

        if not self.filename:

            self.extractor.extract_and_detect_archive_format(**parameters)

        else:


            filename = str(self.setting['EdgeDriver']['LastReleasePlatform'])
            parameters.update(dict(filename=filename, filename_replace=self.filename))

            self.extractor.extract_all_zip_archive_with_specific_name(**parameters)

        if Path(archive_path).exists():
            Path(archive_path).unlink()

        driver_path = self.edgedriver_path

        logger.info(f'Edgedriver was successfully unpacked by path: {driver_path}')

        super()._chmod_driver()

        return driver_path
        