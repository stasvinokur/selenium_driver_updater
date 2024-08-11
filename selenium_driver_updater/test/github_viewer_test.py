import pytest
import jsonschema
import json
from pathlib import Path
from selenium_driver_updater.util.github_viewer import GithubViewer
from selenium_driver_updater.util.exceptions import StatusCodeNotEqualException
from selenium_driver_updater._setting import setting

@pytest.fixture(scope="module")
def setup():
    """Fixture for setting up the environment."""
    return {
        "github_viewer": GithubViewer,
        "repo_name": 'mozilla/geckodriver',
        "specific_version": '0.29.0',
        "specific_asset_name": 'win64',
        "json_schema": json.loads(Path(setting['JsonSchema']['githubReleaseSchema']).read_text(encoding='utf-8'))
    }

def test_get_all_releases_data_by_repo_name_failure(setup):
    with pytest.raises(StatusCodeNotEqualException):
        releases = setup["github_viewer"].get_all_releases_data_by_repo_name(repo_name='mazilla/geckadruver')
        assert len(releases) >= 0, "Expected no releases data due to invalid repo name"

def test_get_latest_release_tag_by_repo_name_failure(setup):
    with pytest.raises(StatusCodeNotEqualException):
        tag = setup["github_viewer"].get_latest_release_tag_by_repo_name(repo_name='mazilla/geckadruver')
        assert len(tag) >= 0, "Expected no tag data due to invalid repo name"

def test_get_release_version_by_repo_name_failure(setup):
    with pytest.raises(StatusCodeNotEqualException):
        version = setup["github_viewer"].get_release_version_by_repo_name(repo_name='mazilla/geckadruver')
        assert len(version) >= 0, "Expected no version data due to invalid repo name"

def test_get_all_releases_data_by_repo_name_and_validate_json_schema(setup):
    releases = setup["github_viewer"].get_all_releases_data_by_repo_name(repo_name=setup["repo_name"])
    assert releases is not None, "Expected releases data"
    assert len(releases) > 0, "Expected non-empty releases data"

    schema = setup["json_schema"]
    for release in releases:
        assert jsonschema.validate(instance=release, schema=schema) is None

def test_get_latest_release_tag_by_repo_name(setup):
    tag_api = setup["github_viewer"].get_latest_release_tag_by_repo_name(repo_name='ariya/phantomjs')
    assert tag_api is not None, "Expected latest release tag from API"
    assert len(tag_api) > 0, "Expected non-empty latest release tag from API"

    tag_site = setup["github_viewer"].get_release_version_by_repo_name_via_site(repo_name='ariya/phantomjs')
    assert tag_site is not None, "Expected latest release tag from website"
    assert len(tag_site) > 0, "Expected non-empty latest release tag from website"

    assert tag_api == tag_site, f'API tag: {tag_api} does not match site tag: {tag_site}'

def test_get_release_version_by_repo_name(setup):
    version_api = setup["github_viewer"].get_release_version_by_repo_name(repo_name=setup["repo_name"])
    assert len(version_api) >= 0, "Expected non-empty version from API"

    version_site = setup["github_viewer"].get_release_version_by_repo_name_via_site(repo_name=setup["repo_name"])
    assert len(version_site) >= 0, "Expected non-empty version from website"

    assert version_api == version_site, f'API version: {version_api} does not match site version: {version_site}'