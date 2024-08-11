#pylint: disable=broad-except,wrong-import-position, protected-access
#Standart library imports
import unittest
import os.path
import time
import platform
from pathlib import Path
import logging

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._edgeDriver import EdgeDriver
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

logging.basicConfig(level=logging.INFO)

# pylint: disable=missing-function-docstring
class testEdgeDriver(unittest.TestCase):
    """Class for unit-testing EdgeDriver class

    Attributes:
        path (str)              : Specific path where test drivers located
        edge_driver             : Initialize class EdgeDriver
        startTime (float)       : Time of starting unit-tests
        setting (dict[str])     : Dict of all additional parametres
        headers                 : Needed headers for requests
        specific_version (str)  : Specific version of edgedriver to test
    """

    @classmethod
    def setUpClass(cls):
        cls.setting = setting

        path : str = str(setting["Program"]["driversPath"])

        parametres = dict(driver_name='edgedriver', path=path,
        info_messages=True, filename='edgedriver_test', version='',
        check_browser_is_up_to_date = False)

        cls.edgedriver = EdgeDriver(**parametres)

        parametres.update(path='failure', filename='edgedriver1_test', version='blablabla')

        cls.edgedriver_failure = EdgeDriver(**parametres)

        cls.requests_getter = RequestsGetter

    @classmethod
    def tearDownClass(cls):
        del cls.edgedriver
        del cls.edgedriver_failure

    def setUp(self):
        self.path : str = str(setting["Program"]["driversPath"])

        self.start_time : float = time.time()

        self.specific_version : str = '90.0.818.49'
        self.specific_version_failure : str = 'blablablanotversion'

        self.edgedriver_name : str = "edgedriver_test.exe" if platform.system() == 'Windows' else\
                                        "edgedriver_test"

        self.edgedriver_path = self.path + self.edgedriver_name

    def tearDown(self):
        end_time = time.time() - self.start_time
        print("%.3f" % end_time)

    #@unittest.skip('Temporary not needed')
    def test01_check_get_current_version_edge_selenium_failure(self):
        current_version = self.edgedriver_failure._get_current_version_driver()
        self.assertEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test02_check_download_driver(self):
        try:
            file_name = self.edgedriver_failure._download_driver(version=self.specific_version_failure)
            self.assertEqual(len(file_name), 0, len(file_name))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test03_check_compare_current_version_and_latest_version_failure(self):
        try:
            is_driver_is_up_to_date, current_version, latest_version = self.edgedriver_failure._compare_current_version_and_latest_version()
            self.assertFalse(is_driver_is_up_to_date, is_driver_is_up_to_date)
            self.assertEqual(len(current_version), 0, len(current_version))
            self.assertEqual(len(latest_version), 0, len(latest_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test04_check_if_edgedriver_is_up_to_date_failure(self):
        try:
            filename = self.edgedriver_failure.main()
            self.assertEqual(len(filename), 0, len(filename))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test05_check_if_version_is_valid_failure(self):
        url = 'blablablanoturl'
        try:
            self.edgedriver_failure._check_if_version_is_valid(url=url)
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test06_check_get_result_by_request(self):
        url = str(self.setting["EdgeDriver"]["LinkLastRelease"])
        json_data = self.requests_getter.get_result_by_request(url=url)
        self.assertGreaterEqual(len(json_data), 0, len(json_data))

    #@unittest.skip('Temporary not needed')
    def test07_check_get_current_version_edge_selenium(self):
        current_version = self.edgedriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test08_check_download_driver_specific_version(self):
        self.edgedriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.edgedriver_path).exists(), self.edgedriver_path)

        file_name = self.edgedriver._download_driver(version=self.specific_version)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.edgedriver_path).exists(), self.edgedriver_path)

        self.edgedriver._chmod_driver()

        current_version = self.edgedriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))
        self.assertEqual(current_version, self.specific_version)

    #@unittest.skip('Temporary not needed')
    def test09_check_download_driver_latest_previous_version(self):
        self.edgedriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.edgedriver_path).exists(), self.edgedriver_path)

        file_name = self.edgedriver._download_driver(previous_version=True)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.edgedriver_path).exists(), self.edgedriver_path)

        self.edgedriver._chmod_driver()

        current_version = self.edgedriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test10_check_get_latest_version_edge_driver(self):
        latest_version = self.edgedriver._get_latest_version_driver()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test11_check_delete_current_edgedriver_for_current_os(self):
        self.edgedriver._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.edgedriver_path).exists(), self.edgedriver_path)

    #@unittest.skip('Temporary not needed')
    def test12_check_download_driver(self):
        latest_version = self.edgedriver._get_latest_version_driver()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

        file_name = self.edgedriver._download_driver()
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.edgedriver_path).exists(), self.edgedriver_path)

        self.edgedriver._chmod_driver()

    #@unittest.skip('Temporary not needed')
    def test13_check_compare_current_version_and_latest_version(self):
        is_driver_is_up_to_date, current_version, latest_version = self.edgedriver._compare_current_version_and_latest_version()
        self.assertIsNotNone(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertIsNotNone(current_version, current_version)
        self.assertIsNotNone(latest_version, latest_version)
        self.assertTrue(is_driver_is_up_to_date, is_driver_is_up_to_date)
        self.assertGreater(len(current_version), 0, len(current_version))
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test14_check_get_current_version_edge_selenium(self):
        current_version = self.edgedriver._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreater(len(current_version), 0, len(current_version))

    #@unittest.skip('Temporary not needed')
    def test15_check_if_edgedriver_is_up_to_date(self):
        filename = self.edgedriver.main()
        self.assertGreater(len(filename), 0, len(filename))

    #@unittest.skip('Temporary not needed')
    def test16_check_if_version_is_valid(self):
        url = str(self.setting["EdgeDriver"]["LinkLastReleaseFile"]).format(self.specific_version)

        if 'mac64_m1' in url:
                try:
                    self.edgedriver._check_if_version_is_valid(url=url)
                except:
                    url = url.replace('mac64_m1', 'mac64')
                    self.edgedriver._check_if_version_is_valid(url=url)
        else:
            self.edgedriver._check_if_version_is_valid(url=url)

if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)
