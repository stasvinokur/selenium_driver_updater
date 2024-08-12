#Standart library imports
import time
import re
from pathlib import Path

# Local imports

from selenium_driver_updater.util.logger import logger

from selenium_driver_updater.browsers._firefoxBrowser import FirefoxBrowser

from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

from selenium_driver_updater.driver_base import DriverBase

class GeckoDriver(DriverBase):
    """Class for working with Selenium geckodriver binary"""

    _repo_name = 'mozilla/geckodriver'

    def __init__(self, **kwargs):

        kwargs.update(repo_name=GeckoDriver._repo_name)

        DriverBase.__init__(self, **kwargs)

        self.system_name = ''

        #assign of specific os
        specific_system = str(kwargs.get('system_name', ''))
        specific_system = specific_system.replace('mac64_m1', 'macos-aarch64').replace('mac64', 'macos')
        if specific_system:
            if 'win' in specific_system:
                self.system_name = "geckodriver-v{}-" + f"{specific_system}.zip"
            else:
                self.system_name = "geckodriver-v{}-" + f"{specific_system}.tar.gz"

        self.geckodriver_path = self.driver_path

        kwargs.update(path=self.geckodriver_path)
        self.firefoxbrowser = FirefoxBrowser(**kwargs)

    def main(self) -> str:
        """Main function, checks for the latest version, downloads or updates geckodriver binary or
        downloads specific version of geckodriver.

        Returns:
            str

            driver_path (str) : Path where geckodriver was downloaded or updated.

        """
        driver_path : str = ''

        self.firefoxbrowser.main()

        if not self.version:

            driver_path = self.__check_if_geckodriver_is_up_to_date()

        else:

            driver_path = self._download_driver(version=self.version)

        return driver_path

    def __check_if_geckodriver_is_up_to_date(self) -> str:
        """Main function, checks for the latest version, downloads or updates geckodriver binary

        Returns:
            str

            driver_path (str)       : Path where geckodriver was downloaded or updated.

        """
        driver_path : str = ''

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version_github()

            if is_driver_up_to_date:
                return self.geckodriver_path

        driver_path = self._download_driver()

        if not self.system_name:

            is_driver_up_to_date, current_version, latest_version = super()._compare_current_version_and_latest_version_github()

            if not is_driver_up_to_date:
                message = ('Problem with updating geckodriver'
                        f'current_version: {current_version} latest_version: {latest_version}')
                logger.error(message)
                message = 'Trying to download previous latest version of geckodriver'
                logger.info(message)

                driver_path = self._download_driver(previous_version=True)

        return driver_path

    def _get_latest_previous_version_geckodriver_via_requests(self) -> str:
        """Gets previous latest geckodriver version


        Returns:
            str

            latest_version_previous (str)   : Latest previous version of geckodriver.

        """

        latest_previous_version : str = ''

        repo_name = GeckoDriver._repo_name
        latest_previous_version = self.github_viewer.get_release_version_by_repo_name(repo_name=repo_name, index=1)

        logger.info(f'Latest previous version of geckodriver: {latest_previous_version}')

        return latest_previous_version

    def _check_if_version_is_valid(self, url : str) -> None:
        """Checks the specified version for existence.

        Args:
            url (str)           : Full download url of geckodriver.

        """
        archive_name : str = url.split("/")[len(url.split("/"))-1]
        is_found : bool = False
        find_string = re.findall(self.setting["Program"]["wedriverVersionPattern"], url)
        driver_version = find_string[0] if len(find_string) > 0 else ''

        json_data = self.github_viewer.get_all_releases_data_by_repo_name(GeckoDriver._repo_name)

        for data in json_data:
            if data.get('name') == driver_version:
                for asset in data.get('assets'):
                    if asset.get('name') == archive_name:
                        is_found = True
                        break
                break

        if not is_found:
            message = f'Wrong version or system_name was specified. driver_version: {driver_version} url: {url}'
            raise DriverVersionInvalidException(message)

    def _download_driver(self, version : str = '', previous_version : bool = False) -> str:
        """Function to download, delete or upgrade current geckodriver

        Args:
            version (str)               : Specific geckodriver version to download. Defaults to empty string.
            previous_version (boll)     : If true, geckodriver latest previous version will be downloaded. Defaults to False.

        Returns:
            str

            driver_path (str)       : Path to unzipped driver.

        """

        url : str = ''
        latest_version : str = ''
        latest_previous_version : str = ''

        driver_path : str = ''

        super()._delete_current_driver_for_current_os()

        if version:

            url = self.setting["GeckoDriver"]["LinkLastReleasePlatform"].format(version, version)
            logger.info(f'Started download geckodriver specific_version: {version}')

        elif previous_version:

            latest_previous_version = self._get_latest_previous_version_geckodriver_via_requests()

            url = self.setting["GeckoDriver"]["LinkLastReleasePlatform"].format(latest_previous_version, latest_previous_version)
            logger.info(f'Started download geckodriver latest_previous_version: {latest_previous_version}')

        else:

            latest_version = super()._get_latest_version_driver_github()

            url = self.setting["GeckoDriver"]["LinkLastReleasePlatform"].format(latest_version, latest_version)
            logger.info(f'Started download geckodriver latest_version: {latest_version}')

        if self.system_name:
            url = url.replace(url.split("/")[-1], '')
            version = [value for key,value in locals().items() if 'version' in key and value][0]
            url = url + self.system_name.format(version)

            logger.info(f'Started downloading geckodriver for specific system: {self.system_name}')

        if any([version, self.system_name ,latest_previous_version]):
            self._check_if_version_is_valid(url=url)

        archive_name = url.split("/")[-1]
        out_path = self.path + archive_name

        if Path(out_path).exists():
            Path(out_path).unlink()

        logger.info(f'Started download geckodriver by url: {url}')
        archive_path = super()._wget_download_driver(url, out_path)
        time.sleep(2)

        logger.info(f'Geckodriver was downloaded to path: {archive_path}')

        out_path = self.path

        parameters = dict(archive_path=archive_path, out_path=out_path)

        if not self.filename:

            self.extractor.extract_and_detect_archive_format(**parameters)

        else:
            filename = self.setting['GeckoDriver']['LastReleasePlatform']
            parameters.update(dict(filename=filename, filename_replace=self.filename))

            self.extractor.extract_all_zip_archive_with_specific_name(**parameters)

        if Path(archive_path).exists():
            Path(archive_path).unlink()

        driver_path = self.geckodriver_path

        logger.info(f'Geckodriver was successfully unpacked by path: {driver_path}')

        super()._chmod_driver()

        return driver_path
        