from selenium_driver_updater._chromeDriver import ChromeDriver
from selenium_driver_updater._geckoDriver import GeckoDriver
from selenium_driver_updater._operaDriver import OperaDriver
from selenium_driver_updater._edgeDriver import EdgeDriver
from selenium_driver_updater._safari_driver import SafariDriver

ALL_DRIVERS= {
    "chromedriver" : ChromeDriver,
    "geckodriver" : GeckoDriver,
    "operadriver" : OperaDriver,
    "edgedriver" : EdgeDriver,
    "safaridriver" : SafariDriver,
}
