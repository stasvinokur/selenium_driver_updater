#pylint: disable=invalid-name
#Standart library imports
import os
import platform

base_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

os_bit = platform.architecture()[0][:-3]
os_bit_phantom_js = 'x86_64' if os_bit == '64' else "i686"

is_arm = 'arm' in platform.processor().lower()
if os.name != 'nt':  # Check if not on Windows
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

#
# BROWSERS AND THEIR UPDATERS
#                                 

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

from dataclasses import dataclass

@dataclass
class info:
    version = "7.0.0"

setting = dict(
    {
        "Program":
        {
            'version'                   : info.version,
            'wedriverVersionPattern'    : r'([0-9.]*\.[0-9]+)',
            'driversPath'               : base_dir + 'test' + os.path.sep + 'drivers' + os.path.sep,
            'DriversFileFormat'         : ".exe" if platform.system() == 'Windows' else '',
            'OSBitness'                 : os_bit,
        },
        "ChromeDriver":
        {
            "LinkLastRelease"                   : "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json",
            "LinkLastReleaseFile"               : chromedriver_latest_release,
            "LastReleasePlatform"               : 'chromedriver',
            "LinkLatestReleaseSpecificVersion"  : "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{}",
            "LinkCheckVersionIsValid"           : "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json",
        },
        "GeckoDriver":
        {
            "LinkLastReleasePlatform"   : geckodriver_platform_release,
            "LastReleasePlatform"       : 'geckodriver',
        },
        "OperaDriver":
        {
            "LinkLastReleasePlatform"   : operadriver_latest_release,
            "LastReleasePlatform"       : 'operadriver',
        },
        "EdgeDriver":
        {
            "LinkLastRelease"                   : 'https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_STABLE',
            "LinkLastReleaseFile"               : edgedriver_latest_release,
            "LastReleasePlatform"               : 'msedgedriver',
            "LinkCheckVersionIsValid"           : "https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver?prefix={}%2F&delimiter=%2F&maxresults=100&restype=container&comp=list&_=1622714933676&timeout=60000",
            "LinkLatestReleaseSpecificVersion"  : "https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_RELEASE_{}_{}",
        },
        "PhantomJS":
        {
            "LinkLastReleaseFile"   : phantomjs_latest_release,
            "LastReleasePlatform"   : 'phantomjs',
            "LinkAllReleases"       : url_release_phantomjs,
        },
        "SafariDriver":
        {   
            "LinkLastRelease"       : 'https://support.apple.com/en-us/HT201222',
            "LastReleasePlatform"   : 'safaridriver',
        },
        "ChromeBrowser":
        {
            "Path"                      : chrome_browser_path,
            "LinkAllLatestRelease"      : 'https://chromereleases.googleblog.com/search/label/Stable%20updates',
            "LinkAllLatestReleaseFile"  : 'https://dl.google.com/chrome/mac/universal/stable/GGRO/googlechrome.dmg',
        },
        "FirefoxBrowser":
        {
            "Path"                          : firefox_browser_path,
            "LinkAllLatestReleases"         : 'https://www.mozilla.org/en-US/firefox/releases/',
            "LinkAllLatestRelease"          : 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/{}/{}/{}/Firefox {}.{}',
        },
        "EdgeBrowser":
        {
            "Path"                          : edge_browser_path,
            "LinkAllLatestRelease"          : 'https://docs.microsoft.com/en-us/deployedge/microsoft-edge-relnote-stable-channel',
            "LinkAllLatestReleaseFile"      : edge_browser_release,
        },
        "OperaBrowser":
        {
            "Path"                          : opera_browser_path,
            "LinkAllLatestRelease"          : 'https://get.geo.opera.com/pub/opera/desktop/',
        },
        "JsonSchema":
        {
            "githubAssetSchema"         : base_dir + 'schemas' + os.path.sep + 'github_asset_schema.json',
            "githubReleaseSchema"       : base_dir + 'schemas' + os.path.sep + 'github_release_schema.json',
            "githubReleaseTagSchema"    : base_dir + 'schemas' + os.path.sep + 'github_release_tag_schema.json',
        },
        "Github":
        {
            "linkLatestReleaseBySpecificRepoName"   : 'https://api.github.com/repos/{}/releases/latest',
            "linkAllReleasesTags"                   : 'https://api.github.com/repos/{}/git/refs/tags',
            "linkAllReleases"                       : 'https://api.github.com/repos/{}/releases?per_page=100000',
        },
        "PyPi":
        {
            'urlProjectJson'    : 'https://pypi.python.org/pypi/selenium-driver-updater/json',
        },
    }
)
