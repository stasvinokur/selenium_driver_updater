#Standart library imports
from typing import Any, Optional

#Requests imports
import requests
from requests.models import Response

#Local imports
from selenium_driver_updater.util.exceptions import StatusCodeNotEqualException

class RequestsGetter():
    """Class for working with requests module"""

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/35.0.1916.47 Safari/537.36'

    _headers = {'User-Agent': user_agent}

    @staticmethod
    def get_result_by_request(
        url : str, is_json : bool = False,
        no_error_status_code : bool = False) -> Any:
        """Gets html text and status_code from the specified url by get request

        Args:
            url (str)                   : Url which we will use for getting information
            cookies                     : Specific cookies for request
            is_json (bool)              : Transorm request.text to json or not. Defaults to False.
            no_error_status_code (bool) : Will not throw an error if status_code not equal to 200.

        Returns:
            str

            request_text (str)  : Returns the html text of the given url

        """

        status_code : int = 0
        request_text : str = ''
        request : Optional[Response] = None

        request = requests.get(url=url, headers=RequestsGetter._headers)
        status_code = request.status_code
        request_text = request.text

        if status_code != 200 and not no_error_status_code:

            message_run = (f'url: {url} status_code: {status_code}'
                            f'not equal to 200 request_text: {request.text}')
            raise StatusCodeNotEqualException(message_run)

        if is_json:
            request_text = request.json()

        return request_text
