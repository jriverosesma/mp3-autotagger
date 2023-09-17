from unittest.mock import Mock, patch

import pytest

from mp3_autotagger import __version__ as current_version
from mp3_autotagger.utils.update import check_for_updates, get_releases_from_github

REPOSITORY_OWNER: str = "jriverosesma"
REPOSITORY_NAME: str = "mp3-autotagger"
RELEASES_URL = f"https://api.github.com/repos/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/releases"


def test_get_releases_from_github_success():
    # Mocking a successful response from the GitHub API.
    mocked_response = Mock()
    mocked_response.status_code = 200
    # Corrected the response structure to match the expected response from the function.
    mocked_response.json.return_value = [{"tag_name": "1.0"}, {"tag_name": "0.9"}]

    with patch("requests.get", return_value=mocked_response) as mock_get:
        releases = get_releases_from_github(REPOSITORY_OWNER, REPOSITORY_NAME)
        mock_get.assert_called_once_with(RELEASES_URL)
        assert releases == ["1.0", "0.9"]


def test_get_releases_from_github_failure():
    # Mocking a failure response from the GitHub API.
    mocked_response = Mock()
    mocked_response.status_code = 404
    mocked_response.json.return_value = []

    with patch("requests.get", return_value=mocked_response) as mock_get:
        with pytest.raises(ValueError, match=r"Bad response \(404\) from the GitHub API"):
            get_releases_from_github(REPOSITORY_OWNER, REPOSITORY_NAME)
            mock_get.assert_called_once_with(RELEASES_URL)


def test_check_for_updates_latest_version():
    # Mock the function to return a version list where the current version is the latest.
    with patch("mp3_autotagger.utils.update.get_releases_from_github", return_value=[current_version, "0.9"]):
        result = check_for_updates()
        assert result == f"mp3-autotagger is already at the latest version ({current_version})"


def test_check_for_updates_new_version_available():
    # Mock the function to return a version list where there's a newer version.
    newest_version = "1.1"
    with patch("mp3_autotagger.utils.update.get_releases_from_github", return_value=[newest_version, current_version]):
        result = check_for_updates()
        assert result == (
            f"<p>Newest mp3-autotagger version {newest_version} available.</p>"
            "<p>Install using: <b>pip install --upgrade mp3-autotagger</b></p>"
        )
