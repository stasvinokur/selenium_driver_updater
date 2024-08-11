#pylint: disable=broad-except,wrong-import-position, protected-access
#Standart library imports
import unittest
import os.path
import time
import platform
import logging
from pathlib import Path

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._operaDriver import OperaDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

logging.basicConfig(level=logging.INFO)

# pylint: disable=missing-function-docstring
class testOperaDriver(unittest.TestCase):
    """Class for unit-testing OperaDriver class

    Attributes:
        path (str)              : Specific path where test drivers located
        opera_driver            : Initialize class OperaDriver
        startTime (float)       : Time of starting unit-tests
        setting (dict[str])     : Dict of all additional parametres
        headers                 : Needed headers for requests
        specific_version (str)  : Specific version of edgedriver to test
    """
    @classmethod
    def setUpClass(cls):
        cls.setting = setting

        path : str = str(setting["Program"]["driversPath"])

        parametres = dict(driver_name='operadriver', path=path,
        info_messages=True, filename='operadriver_test', version='',
        check_browser_is_up_to_date = False)

        cls.operadriver = OperaDriver(**parametres)

        parametres.update(path='failure', filename='operadriver1_test', version='blablabla')

        cls.operadriver_failure = OperaDriver(**parametres)

        cls.requests_getter = RequestsGetter

    @classmethod
    def tearDownClass(cls):
        del cls.operadriver
        del cls.operadriver_failure

    def setUp(self):
        self.path : str = str(setting["Program"]["driversPath"])

        self.start_time : float = time.time()

        self.specific_version : str = '89.0.4389.82'
        self.specific_version_failure : str = 'blablablanotversion'

        self.operadriver_name : str = "operadriver_test.exe" if platform.system() == 'Windows' else\
                                        "operadriver_test"

        self.operadriver_path = self.path + self.operadriver_name

    def tearDown(self):
        end_time = time.time() - self.start_time
        print("%.3f" % end_time)

    #@unittest.skip('Temporary not needed')
    def test01_check_get_current_version_operadriver_selenium_failure(self):
        try:
            current_version = self.operadriver_failure._get_current_version_driver()
            self.assertEqual(len(current_version), 0, len(current_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test02_check_download_driver(self):
        try:
            file_name = self.operadriver_failure._download_driver(version=self.specific_version_failure)
            self.assertEqual(len(file_name), 0, len(file_name))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test03_check_compare_current_version_and_latest_version_failure(self):
        try:
            is_driver_is_up_to_date, current_version, latest_version = self.operadriver_failure._compare_current_version_and_latest_version_github()
            self.assertFalse(is_driver_is_up_to_date, is_driver_is_up_to_date)
            self.assertEqual(len(current_version), 0, len(current_version))
            self.assertEqual(len(latest_version), 0, len(latest_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test04_check_if_operadriver_is_up_to_date_failure(self):
        try:
            filename = self.operadriver_failure.main()
            self.assertEqual(len(filename), 0, len(filename))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test05_check_if_version_is_valid_failure(self):
        url = 'blablablanoturl'
        try:
            self.operadriver_failure._check_if_version_is_valid(url=url)
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test06_check_download_driver_specific_version(self):
        self.operadriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.operadriver_path).exists(), self.operadriver_path)

        file_name = self.operadriver._download_driver(version=self.specific_version)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.operadriver_path).exists(), self.operadriver_path)

        self.operadriver._chmod_driver()

        current_version = self.operadriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))
        self.assertEqual(current_version, self.specific_version)

    #@unittest.skip('Temporary not needed')
    def test07_check_download_driver_latest_previous_version(self):
        self.operadriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.operadriver_path).exists(), self.operadriver_path)

        file_name = self.operadriver._download_driver(previous_version=True)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.operadriver_path).exists(), self.operadriver_path)

        self.operadriver._chmod_driver()

        current_version = self.operadriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test08_check_get_latest_version_operadriver(self):
        latest_version = self.operadriver._get_latest_version_driver_github()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test09_check_delete_current_operadriver_for_current_os(self):
        self.operadriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.operadriver_path).exists(), self.operadriver_path)

    #@unittest.skip('Temporary not needed')
    def test10_check_download_driver(self):
        file_name = self.operadriver._download_driver()
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.operadriver_path).exists(), self.operadriver_path)

        self.operadriver._chmod_driver()

    #@unittest.skip('Temporary not needed')
    def test11_check_compare_current_version_and_latest_version(self):
        is_driver_is_up_to_date, current_version, latest_version = self.operadriver._compare_current_version_and_latest_version_github()
        self.assertIsNotNone(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertIsNotNone(current_version, current_version)
        self.assertIsNotNone(latest_version, latest_version)
        self.assertTrue(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertGreater(len(current_version), 0, len(current_version))
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test12_check_get_current_version_operadriver_selenium(self):
        current_version = self.operadriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreater(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test13_check_if_operadriver_is_up_to_date(self):
        filename = self.operadriver.main()
        self.assertGreater(len(filename), 0, len(filename))

    ##@unittest.skip('Temporary not needed')
    def test14_check_if_version_is_valid(self):
        url = str(self.setting["OperaDriver"]["LinkLastReleasePlatform"]).format(self.specific_version)

        self.operadriver_failure._check_if_version_is_valid(url=url)

if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)
    