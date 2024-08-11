#pylint: disable=broad-except,wrong-import-position, protected-access
#Standart library imports
import time
import platform
import unittest
import os.path
import logging
from pathlib import Path

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._chromeDriver import ChromeDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter

logging.basicConfig(level=logging.INFO)

from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

# pylint: disable=missing-function-docstring
class testChromeDriver(unittest.TestCase):
    """Class for unit-testing ChromeDriver class

    Attributes:
        path (str)              : Specific path where test drivers located
        chrome_driver           : Initialize class ChromeDriver
        startTime (float)       : Time of starting unit-tests
        setting (dict[str])     : Dict of all additional parametres
        specific_version (str)  : Specific version of chromedriver to test
    """

    @classmethod
    def setUpClass(cls):
        cls.setting = setting

        path : str = str(setting["Program"]["driversPath"])

        parametres = dict(driver_name='chromedriver', path=path,
        info_messages=True, filename='chromedriver_test', version='',
        check_browser_is_up_to_date = False)

        cls.chrome_driver = ChromeDriver(**parametres)

        parametres.update(path='failure', filename='chromedriver1_test', version='blablabla')

        cls.chrome_driver_failure = ChromeDriver(**parametres)

        cls.requests_getter = RequestsGetter

    @classmethod
    def tearDownClass(cls):
        del cls.chrome_driver
        del cls.chrome_driver_failure

    def setUp(self):

        self.path : str = str(setting["Program"]["driversPath"])

        self.start_time : float = time.time()

        self.specific_version : str = '115.0.5763.0'
        self.specific_version_failure : str = 'blablablanotversion'

        self.chromedriver_name : str = "chromedriver_test.exe" if platform.system() == 'Windows' else\
                                        "chromedriver_test"

        self.chromedriver_path = self.path + self.chromedriver_name

    def tearDown(self):
        end_time = time.time() - self.start_time
        print("%.3f" % end_time)

    #@unittest.skip('Temporary not needed')
    def test01_check_get_current_version_chrome_selenium_failure(self):
        current_version = self.chrome_driver_failure._get_current_version_driver()
        self.assertEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test02_check_download_driver_failure(self):
        try:
            file_name = self.chrome_driver_failure._download_driver(version=self.specific_version_failure)
            self.assertEqual(len(file_name), 0, len(file_name))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test03_check_compare_current_version_and_latest_version_failure(self):
        is_driver_is_up_to_date, current_version, latest_version = self.chrome_driver_failure._compare_current_version_and_latest_version()
        self.assertFalse(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertEqual(len(current_version), 0, len(current_version))
        self.assertEqual(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test04_check_chromedriver_is_up_to_date_failure(self):
        try:
            filename = self.chrome_driver_failure.main()
            self.assertEqual(len(filename), 0, len(filename))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test05_check_if_version_is_valid_failure(self):
        url = 'blablablanoturl'
        try:
            self.chrome_driver_failure._check_if_version_is_valid(url=url)
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test06_check_get_result_by_request(self):
        url = str(self.setting["ChromeDriver"]["LinkLastRelease"])
        json_data = self.requests_getter.get_result_by_request(url=url)
        self.assertGreaterEqual(len(json_data), 0, len(json_data))

    #@unittest.skip('Temporary not needed')
    def test07_check_get_result_by_request(self):
        latest_version = self.chrome_driver._get_latest_version_driver()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

        latest_previous_version = latest_version.split(".", maxsplit=1)[0]

        url = str(self.setting["ChromeDriver"]["LinkLatestReleaseSpecificVersion"]).format(latest_previous_version)
        json_data = self.requests_getter.get_result_by_request(url=url)
        self.assertGreaterEqual(len(json_data), 0, len(json_data))

    #@unittest.skip('Temporary not needed')
    def test08_check_get_current_version_chrome_selenium(self):
        current_version = self.chrome_driver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test09_check_download_driver_specific_version(self):
        self.chrome_driver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.chromedriver_path).exists(), self.chromedriver_path)

        file_name = self.chrome_driver._download_driver(version=self.specific_version)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.chromedriver_path).exists(), self.chromedriver_path)

        self.chrome_driver._chmod_driver()

        current_version = self.chrome_driver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))
        self.assertEqual(current_version, self.specific_version)

    #@unittest.skip('Temporary not needed')
    def test10_check_download_driver_latest_previous_version(self):
        self.chrome_driver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.chromedriver_path).exists(), self.chromedriver_path)

        file_name = self.chrome_driver._download_driver(previous_version=True)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.chromedriver_path).exists(), self.chromedriver_path)

        self.chrome_driver._chmod_driver()

        current_version = self.chrome_driver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test11_check_get_latest_version_chrome_driver(self):
        latest_version = self.chrome_driver._get_latest_version_driver()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test12_check_delete_current_chromedriver_for_current_os(self):
        self.chrome_driver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.chromedriver_path).exists(), self.chromedriver_path)

    #@unittest.skip('Temporary not needed')
    def test13_check_download_driver(self):
        latest_version = self.chrome_driver._get_latest_version_driver()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

        file_name = self.chrome_driver._download_driver()
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.chromedriver_path).exists(), self.chromedriver_path)

        self.chrome_driver._chmod_driver()

    #@unittest.skip('Temporary not needed')
    def test14_check_compare_current_version_and_latest_version(self):
        is_driver_is_up_to_date, current_version, latest_version = self.chrome_driver._compare_current_version_and_latest_version()
        self.assertIsNotNone(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertIsNotNone(current_version, current_version)
        self.assertIsNotNone(latest_version, latest_version)
        self.assertTrue(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertGreater(len(current_version), 0, len(current_version))
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test15_check_get_current_version_chrome_selenium(self):
        current_version = self.chrome_driver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreater(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test16_check_chromedriver_is_up_to_date(self):
        filename = self.chrome_driver.main()
        self.assertGreater(len(filename), 0, len(filename))

    ##@unittest.skip('Temporary not needed')
    def test17_check_if_version_is_valid(self):
        url = str(self.setting["ChromeDriver"]["LinkLastReleaseFile"]).format(self.specific_version)

        self.chrome_driver._check_if_version_is_valid(url=url)


if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)
