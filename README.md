# selenium_driver_updater

[![PyPI version](https://badge.fury.io/py/selenium-driver-updater.svg)](https://badge.fury.io/py/selenium-driver-updater)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/selenium-driver-updater)](https://pepy.tech/project/selenium-driver-updater)
[![Downloads](https://static.pepy.tech/badge/selenium-driver-updater/month)](https://pepy.tech/project/selenium-driver-updater)
[![Downloads](https://static.pepy.tech/badge/selenium-driver-updater/week)](https://pepy.tech/project/selenium-driver-updater)

[![Build](https://github.com/stasvinokur/selenium_driver_updater/actions/workflows/build.yml/badge.svg)](https://github.com/stasvinokur/selenium_driver_updater/actions/workflows/build.yml)

It is a fast and convenience package that can automatically download or update Selenium webdriver binaries and their browsers for different OS.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install selenium_driver_updater.

```
pip install selenium-driver-updater
```

## Usage in code
This example shows how you can use this library to download chromedriver binary and use it immediately. The chromedriver will be downloaded to base directory.
```python
from selenium_driver_updater import DriverUpdater
from selenium import webdriver

filename = DriverUpdater.install(DriverUpdater.chromedriver)

driver = webdriver.Chrome(filename)
driver.get('https://google.com')

```

Or you can specify a path where you want to download a chromedriver to
```python
from selenium_driver_updater import DriverUpdater
from selenium import webdriver
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

filename = DriverUpdater.install(path=base_dir, driver_name=DriverUpdater.chromedriver)

driver = webdriver.Chrome(filename)
driver.get('https://google.com')

```

You can also specify the version type (beta, dev, canary) you want to download.
```python
from selenium_driver_updater import DriverUpdater
from selenium import webdriver

filename = DriverUpdater.install(driver_name=DriverUpdater.chromedriver, version=DriverUpdater.chromedriver_beta)

driver = webdriver.Chrome(filename)
driver.get('https://google.com')

```

You can also use library to download and update chromedriver and geckodriver binaries at the same time.
```python
from selenium_driver_updater import DriverUpdater
from selenium import webdriver
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
list_drivers = [DriverUpdater.chromedriver, DriverUpdater.geckodriver]

filenames = DriverUpdater.install(path=base_dir, driver_name=list_drivers)
print(filenames)

driver_chrome = webdriver.Chrome(filename[0])
driver_chrome.get('https://google.com')

driver_firefox = webdriver.Firefox(filename[1])
driver_firefox.get('https://google.com')

```

## Usage with help of command line
Use 
```bash
selenium-driver-updater --help
```
To see all available arguments and commands

Or you can use alias
```bash
selupd --help
```
for easier use

This example shows how you can use this console updater to download chromedriver to current dir 
```bash
selenium-driver-updater -d chromedriver
```

Or you can use console updater to download chromedriver and geckodriver at the same time
```bash
selenium-driver-updater -d chromedriver,geckodriver
```

# Supported Selenium Binaries

### ``Chromedriver`` 
#### ``DriverUpdater.chromedriver``

For installing or updating [chromedriver binary](https://developer.chrome.com/docs/chromedriver/)

All supported OS for this driver are:

- Windows
- Linux
- MacOS
- MacOS on M-based processors

### ``Geckodriver`` 
#### ``DriverUpdater.geckodriver``

For installing or updating [geckodriver binary](https://github.com/mozilla/geckodriver/releases)

All supported OS's for this driver are:

- Windows
- Windows ARM
- Linux
- Linux ARM
- MacOS
- MacOS on M-based processors

### ``Operadriver`` 
#### ``DriverUpdater.operadriver``

For installing or updating [operadriver binary](https://github.com/operasoftware/operachromiumdriver)

All supported OS's for this driver are:

- Windows
- Linux
- MacOS

### ``Edgedriver`` 
#### ``DriverUpdater.edgedriver``

For installing or updating [edgedriver binary](https://developer.microsoft.com/ru-ru/microsoft-edge/tools/webdriver/)

All supported OS's for this driver are:

- Windows
- Windows ARM
- MacOS
- MacOS on M-based processors
- Linux

### ``SafariDriver`` 
#### ``DriverUpdater.safaridriver``

For installing or updating [safaridriver binary](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)

All supported OS's for this driver are:

- MacOS

# Supported browsers for checking version

### ``Chrome Browser``

For checking version [chrome browser](https://www.google.com/chrome/)

### ``Firefox Browser``

For checking version [firefox browser](https://www.mozilla.org/en-US/firefox/)

### ``Opera Browser``

For checking version [opera browser](https://www.opera.com)

### ``Edge Browser``

For checking version [edge browser](https://www.microsoft.com/en-us/edge)