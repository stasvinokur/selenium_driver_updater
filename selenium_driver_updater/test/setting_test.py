import pytest
import platform
import os

from selenium_driver_updater._setting import setting

# Общие переменные для тестов
base_dir = os.path.dirname(os.path.abspath(__file__))[:-5] + os.path.sep
os_bit = platform.architecture()[0][:-3]
os_bit_phantom_js = 'x86_64' if os_bit == '64' else "i686"

is_arm = 'arm' in platform.processor().lower()
if os.name != 'nt':  # Check if not на Windows
    is_arm = is_arm or 'arm' in str(os.uname().machine)

os_type = {
    'Windows': {
        'chromedriver': f"win{os_bit}",
        'geckodriver': f"win{os_bit}.zip" if not is_arm else "win-aarch64.zip",
        'operadriver': f"win{os_bit}",
        'edgedriver': f"win{os_bit}",
        'phantomjs': "windows.zip",
    },
    'Linux': {
        'chromedriver': "linux64",
        'geckodriver': f"linux{os_bit}.tar.gz" if not is_arm else "linux-aarch64.tar.gz",
        'operadriver': "linux64",
        'edgedriver': "linux64",
        'phantomjs': f"linux-{os_bit_phantom_js}.tar.bz2",
    },
    'Darwin': {
        'chromedriver': "mac-x64" if not is_arm else "mac-arm64",
        'geckodriver': "macos.tar.gz" if not is_arm else "macos-aarch64.tar.gz",
        'operadriver': "mac64",
        'edgedriver': "mac64" if not is_arm else "mac64_m1",
        'phantomjs': "macosx",
    },
    'Other': {
        'edgedriver': "arm64" if is_arm else None,
    }
}

os_name = platform.system()
if os_name not in ['Darwin', 'Linux', 'Windows']:
    os_name = 'Other'

latest_release = "https://storage.googleapis.com/chrome-for-testing-public/{}/"
chromedriver_latest_release = f'{latest_release}{os_type[os_name]["chromedriver"]}' + f"/chromedriver-{os_type[os_name]['chromedriver']}.zip"

latest_release_geckodriver = 'https://github.com/mozilla/geckodriver/releases/download/v{}/'
geckodriver_platform_release = f'{latest_release_geckodriver}geckodriver-v{{}}-{os_type[os_name]["geckodriver"]}'

latest_release_operadriver = 'https://github.com/operasoftware/operachromiumdriver/releases/download/v.{}/'
operadriver_latest_release = f'{latest_release_operadriver}operadriver_{os_type[os_name]["operadriver"]}.zip'

latest_release_edgedriver = 'https://msedgedriver.azureedge.net/{}/'
edgedriver_latest_release = f'{latest_release_edgedriver}edgedriver_{os_type[os_name]["edgedriver"]}.zip'

url_release_phantomjs = "https://api.bitbucket.org/2.0/repositories/ariya/phantomjs/downloads/"
phantomjs_latest_release = f'{url_release_phantomjs}phantomjs-{{}}-{os_type[os_name]["phantomjs"]}.zip'

browser_paths = {
    'Darwin': {
        'chrome': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                   "/Applications/Chromium.app/Contents/MacOS/Chromium"],
        'firefox': '/Applications/Firefox.app/Contents/MacOS/firefox',
        'edge': '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
        'edge_release': 'https://go.microsoft.com/fwlink/?linkid=2069148&platform=Mac&Consent=1&channel=Stable' if not is_arm else
                        'https://go.microsoft.com/fwlink/?linkid=2093504&platform=Mac&Consent=1&channel=Stable',
        'opera': '/Applications/Opera.app/Contents/MacOS/Opera',
    },
    'Windows': {
        'chrome': ['reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                   r'reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v version'],
        'firefox': ['reg query "HKEY_CURRENT_USER\Software\Mozilla\Mozilla Firefox" /v CurrentVersion',
                    'reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Mozilla Firefox" /v CurrentVersion',
                    r"Powershell (Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)').VersionInfo.ProductVersion"],
        'edge': 'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
        'opera': r'reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall" /f Opera',
    },
    'Linux': {
        'chrome': 'google-chrome-stable',
        'firefox': 'firefox',
        'opera': 'opera',
    }
}

