#Standart library imports
import argparse

#Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.driverUpdater import DriverUpdater

#pylint: disable=protected-access
class ConsoleUpdater():
    """Class for working with command line of selenium driver updater library"""

    @staticmethod
    def parse_command_line():
        "Function for parsing arguments that were specified in command line"

        description_text = (
        "Download or update your selenium driver binaries and their browsers automatically with this package.\n\n"
        "Available drivers are: (you can use them with -d or --driver_name command)\n"
        "chromedriver, edgedriver, geckodriver, phantomjs, operadriver, safaridriver\r\n\r\n"
        "Available OSes are: (you can use them with --system_name command)\n"
        "win64, win32, linux64, linux32, mac64, mac64_m1 (stands for mac with arm-based architecture), arm64"
        )
        parser = argparse.ArgumentParser(
            description=description_text, formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument(
        "--driver_name",
        "-d",
        type=ConsoleUpdater.comma_separated_string,
        action="store",
        dest="driver_name",
        metavar="DRIVER_NAME",
        help="Specified driver name/names which will be downloaded or updated, if you want to specify multiple drivers, use commas",
        default='',
        required=True,
        )
        parser.add_argument(
        "--path",
        "-p",
        action="store",
        dest="path",
        metavar="DIR",
        help="Specified path which will used for downloading or updating Selenium driver binary. Must be folder path",
        default='',
        )
        parser.add_argument(
        "--info_messages",
        "-im",
        action="store",
        dest="info_messages",
        metavar="BOOLEAN",
        help="If false, it will disable all info messages",
        default=True,
        )
        parser.add_argument(
        "--filename",
        type=ConsoleUpdater.comma_separated_string,
        action="store",
        dest="filename",
        metavar="FILENAME",
        help="Specific name for driver. If given, it will replace name for driver",
        default='',
        )
        parser.add_argument(
        "--check_browser_is_up_to_date",
        "-cb",
        action="store",
        dest="check_browser_is_up_to_date",
        metavar="BOOLEAN",
        help="If true, it will check browser version before specific driver update or upgrade",
        default=False,
        )
        parser.add_argument(
        "--system_name",
        action="store",
        dest="system_name",
        metavar="SYSTEM_NAME",
        help="Specific OS for driver",
        default='',
        )
        parser.add_argument("--version", action="version", version=str(setting["Program"]["version"]))
        return parser.parse_args()
    
    @staticmethod
    def comma_separated_string(value):
        """Convert a comma-separated string into a list or return as a string if no comma."""
        if ',' in value:
            return value.split(',')
        return value

    @staticmethod
    def install():
        "Main function that initializes all variables and pass it to main module (driver Updater)"

        args = ConsoleUpdater.parse_command_line()
        kwargs = vars(args)
        
        if kwargs['filename']:
            if isinstance(kwargs['driver_name'], list) and isinstance(kwargs['filename'], str):
                kwargs['filename'] = [kwargs['filename']]

        DriverUpdater.install(**kwargs)
