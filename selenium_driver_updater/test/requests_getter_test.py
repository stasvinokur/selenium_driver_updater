import pytest
from selenium_driver_updater.util.requests_getter import RequestsGetter
from selenium_driver_updater._setting import setting
import os

@pytest.fixture(scope="module")
def setup():
    """Fixture for setting up the environment."""
    return {
        "requests_getter": RequestsGetter,
    }

def test_check_get_result_by_request_failure(setup):
    url = 'hi'  # Invalid URL to trigger failure
    with pytest.raises(Exception):
        setup["requests_getter"].get_result_by_request(url=url)

def test_check_get_result_by_request(setup):
    url = setting['ChromeDriver']['LinkLastRelease']
    json_data = setup["requests_getter"].get_result_by_request(url=url)
    
    # Check if the response is a non-empty string
    assert isinstance(json_data, str), "Expected the result to be a string"
    assert len(json_data) > 0, "Expected non-empty result"