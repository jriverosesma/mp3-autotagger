import requests
from PyQt5 import QtCore, QtGui

from mp3_autotagger import __version__ as current_version
from mp3_autotagger.utils.package import is_running_as_pyinstaller_bundle

REPOSITORY_OWNER: str = "jriverosesma"
REPOSITORY_NAME: str = "mp3-autotagger"

translate: callable = QtCore.QCoreApplication.translate


def get_releases_from_github(owner: str, repo: str) -> list[str]:
    """
    Get published releases for a GitHub repository.

    Args:
        owner (str): repository owner.
        repo (str): repository name.

    Returns:
        (list[str]): List of releases.
    """

    url = f"https://api.github.com/repos/{owner}/{repo}/releases"

    response = requests.get(url)

    if response.status_code == 200:
        releases = response.json()
        return [release["tag_name"] for release in releases]
    else:
        raise ValueError(
            f"Bad response ({response.status_code}) from the GitHub API. No releases found for the repository."
        )


def check_for_updates() -> str:
    """
    Check for application updates.

    Returns:
        str: A message indicating if there are new appliation updates available.
    """

    releases: list[str] = get_releases_from_github(REPOSITORY_OWNER, REPOSITORY_NAME)
    newest_version = releases[0]
    if current_version == newest_version:
        return translate("Main Window", f"mp3-autotagger is already at the latest version ({current_version})")
    else:
        if is_running_as_pyinstaller_bundle():
            message = translate(
                "Main Window",
                (
                    f"Newest mp3-autotagger version {newest_version} available in "
                    f"<a href='https://github.com/{REPOSITORY_OWNER}/{REPOSITORY_NAME}/releases'>GitHub</a>!"
                ),
            )
        else:
            message = translate(
                "Main Window",
                (
                    f"<p>Newest mp3-autotagger version {newest_version} available.</p>"
                    "<p>Install using: <code>pip install --upgrade mp3-autotagger</code></p>"
                ),
            )
        return message
