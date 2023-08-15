import asyncio
import os
import shutil
import urllib

import pytest

from mp3_autotagger.utils import (
    convert2mp3,
    download_youtube_audiostream,
    get_youtube_audiostreams,
    shazam_find_track_info,
    update_app,
)


@pytest.fixture(scope="class")
def assets_dir():
    return "test/assets"


@pytest.fixture(scope="class")
def best_audiostream():
    return get_youtube_audiostreams("https://www.youtube.com/watch?v=HHjSdy9l7Kc", get_best_audio=True)


@pytest.fixture(scope="class")
def audiostreams():
    return get_youtube_audiostreams("https://www.youtube.com/watch?v=HHjSdy9l7Kc")


@pytest.fixture(scope="class")
def mp3_filepath(assets_dir):
    return os.path.join(assets_dir, "tmp.mp3")


@pytest.fixture(scope="class")
def webm_filepath(assets_dir):
    return os.path.join(assets_dir, "tmp.webm")


@pytest.fixture(scope="class", autouse=True)
def cleanup(mp3_filepath, webm_filepath):
    yield  # This makes sure the cleanup happens after tests run
    if os.path.exists(mp3_filepath):
        os.remove(mp3_filepath)
    if os.path.exists(webm_filepath):
        os.remove(webm_filepath)


def test_shazam_find_track_info(assets_dir):
    shazam_out = asyncio.run(shazam_find_track_info(assets_dir + "/example_0.mp3"))
    print(shazam_out["track"]["images"]["coverarthq"])
    assert shazam_out["track"]["subtitle"].upper() == "RED HOT CHILI PEPPERS"
    assert shazam_out["track"]["title"] == "Scar Tissue"
    assert shazam_out["track"]["sections"][0]["metadata"][0]["text"] == "Californication (Deluxe Edition)"
    assert shazam_out["track"]["genres"]["primary"] == "Alternative"
    assert shazam_out["track"]["sections"][0]["metadata"][2]["text"] == "1999"
    assert urllib.request.urlopen(shazam_out["track"]["images"]["coverarthq"]).status == 200  # OK


def test_get_youtube_audiostreams(best_audiostream, audiostreams):
    assert max([float(a.bitrate.replace("k", "e3")) for a in audiostreams]) == float(
        best_audiostream.bitrate.replace("k", "e3")
    )
    assert best_audiostream.extension == "webm"
    print(best_audiostream.filename)
    assert best_audiostream.filename == "15 Seconds.webm"
    assert best_audiostream.bitrate == "132.155k"
    assert best_audiostream.get_filesize() == 248138


def test_download_youtube_audiostream(best_audiostream, webm_filepath):
    download_youtube_audiostream(best_audiostream, save_filepath=webm_filepath)
    assert os.path.exists(webm_filepath)


def test_convert2mp3(assets_dir, best_audiostream, mp3_filepath, webm_filepath):
    shutil.copy(os.path.join(assets_dir, "example.webm"), webm_filepath)
    convert2mp3(webm_filepath, best_audiostream.extension)
    assert os.path.exists(mp3_filepath)
    assert not os.path.exists(webm_filepath)


def test_update_app():
    status = update_app()
    assert status == "mp3-autotagger updated successfully!"
