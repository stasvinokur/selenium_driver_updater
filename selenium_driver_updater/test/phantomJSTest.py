#pylint: disable=broad-except,wrong-import-position, protected-access
#Standart library imports
import unittest
import os.path
import time
import platform
import logging
from pathlib import Path

import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater._phantomJS import PhantomJS

from selenium_driver_updater.util.requests_getter import RequestsGetter

from selenium_driver_updater.util.exceptions import DriverVersionInvalidException

logging.basicConfig(level=logging.INFO)

# pylint: disable=missing-function-docstring
class testPhantomJS(unittest.TestCase):
    """Class for unit-testing PhantomJS class

    Attributes:
        path (str)              : Specific path where test drivers located
        phantomjs               : Initialize class PhantomJS
        startTime (float)       : Time of starting unit-tests
        setting (dict[str])     : Dict of all additional parametres
        specific_version (str)  : Specific version of chromedriver to test
    """

    @classmethod
    def setUpClass(cls):
        cls.setting = setting

        path : str = str(setting["Program"]["driversPath"])

        parametres = dict(driver_name='phantomjs', path=path,
        info_messages=True, filename='phantomjs_test', version='')

        cls.phantomjs = PhantomJS(**parametres)

        parametres.update(path='failure', filename='phatomjs1_test', version='blablabla')

        cls.phantomjs_failure = PhantomJS(**parametres)

        cls.requests_getter = RequestsGetter

    @classmethod
    def tearDownClass(cls):
        del cls.phantomjs
        del cls.phantomjs_failure

    def setUp(self):

        self.path : str = str(setting["Program"]["driversPath"])

        self.start_time : float = time.time()

        self.specific_version : str = '2.1.1'
        self.specific_version_failure : str = 'blablablanotversion'

        self.phantomjs_name : str = "phantomjs_test.exe" if platform.system() == 'Windows' else\
                                        "phantomjs_test"

        self.phantomjs_path = self.path + self.phantomjs_name

    def tearDown(self):
        end_time = time.time() - self.start_time
        print("%.3f" % end_time)

    #@unittest.skip('Temporary not needed')
    def test01_check_get_current_version_phantomjs(self):
        try:
            current_version = self.phantomjs_failure._get_current_version_driver()
            self.assertEqual(len(current_version), 0, len(current_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test02_check_download_driver_failure(self):
        try:
            current_version = self.phantomjs_failure._download_driver(version=self.specific_version_failure)
            self.assertEqual(len(current_version), 0, len(current_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test03_check_compare_current_version_and_latest_version_failure(self):
        try:
            is_driver_is_up_to_date, current_version, latest_version = self.phantomjs_failure._compare_current_version_and_latest_version_github()
            self.assertFalse(is_driver_is_up_to_date, is_driver_is_up_to_date)
            self.assertEqual(len(current_version), 0, len(current_version))
            self.assertEqual(len(latest_version), 0, len(latest_version))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test04_check_phantomjs_is_up_to_date_failure(self):
        try:
            filename = self.phantomjs_failure.main()
            self.assertEqual(len(filename), 0, len(filename))
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    ##@unittest.skip('Temporary not needed')
    def test05_check_if_version_is_valid_failure(self):
        try:
            url = str(self.setting["PhantomJS"]["LinkAllReleases"]).format(self.specific_version_failure)
            self.phantomjs_failure._check_if_version_is_valid(url=url)
        except Exception as error:
            self.assertTrue(error.__class__ == DriverVersionInvalidException, error.__class__)

    #@unittest.skip('Temporary not needed')
    def test06_check_get_latest_version_phantomjs(self):
        latest_version = self.phantomjs._get_latest_version_phantomjs()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

    #@unittest.skip('Temporary not needed')
    def test07_check_download_driver_specific_version(self):
        self.phantomjs._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.phantomjs_path).exists(), self.phantomjs_path)

        file_name = self.phantomjs._download_driver(version=self.specific_version)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.phantomjs_path).exists(), self.phantomjs_path)

        self.phantomjs._chmod_driver()

        current_version = self.phantomjs._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))
        self.assertEqual(current_version, self.specific_version)

    @unittest.skip('Temporary not needed')
    def test08_check_download_driver_latest_previous_version(self):
        self.phantomjs._delete_current_driver_for_current_os()
        self.assertFalse(Path(self.phantomjs_path).exists(), self.phantomjs_path)

        file_name = self.phantomjs._download_driver(previous_version=True)
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.phantomjs_path).exists(), self.phantomjs_path)

        self.phantomjs._chmod_driver()

        current_version = self.phantomjs._get_current_version_driver()
        self.assertIsNotNone(current_version, current_version)
        self.assertGreaterEqual(len(current_version), 0, len(current_version))


    #@unittest.skip('Temporary not needed')
    def test09_check_download_driver(self):
        latest_version = self.phantomjs._get_latest_version_phantomjs()
        self.assertIsNotNone(latest_version, latest_version)
        self.assertGreater(len(latest_version), 0, len(latest_version))

        file_name = self.phantomjs._download_driver()
        self.assertIsNotNone(file_name,file_name)
        self.assertGreater(len(file_name), 0, len(file_name))
        self.assertTrue(Path(self.phantomjs_path).exists(), self.phantomjs_path)

        self.phantomjs._chmod_driver()

    #@unittest.skip('Temporary not needed')
    def test10_check_phantomjs_is_up_to_date(self):
        filename = self.phantomjs.main()
        self.assertGreater(len(filename), 0, len(filename))

    #@unittest.skip('Temporary not needed')
    def test11_check_if_version_is_valid(self):
        url = str(self.setting["PhantomJS"]["LinkLastReleaseFile"]).format(self.specific_version)
        self.phantomjs._check_if_version_is_valid(url=url)

if __name__ == '__main__':
    unittest.main(verbosity=2, failfast=True, exit=False)
    