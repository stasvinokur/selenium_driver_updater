#Standart library imports
from typing import Any
import re

#Third party imports
from bs4 import BeautifulSoup

# Local imports
from selenium_driver_updater._setting import setting
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.logger import logger

from selenium_driver_updater.util.exceptions import StatusCodeNotEqualException, GithubApiLimitException

class GithubViewer():
    """Class for working with github repositories"""

    API_RATE_LIMIT_MSG = 'API rate limit exceeded for'

    @staticmethod
    def get_release_version_by_repo_name(repo_name: str, index:int = 0) -> str:
        """Gets latest release asset by github repository name

        Args:
            repo_name (str): Repository path on github.

        Returns:
            Any

            version         : All latest release data.
        """

        if index:
            url: str = str(setting["Github"]["linkAllReleases"]).format(repo_name)
        else:
            url: str = str(setting["Github"]["linkLatestReleaseBySpecificRepoName"]).format(repo_name)
        version: Any = ''

        try:
            version = RequestsGetter.get_result_by_request(url=url, is_json=True)

            if index:
                version = version[index].get('name')
            else:
                version = version.get('name')

        except StatusCodeNotEqualException as error:
            if GithubViewer.API_RATE_LIMIT_MSG in error.args[0]:
                message = 'Github API rate limit exceeded for your IP, trying to get needed data via site.'
                logger.warning(message)

                version = GithubViewer.get_release_version_by_repo_name_via_site(repo_name=repo_name, index=index)

            else:
                raise StatusCodeNotEqualException from error

        return version

    @staticmethod
    def get_all_releases_data_by_repo_name(repo_name: str) -> Any:
        """Gets all releases data by github repository name

        Args:
            repo_name (str): Repository path on github.

        Returns:
            Any

            json_data         : All releases data.
        """

        url: str = str(setting["Github"]["linkAllReleases"]).format(repo_name)

        try:

            json_data = RequestsGetter.get_result_by_request(url=url, is_json=True)

        except StatusCodeNotEqualException as error:
            if GithubViewer.API_RATE_LIMIT_MSG in error.args[0]:
                message = 'Github API rate limit exceeded for your IP, could not get needed data.'
                logger.warning(message)
                raise GithubApiLimitException(message) from error
            else:
                raise StatusCodeNotEqualException from error

        return json_data

    @staticmethod
    def get_release_version_by_repo_name_via_site(repo_name: str, index:int = 0) -> Any:
        """Gets latest release asset by github repository name

        Args:
            repo_name (str): Repository path on github.

        Returns:
            Any

            json_data         : All latest release data.
        """

        url: str = str(setting["Github"]["linkAllReleases"]).format(repo_name)
        version:str = ''

        json_data = RequestsGetter.get_result_by_request(url=url)

        soup = BeautifulSoup(json_data, 'html.parser')
        try:
            version = soup.findAll('a', href=lambda href: href and 'releases/tag' in href)[index].text.strip()
        except IndexError:
            logger.error('Could not retrieve version via releases, trying to retrieve version via tags')
            url: str = 'https://github.com/{}/tags'.format(repo_name)

            json_data = RequestsGetter.get_result_by_request(url=url)

            soup = BeautifulSoup(json_data, 'html.parser')

            version_tag = soup.findAll('a', href=lambda href: href and 'releases/tag' in href)[index].text.strip()

            version = re.findall(setting["Program"]["wedriverVersionPattern"], str(version_tag))[0]

        return version

    @staticmethod
    def get_latest_release_tag_by_repo_name(repo_name: str) -> Any:
        """Gets latest release tag by github repository name
        Args:
            repo_name (str): Repository path on github.
        Returns:
            Any
            json_data         : Latest release tag.
        """

        url: str = str(setting["Github"]["linkAllReleasesTags"]).format(repo_name)

        try:

            json_data = RequestsGetter.get_result_by_request(url=url, is_json=True)

            find_string = re.findall(str(setting["Program"]["wedriverVersionPattern"]), json_data[-1].get('ref'))
            tag = find_string[0] if len(find_string) > 0 else ''

        except StatusCodeNotEqualException as error:
            if GithubViewer.API_RATE_LIMIT_MSG in error.args[0]:
                message = 'Github API rate limit exceeded for your IP, could not get needed data.'
                logger.warning(message)

                tag = GithubViewer.get_release_version_by_repo_name_via_site(repo_name=repo_name)

            else:
                raise StatusCodeNotEqualException from error

        return tag
