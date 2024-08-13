## [7.0.0] - xx/08/2024
This version was written and tested on Python 3.11.1

#### Added

- Added new command assosiation "selupd" for easier use
- Added automatic pypi release
- Added deleting of .tmp files when downloading is manually stopped (KeyboardInterrupt)

#### Improvements

- Cosmetic changes to code
- Improved tests by switching from unit-tests to pytest
- Parameters chmod, upgrade, check_driver_is_up_to_date have been Deprecated. Now always defaults to True.
- Parameter "check_browser_is_up_to_date" renamed to "check_browser" for easier use.
- Made code easier to read, removed some complexity in the code

#### Fixes

- Fixed an issue with incorrect extracting of tar.gz archives when specific filename is present
- Fixed an issue with incorrect extracting of chromedriver with third_party_notice file
- Fixed an issues with browsers versions checking

#### Removed

- Removed support for PhantomJS
- Removed downloading of browsers on MacOS. Only kept checking current and latest versions.
- Removed Pylint comments everywhere, because of the use of sonarlint and sonarqube.

## [6.0.3] - 07/03/2024
This version was written and tested on Python 3.11.1

#### Fixes

- Fixed an issue with incorrect url in chromedriver (#6)
- Fixed an issue with not including all results when getting releases from github

## [6.0.2] - 26/09/2023
This version was written and tested on Python 3.11.1

#### Fixes

- Fixed checking for ARM-based architecture on Windows

## [6.0.1] - 26/09/2023
This version was written and tested on Python 3.11.1

#### Added

- Added new package "packaging" in setup.py

#### Improvements

- Improved code in setting.py, made it more readable (config file)
- Overall code improvements

## [6.0.0] - 02/09/2023
This version was written and tested on Python 3.11.1

#### Complete overhaul of chromedriver
- Added updated method to download chromedriver
- Added support for Windows 64 bit chromedriver

#### Added
- Added support for Windows ARM, Linux ARM Geckodriver
- Added proper comparison of versions
- Added universal extraction of only drivers (before it was extracting all elements in archive)
- Added support of multiple drivers in console updater - you need to separate drivers with comma, like this: chromedriver,geckodriver
- Added support for one filename if multiple drivers are given

#### Improved
- Improved console line updater help function and added more additional information to become more understandable to user
- Improved WGET bar to be more understandable, now file size is measuring in MB's
- Overall code improvements

#### Removed
- Removed parameter "old_return"

## [5.1.8] - 22/01/2023
This version was written and tested on Python 3.11.1
This version fully supports Python 3.11!

#### Improvements

- Improved detecting M1 binary of chromedriver without additional checks
- Improved some unit-tests

#### Fixes

- Fixed an issue with incorrect getting of latest previous version of edgedriver

#### Other

- Removed requirement for selenium to be lower than or equal to version 4.2.0

## [5.1.7] - 02/12/2022
This version was written and tested on Python 3.10.8

#### Fixes

- Fixed CVE-2007-4559 patch (thanks to TrellixVulnTeam)

#### Other

- Added requirement for selenium to be lower than or equal to version 4.2.0

## [5.1.6] - 14/11/2022
This version was written and tested on Python 3.10.8

#### Fixes

- Minor fixes

## [5.1.5] - 09/11/2022
This version was written and tested on Python 3.10.8

#### Added

- Added checking for Mac M1 binary if specific version of edgedriver specified
- Added checking for suitable version if latest previous version parameter is on

#### Fixes

- Fixed an issue that caused Mac M1 users to install the default Mac EdgeDriver even though the Mac M1 binary was available.

## [5.1.4] - 08/11/2022
This version was written and tested on Python 3.10.8
This version fully supports Python 3.10!
#### Fixes

- Fixed an issue with incorrect downloading of Mac M1 binaries of chromedriver

## [5.1.3] - 03/11/2021
This version was written and tested on Python 3.9.6

#### Fixes

- Fixed an issue with incorrect getting of latest version of edgedriver (#1)

## [5.1.2] - 24/10/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue where the previous latest version was incorrectly received through the github site
- Fixed an issue with incorrect getting of phantomjs versions via github releases
- Fixed an issue if browser is not pre installed and could not be updated
- Fixed an issue with incorrect getting of latest previous version of edgedriver

## [5.1.1] - 25/09/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect getting of latest version of edge browser (returned old method of getting version)
- Fixed an issue with incorrect getting of latest version of safaridriver

## [5.1.0] - 27/08/2021
This version was written and tested on Python 3.9.6

### Added

- Added full updating of edge, opera, firefox and chrome browsers on MacOS (full installation instead of browser update command)
- Added full updating of opera browser on Windows (full installation instead of browser update command)

- Added killing of browser if its getting updated
- Added support for edgedriver ARM version on Windows

### Improvements

- Speeded up getting latest version of safaridriver
- Improved parameter "old_return" with improved back-compatibility

### Fixes

- Partial fixed of getting latest version of edge browser (already fixed in version 5.0.4)
- Fixed an issue with incorrect default path detecting if library was ran in console mode (already fixed in version 5.0.3)

### Other

- Setted default value "False" for parameter "old_return"

## [5.0.4] - 27/08/2021
This version was written and tested on Python 3.9.6

### Fixes

- Partial fixed of getting latest version of edge browser 

## [5.0.3] - 17/08/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect default path detecting if library was ran in console mode

## [5.0.2] - 09/08/2021
This version was written and tested on Python 3.9.6

### Improvements

- Simplified checking for correct driver_name

### Other

- Dropped support for chromium chromedriver and chromiumbrowser (due to incorrect concept)

## [5.0.1] - 07/08/2021
This version was written and tested on Python 3.9.6

### Improvements

- Improved and fixed getting latest version of opera browser

## [5.0.0] - 06/08/2021
This version was written and tested on Python 3.9.6

### Added

- Added custom logger (No need to override root logger now)
- Added custom user-defined exceptions instead of “result and message”
- Added parameter "old_return" for returning old variables like "result and message" (if you need to)
- Added command line control
- Added alternative method of getting needed data via github if github api limit is restricted (not all methods, but many necessary)
- Added base class for all driver classes
- Added support for safaridriver (not updating or downloading)
- Added properly exiting driver with context managers instead of driver.quit()

### Improvements

- Simplified driver classes initialization
- Simplified checking for correct driver_name
- Improved driver version validating if specific version was given
- Improved getting current version of chrome browser on MacOS (added additional path)

### Fixes

- Fixed an issue with incorrect operadriver downloading (fixed in 4.1.5)
- Fixed an issue if multiply identical drivers and different OS's names were given and later was incorrect filename extension checking (fixed in 4.1.6)
- Fixed an issue with incorrect getting current version of opera browser (fixed in 4.1.7)

### Other

- Removed error handling pattern

## [4.1.7] - 04/08/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect getting current version of opera browser

## [4.1.6] - 30/07/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue if multiply identical drivers and different OS's names were given and later was incorrect filename extension checking

## [4.1.5] - 28/07/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect operadriver downloading

## [4.1.4] - 22/07/2021
This version was written and tested on Python 3.9.6

### Improvements

- Improved getting current version of firefox browser

## [4.1.3] - 19/07/2021
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect folder imports

### Comments 

(For example there was two folders - one folder in library and one from another directory, 
library takes folder from another directory, not from herself)

## [4.1.2] - 12/07/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.6

### Operations

- Setted correct default value for OS parameter "linux"

## [4.1.1] - 08/07/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.6

### Fixes

- Fixed an issue with incorrect filename extension on Windows

## [4.1.0] - 08/07/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.6

### Improvements

- Improved overall code optimization

## [4.0.2] - 07/07/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.6

### Fixes

- Minor fixes with phantomjs

## [4.0.1] - 07/07/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.6

### Improvements

- Improved overall code optimization

### Fixes

- Fixed an issues with incorrect checking of system_name for chromedriver

### Operations

- Removed some duplicated code

## [4.0.0] - 05/07/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### New

- Added new OS type "ARM"
- Added correct errors exceptions

### Improvements

- Improved code optimization
- Improved getting latest previous version for edgedriver

### Operations

- Global code refactoring

## [3.16.0] - 29/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved getting latest version of firefox browser
- Improved error messages

## [3.15.0] - 28/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved getting latest version of Chrome Browser (added os detection in post text)

## [3.14.0] - 24/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved working with paths (replaced all os.path calls to pathlib.Path)

### Fixes

- Fixed an issue with incorrect unit-tests status code return

## [3.13.0] - 21/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved overall code optimization (improved drivers classes initialization)
- Improved getting current version of opera browser for Windows
- Improved getting latest version of edgedriver
- Improved unit-tests (remove unnecessary redefinition of variables)

### Fixes

- Fixed an issue with incorrect parametres initalization if multiply drivers were given

## [3.12.3] - 18/06/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed some issues with typing

## [3.12.2] - 18/06/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed some issues with typing

## [3.12.1] - 18/06/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed some issues with typing

## [3.12.0] - 18/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### New

- Added version validation for latest previous version of driver

### Improvements

- Improved overall code optimization
- Improved getting current and latest versions of drivers (fixed incorrect regex)

### Fixes

- Fixed an issue with incorrect getting of current version of firefox browser
- Fixed an issue with incorrect validation of specific version for operadriver
- Fixed an issue with system_name if multiply specific OS's were given

### Operations

- Removed unused imports
- Removed unnecessary function in github_viewer

## [3.11.1] - 15/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with unable to start downloading driver

## [3.11.0] - 15/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved overall code optimization (removed many unnecessary rederections of variables)
- Improved unit-tests

### Fixes

- Fixed an issue with unable to get latest version of edgedriver

## [3.10.0] - 07/06/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support for downloading multiply specific versions for multiply drivers

### Improvements

- Improved overall code optimization (removed alternative method for getting current version of driver via its capabilities)
- Improved unit-tests

### Fixes

- Fixed an issue with incorrect version validation for operadriver

## [3.9.1] - 05/06/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Minor fixes

## [3.9.0] - 05/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Speeded up phantomjs binary download
- Speeded up validation of specific version for phantomjs
- Improved unit-tests

## [3.8.0] - 03/06/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Speeded up validation of specific version for all drivers
- Improved unit-tests by all drivers and github_viewer

## [3.7.0] - 02/06/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added parameter "system_name" for downloading drivers for specific OS
- Added support for downloading multiply drivers with specific OS's
Like:

DriverUpdater.install(driver_name=DriverUpdater.chromedriver, system_name=DriverUpdater.windows)

### Improvements

- Improved getting current version of edge and chrome browsers via terminal on Windows
- Improved unit-tests by all drivers

### Fixes

- Fixed an issue with incorrect detecting current version of fifefox browser via terminal
- Fixed an issue with incorrect getting of latest previous version of edgedriver

## [3.6.0] - 31/05/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added downloading of latest previous version when latest version of driver cannot be downloaded

### Improvements

- Improved getting latest version of geckodriver and operadriver
- Improved overall code optimization

## [3.5.2] - 30/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Minor fixes with unit-tests

## [3.5.1] - 30/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Minor fixes with unit-tests

## [3.5.0] - 30/05/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support for edgedriver on Linux

### Improvements

- Improved overall code optimization
- Improved unit-tests

### Operations

- Separated drivers and browsers into different files

## [3.4.0] - 28/05/2021
This version provides some innovations.
This version was written and tested on Python 3.9.5

### New

- Added support for multiply driver filenames if multiply drivers were given.

Like:

list_drivers = ## [DriverUpdater.chromedriver, DriverUpdater.geckodriver, DriverUpdater.edgedriver]
filenames = ## ['chrometest', 'geckotest']

DriverUpdater.install(driver_name=list_drivers, filename=filenames)

## [3.3.1] - 27/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with incorrect downloading and renaming phantomjs driver on Linux

## [3.3.0] - 27/05/2021
This version provides some innovations and minor fixes.
This version was written and tested on Python 3.9.5

### New

- Added support for some lower versions of Python (3.8 and lower).
If you are have some issues with library on lowers versions please report it in repository.

### Fixes

- Fixed an issue if info_messages was False, but progress bar was not hidden.
- Fixed an issue with incorrect return of drivers path if multiply drivers were given.

## [3.2.1] - 26/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with incorrect detection of phantomjs os bitness on Linux

## [3.2.0] - 26/05/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support for PhantomJS
- Added properly comparing of latest and current version of library
- Added unit-tests by PhantomJS

### Improvements

- Improved getting latest version of chrome browser
- Improved getting current version of drivers via its capabilities
- Improved overall code optimization
- Improved unit-tests by extractor and github_viewer

### Fixes

- Fixed an issue with getting latest version of webdriver twice, if driver was not exists
- Fixed an issue with incorrect return of path, if chromedriver main version was not equals to chrome browser main version

## [3.1.0] - 25/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue "module 'os' has no attribute 'getuid'" on Windows

### Operations

- Removed some duplicated code

## [3.0.1] - 24/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Minor fixes with unit-tests

## [3.0.0] - 24/05/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support of chromium_chromedriver webdriver on Linux

- Added support of updating chrome browser on Linux
- Added support of updating firefox on Linux
- Added support of updating opera browser on Linux

- Added unit-tests by chromiumChromeDriver module

### Improvements

- Improved overall code optimization
- Improved unit-tests

### Fixes

- Fixed an issue if incorrect driver_name was given, but there was no error message
- Fixed an issue with incorrect comparing of main version of chromedriver and chrome browser

### Operations

- Droped support for edgedriver on Linux (not supported yet)
- Removed all unused variables in code
- Removed all unused imports in code

## [2.19.0] - 23/05/2021
This version provides some innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support for updating chromium browser for Linux

### Improvements

- Improved getting current version of firefox on different Windows versions

### Fixes

- Fixed an issue when webdriver browser was not checked if webdriver was not exists

## [2.18.0] - 22/05/2021
This version provides some improvements and optimizations.
This version was written and tested on Python 3.9.5

### New

- Added bigger timeout while updating webdrivers browsers

### Improvements

- Improved overall code optimization

### Operations

- Speeded up all webdrivers download

## [2.17.0] - 21/05/2021
This version provides some improvements and minor fixes.
This version was written and tested on Python 3.9.5

### New

- Added getting current versions of edge and opera browsers via terminal on Windows

### Improvements

- Improved getting current versions of webdrivers and webdrivers browsers on different OS's

### Fixes

- Fixed some issues with unit-tests

## [2.16.0] - 20/05/2021
This version provides some improvements and fixes.
This version was written and tested on Python 3.9.5

### Improvements

- Improved getting latest version of webdriver browsers

### Fixes

- Fixed an issue with incorrect determination latest version of chrome browser
- Fixed an issue with incorrect determination latest version of opera browser in some OS's

## [2.15.1] - 19/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with unable to determination latest version of chrome browser

## [2.15.0] - 18/05/2021
This version provides some minor improvements.
This version was written and tested on Python 3.9.5

### Improvements

- Improved overall code optimization

## [2.14.0] - 17/05/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added default folder path - if path does not specified
- Added unit-tests by requests_getter module

### Improvements

- Improved functions decomposition
- Improved unit-tests (added checking with incorrect parameters - for failure test)

### Fixes

- Fixed an issue if edgedriver return result was false, without printing an error message
- Fixed an issue with slow downloading of specific version of edgedriver

## [2.13.1] - 15/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with incorrect detection of firefox browser path on Windows

## [2.13.0] - 15/05/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.5

### Improvements

- Improved getting current version of chrome browser, firefox, opera browser and edge browser on MacOS 
- Improved getting current version of chromebrowser and firefox on Windows
- Improved getting current version of webdrivers in MacOS and Windows
- Improved unit-tests (added checking with incorrect parameters - for failure test)

## [2.12.0] - 13/05/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added support for multiply driver names in parameters

### Improvements

- Improved overall code optimization
- Improved function decomposition
- Improved unit-tests (added checking with incorrect parameters - for failure test)

## [2.11.0] - 11/05/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.5

### New

- Added checking for python version while start

### Improvements

- Improved overall code optimization
- Improved function decomposition
- Improved unit-tests

### Fixes

- Fixed an issue if same drivers filenames was in library and in different directory

## [2.10.1] - 11/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with unable to determination latest version of chrome browser

## [2.10.0] - 10/05/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.5

### New

- Added unit-tests by driverUpdater class

### Improved

- Improved overall code optimization

### Operations

- Deleted some duplicated code

## [2.9.1] - 09/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.5

### Fixes

- Fixed an issue with some logging that ignored "info_messages" parameter

## [2.9.0] - 09/05/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.5

### New

- Added checking of library is up to date
- Added new parameter (enable_library_update_check) - for enable or disable checking versions

## [2.8.0] - 07/05/2021
This version provides some minor improvements.
This version was written and tested on Python 3.9.4

### Improvements

- Improved setting.py file (became more understandable)

### Operations

- Removed some hardcode from operaDriver.py file

## [2.7.1] - 05/05/2021
This version provides improvements and minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect geckodriver and operadriver downloading if macOS was on Intel

## [2.7.0] - 05/05/2021
This version provides improvements and minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect geckodriver, edgedriver downloading if macOS was on Intel

### Improvements

- Improved unit-tests by githubviewer
- Improved overall code optimization

## [2.6.3] - 04/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with unable to determination latest version of chrome browser

## [2.6.2] - 04/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Minor fixes

## [2.6.1] - 04/05/2021
This version provides some minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect checking of OS bitness. (Windows)
- Fixed an issue with incorrect checking of driver if macOS was on Intel. (with other drivers)

## [2.6.0] - 04/05/2021
This version provides improvements and minor fixes.
This version was written and tested on Python 3.9.4

### New

- Added protect from downloading incorrect version of chromedriver

### Improvements

- Improved unit-tests by githubviewer
- Improved unit-tests by all drivers

### Fixes

- Fixed an issue with incorrect checking of OS bitness. (Windows)
- Fixed an issue with incorrect checking of driver if macOS was on Intel.

## [2.5.2] - 03/05/2021
This version provides minor fixes and improvements.
This version was written and tested on Python 3.9.4

### Operations

- Minor fixes with unit-tests

## [2.5.1] - 03/05/2021
This version provides minor fixes and improvements.
This version was written and tested on Python 3.9.4

### Improvements

- Improved deletion of different Selenium driver binaries.

### Operations

- Turned off some tests that cannot run on github workflow.

## [2.5.0] - 03/05/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added requirements.txt for github workflow (this will be not included in final package)
- Added validating of json_data from github
- Added **kwargs instead of many parameters

### Improvements

- Improved unit-tests by githubviewer

## [2.4.0] - 02/05/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added unit-tests by all classes in /util folder

### Improvements

- Improved unit-tests by all drivers

## [2.3.0] - 01/05/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added support for updating firefox browser for Windows

### Improvements

- Improved unit-tests by chromedriver

### Operations

- Excluded unneccessary files in final package

## [2.2.0] - 30/04/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added support for updating chrome browser for MacOS
- Added support for updating edge browser for MacOS
- Added support for updating opera browser for MacOS
- Added support for updating firefox browser for MacOS

### Improvements

- Improved functions decomposition

## [2.1.0] - 29/04/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added support for updating edge browser for Windows
- Added support for updating opera browser for Windows

### Improvements

- Improved unit tests by all drivers

## [2.0.0] - 28/04/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added support for updating chrome browser for Windows

## [1.9.0] - 27/04/2021
This version provides minor fixes and improvements.
This version was written and tested on Python 3.9.4

### New

- Added error message if request status_code not equal 200.

### Operations

- Removed all unused imports.

## [1.8.1] - 26/04/2021
This version provides minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue were some folder were not uploaded to pypi

## [1.8.0] - 26/04/2021
This version provides some improvements.
This version was written and tested on Python 3.9.4

### Improvements

- Improved functions decomposition.

## [1.7.1] - 26/04/2021
This version provides minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue if file setting.py was in library and in different directory.

## [1.7.0] - 25/04/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.4

### New

- Added unit tests for all drivers
- Added support for downloading specific version of driver

## [1.6.0] - 24/04/2021
This version provides innovations and improvements.
This version was written and tested on Python 3.9.4

### New

- Added error message if Selenium binaries was not found in github assets.

### Improvements

- Improved functions decomposition.

## [1.5.3] - 24/04/2021
This version provides minor bug fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect name of some drivers If no name was given for the driver

## [1.5.2] - 24/04/2021
This version provides minor bug fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect name of some drivers If no name was given for the driver
- Fixed an issue with incorrect unpack of geckodriver if was Windows OS

## [1.5.1] - 23/04/2021
This version provides minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect unpack of some drivers If no name was given for the driver

## [1.5.0] - 23/04/2021
This version provides innovations and minor improvements.
This version was written and tested on Python 3.9.4

### New

- Added support for different names of Selenium webdriver binary.
- Added detailed return to main function
- Added lighter function call

### Fixes

- Fixed an issue with incorrect detection of system bitness.

## [1.4.0] - 22/04/2021
This version provides innovations and minor fixes.
This version was written and tested on Python 3.9.4

### New

- Added edgedriver support
- Added support for downloading different OS bit (x86 / x64)

## [1.3.1] - 21/04/2021
This version provides minor fixes.
This version was written and tested on Python 3.9.4

### Fixes

- Fixed an issue with incorrect checking of the given path

## [1.3.0] - 21/04/2021
This version provides innovations and minor fixes.
This version was written and tested on Python 3.9.4

### New

- Added support for geckodriver
- Added support for operadriver

### Fixes

- Fixed an error when chromedriver wasnt in the specific folder and parameter "check_driver_is_up_to_date" was True

## [1.2.0] - 20/04/2021
This version provides innovations and minor fixes.
This version was written and tested on Python 3.9.4

### New

- Added additional parameter "check_driver_is_up_to_date" for checking chromedriver version before and after updating.
- Added additional parameter "info_message" for disabling info messages during installation or updating.
- Added additional info messages to some functions

## [1.1.0] - 19/04/2021
This version provides minor fixes and improvements.
This version was written and tested on Python 3.9.4

### New

- Added Google Docstring to each functions
- Added checking for all input parameters

## [1.0.2] - 18/04/2021

- Removed unneccessary folders

## [1.0.0] - 18/04/2021

- Initial release