chrome_browser_path = browser_paths[os_name].get('chrome', '')
firefox_browser_path = browser_paths[os_name].get('firefox', '')
edge_browser_path = browser_paths[os_name].get('edge', '')
edge_browser_release = browser_paths[os_name].get('edge_release', '')
opera_browser_path = browser_paths[os_name].get('opera', '')

@pytest.fixture(scope="module")
def settings():
    return setting

def test_check_count_main_param(settings):
    assert len(settings) == 14

def test_check_count_params(settings):
    assert len(settings["Program"]) == 5
    assert len(settings["ChromeDriver"]) == 5
    assert len(settings["GeckoDriver"]) == 2
    assert len(settings["OperaDriver"]) == 2
    assert len(settings["EdgeDriver"]) == 5
    assert len(settings["PhantomJS"]) == 3
    assert len(settings["SafariDriver"]) == 2

    assert len(settings["ChromeBrowser"]) == 3
    assert len(settings["FirefoxBrowser"]) == 3
    assert len(settings["EdgeBrowser"]) == 3
    assert len(settings["OperaBrowser"]) == 2

    assert len(settings["JsonSchema"]) == 3
    assert len(settings["Github"]) == 3
    assert len(settings["PyPi"]) == 1

def test_check_values_params(settings):
    assert settings["Program"]["version"] == "7.0.0"
    assert settings["Program"]["wedriverVersionPattern"] == r'([0-9.]*\.[0-9]+)'
    assert settings["Program"]["driversPath"] == base_dir + 'test' + os.path.sep + 'drivers' + os.path.sep
    file_format = ".exe" if platform.system() == 'Windows' else ''
    assert settings["Program"]["DriversFileFormat"] == file_format
    assert settings["Program"]["OSBitness"] == os_bit

    assert settings["ChromeDriver"]["LinkLastReleaseFile"] == chromedriver_latest_release
    assert settings["ChromeDriver"]["LinkLastRelease"] == "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"
    
    assert settings["GeckoDriver"]["LinkLastReleasePlatform"] == geckodriver_platform_release
    
    assert settings["OperaDriver"]["LinkLastReleasePlatform"] == operadriver_latest_release
    
    assert settings["EdgeDriver"]["LinkLastReleaseFile"] == edgedriver_latest_release
    
    assert settings["PhantomJS"]["LinkLastReleaseFile"] == phantomjs_latest_release
    assert settings["PhantomJS"]["LinkAllReleases"] == url_release_phantomjs

    assert settings["SafariDriver"]["LinkLastRelease"] == 'https://support.apple.com/en-us/HT201222'
    
    assert settings["ChromeBrowser"]["Path"] == chrome_browser_path
    
    assert settings["FirefoxBrowser"]["Path"] == firefox_browser_path

    assert settings["EdgeBrowser"]["Path"] == edge_browser_path
    assert settings["EdgeBrowser"]["LinkAllLatestReleaseFile"] == edge_browser_release

    assert settings["OperaBrowser"]["Path"] == opera_browser_path

    assert settings["JsonSchema"]["githubAssetSchema"] == base_dir + 'schemas' + os.path.sep + 'github_asset_schema.json'
    assert settings["JsonSchema"]["githubReleaseSchema"] == base_dir + 'schemas' + os.path.sep + 'github_release_schema.json'
    assert settings["JsonSchema"]["githubReleaseTagSchema"] == base_dir + 'schemas' + os.path.sep + 'github_release_tag_schema.json'

    assert settings["Github"]["linkLatestReleaseBySpecificRepoName"] == 'https://api.github.com/repos/{}/releases/latest'
    assert settings["Github"]["linkAllReleasesTags"] == 'https://api.github.com/repos/{}/git/refs/tags'
    assert settings["Github"]["linkAllReleases"] == 'https://api.github.com/repos/{}/releases?per_page=100000'

    assert settings["PyPi"]["urlProjectJson"] == 'https://pypi.python.org/pypi/selenium-driver-updater/json'