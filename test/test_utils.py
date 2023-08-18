import asyncio
import urllib
from pathlib import Path
from typing import Any

import pytest

from mp3_autotagger.utils import get_package_version, get_youtube_audiostream, shazam_find_track_info, update_package


@pytest.fixture(scope="class")
def package_name() -> str:
    return "mp3-autotagger"


@pytest.fixture(scope="class")
def assets_dirpath() -> Path:
    return Path("test/assets")


@pytest.fixture(scope="class")
def video_url() -> str:
    return "https://www.youtube.com/watch?v=HHjSdy9l7Kc"


@pytest.fixture(scope="class")
def mp3_filepath(assets_dirpath: Path) -> Path:
    return assets_dirpath / "tmp.mp3"


@pytest.fixture(scope="class")
def audiostream(video_url: str, assets_dirpath: Path) -> dict[str, Any]:
    return get_youtube_audiostream(video_url, assets_dirpath)


@pytest.fixture(scope="class", autouse=True)
def cleanup(mp3_filepath: Path, assets_dirpath: Path) -> None:
    yield  # This makes sure the cleanup happens after tests run
    if mp3_filepath.exists():
        mp3_filepath.unlink()
    if (assets_dirpath / "15 Seconds.mp3").exists():
        (assets_dirpath / "15 Seconds.mp3").unlink()


def test_shazam_find_track_info(assets_dirpath: Path) -> None:
    shazam_out = asyncio.run(shazam_find_track_info(assets_dirpath / "example_0.mp3"))
    assert shazam_out["track"]["subtitle"].upper() == "RED HOT CHILI PEPPERS"
    assert shazam_out["track"]["title"] == "Scar Tissue"
    assert shazam_out["track"]["sections"][0]["metadata"][0]["text"] == "Californication (Remastered)"
    assert shazam_out["track"]["genres"]["primary"] == "Alternative"
    assert shazam_out["track"]["sections"][0]["metadata"][2]["text"] == "1999"
    assert urllib.request.urlopen(shazam_out["track"]["images"]["coverarthq"]).status == 200  # OK


def test_download_youtube_audiostream(audiostream: dict[str, Any], assets_dirpath: Path) -> None:
    assert audiostream["ext"] == "webm"
    assert audiostream["title"] == "15 Seconds"
    assert audiostream["abr"] == 132.155
    assert audiostream["filesize"] == 248138
    assert (assets_dirpath / f"{audiostream['title']}.mp3").exists()


def test_update_package(package_name: str) -> None:
    initial_version = get_package_version(package_name)
    status = update_package()
    updated_version = get_package_version(package_name)
    if updated_version == initial_version:
        assert status == f"{package_name} is already at the latest version ({updated_version})."
    else:
        assert status == f"{package_name} updated successfully from version {initial_version} to {updated_version}!"
