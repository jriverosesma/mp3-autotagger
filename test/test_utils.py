import asyncio
import os
import urllib

import pytest

from mp3_autotagger.utils import get_package_version, get_youtube_audiostream, shazam_find_track_info, update_package


@pytest.fixture(scope="class")
def package_name():
    return "mp3-autotagger"


@pytest.fixture(scope="class")
def assets_dirpath():
    return "test/assets"


@pytest.fixture(scope="class")
def video_url():
    return "https://www.youtube.com/watch?v=HHjSdy9l7Kc"


@pytest.fixture(scope="class")
def mp3_filepath(assets_dirpath):
    return os.path.join(assets_dirpath, "tmp.mp3")


@pytest.fixture(scope="class")
def audiostream(video_url, assets_dirpath):
    return get_youtube_audiostream(video_url, assets_dirpath)


@pytest.fixture(scope="class", autouse=True)
def cleanup(mp3_filepath, assets_dirpath):
    yield  # This makes sure the cleanup happens after tests run
    if os.path.exists(mp3_filepath):
        os.remove(mp3_filepath)
    if os.path.exists(assets_dirpath + "/15 Seconds.mp3"):
        os.remove(assets_dirpath + "/15 Seconds.mp3")


def test_shazam_find_track_info(assets_dirpath):
    shazam_out = asyncio.run(shazam_find_track_info(assets_dirpath + "/example_0.mp3"))
    assert shazam_out["track"]["subtitle"].upper() == "RED HOT CHILI PEPPERS"
    assert shazam_out["track"]["title"] == "Scar Tissue"
    assert shazam_out["track"]["sections"][0]["metadata"][0]["text"] == "Californication (Remastered)"
    assert shazam_out["track"]["genres"]["primary"] == "Alternative"
    assert shazam_out["track"]["sections"][0]["metadata"][2]["text"] == "1999"
    assert urllib.request.urlopen(shazam_out["track"]["images"]["coverarthq"]).status == 200  # OK


def test_download_youtube_audiostream(audiostream, assets_dirpath):
    assert audiostream["ext"] == "webm"
    assert audiostream["title"] == "15 Seconds"
    assert audiostream["abr"] == 132.155
    assert audiostream["filesize"] == 248138
    assert os.path.exists(assets_dirpath + f"/{audiostream['title']}.mp3")


def test_update_package(package_name):
    initial_version = get_package_version(package_name)
    status = update_package()
    updated_version = get_package_version(package_name)
    if updated_version == initial_version:
        assert status == f"{package_name} is already at the latest version ({updated_version})."
    else:
        assert status == f"{package_name} updated successfully from version {initial_version} to {updated_version}!"
