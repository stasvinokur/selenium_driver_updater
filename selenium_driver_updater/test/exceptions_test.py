import pytest
import logging

from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater.util.github_viewer import GithubViewer
from selenium_driver_updater.util.exceptions import StatusCodeNotEqualException

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope="module")
def setup_requests_getter():
    return RequestsGetter

def test_status_code_not_equal_exception(setup_requests_getter):
    url = 'https://google.com/aboba'  # Некорректный URL
    with pytest.raises(StatusCodeNotEqualException):
        setup_requests_getter.get_result_by_request(url=url)