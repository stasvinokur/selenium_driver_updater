#Standart library imports
import platform

#Third library imports
from bs4 import BeautifulSoup

# Local imports
from selenium_driver_updater.util.logger import logger

from selenium_driver_updater.driver_base import DriverBase

class SafariDriver(DriverBase):
    "Class for working with Selenium safaridriver binary"

    def __init__(self, **kwargs):

        kwargs.update(path='/usr/bin/')
        DriverBase.__init__(self, **kwargs)

    def main(self) -> str:
        """Main function, checks for the latest version of safaridriver.

        Returns:
            str

            driver_path (str) : Path where safaridriver is located.

        """
        if platform.system() != 'Darwin':
            message = 'safaridriver is only supported for MacOS only.'
            raise OSError(message)

        self._compare_current_version_and_latest_version_safaridriver()

        return self.driver_path

    def _compare_current_version_and_latest_version_safaridriver(self) -> None:
        """Compares current version of safaridriver to latest version"""

        current_version = super()._get_current_version_driver()

        latest_version = self._get_latest_version_safaridriver()

        if current_version == latest_version:
            message = ('Your existing safaridriver is up to date.'
                        f'current_version: {current_version} latest_version: {latest_version}')
            logger.info(message)

        else:
            message = (f'Your current version of safaridriver is not equal to latest verison. current_version: {current_version} latest_version: {latest_version}\n'
                        'Please update your browser.')
            logger.info(message)

    def _get_latest_version_safaridriver(self) -> str:
        """Gets latest safaridriver version


        Returns:
            str

            latest_version (str)    : Latest version of safaridriver.

        """

        latest_version : str = ''
        url = self.setting["SafariDriver"]["LinkLastRelease"]

        json_data = self.requests_getter.get_result_by_request(url=url)
        soup = BeautifulSoup(json_data, 'html.parser')

        for release in soup.findAll('td'):
            if 'safari' in release.text.lower():
                latest_version = release.text.lower().split('safari ')[1]

                if '.' not in latest_version:
                    latest_version = str(float(latest_version))
                break

        if not latest_version:
            message = 'Could not determine latest version of safaridriver, maybe the site was changed'
            raise ValueError(message)

        logger.info(f'Latest version of safaridriver: {latest_version}')

        return latest_version
