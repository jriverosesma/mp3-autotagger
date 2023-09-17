import pytest

from mp3_autotagger import __version__ as current_version
from mp3_autotagger.utils.update import check_for_updates, get_releases_from_github

REPOSITORY_OWNER: str = "jriverosesma"
REPOSITORY_NAME: str = "mp3-autotagger"
RELEASES_URL: str = f"https://api.github.com/repos/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/releases"


def test_get_releases_from_github_success(mocker):
    mocked_response = mocker.Mock()
    mocked_response.status_code = 200
    mocked_response.json.return_value = [{"tag_name": "1.0"}, {"tag_name": "0.9"}]

    mocker.patch("requests.get", return_value=mocked_response)

    releases = get_releases_from_github(REPOSITORY_OWNER, REPOSITORY_NAME)
    assert releases == ["1.0", "0.9"]


def test_get_releases_from_github_failure(mocker):
    mocked_response = mocker.Mock()
    mocked_response.status_code = 404
    mocked_response.json.return_value = []

    mocker.patch("requests.get", return_value=mocked_response)

    with pytest.raises(ValueError, match=r"Bad response \(404\) from the GitHub API"):
        get_releases_from_github(REPOSITORY_OWNER, REPOSITORY_NAME)


def test_check_for_updates_latest_version(mocker):
    mocker.patch("mp3_autotagger.utils.update.get_releases_from_github", return_value=[current_version, "0.9"])

    result = check_for_updates()
    assert result == f"mp3-autotagger is already at the latest version ({current_version})"


def test_check_for_updates_new_version_available(mocker):
    newest_version = "1.1"
    mocker.patch("mp3_autotagger.utils.update.get_releases_from_github", return_value=[newest_version, current_version])

    result = check_for_updates()
    assert result == (
        f"<p>Newest mp3-autotagger version {newest_version} available.</p>"
        "<p>Install using: <code>pip install --upgrade mp3-autotagger</code></p>"
    )
