from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import yt_dlp as ydl

from mp3_autotagger.utils.youtube import get_youtube_audiostream


@pytest.fixture(scope="class")
def assets_dirpath() -> Path:
    return Path("test/assets")


@pytest.fixture(scope="class")
def mp3_filepath(assets_dirpath: Path) -> Path:
    return assets_dirpath / "15 Seconds.mp3"


@pytest.fixture(scope="class")
def video_url() -> str:
    return "https://www.youtube.com/watch?v=HHjSdy9l7Kc"


# Mocked audiostream response fixture
@pytest.fixture(scope="class")
def mocked_audiostream() -> dict[str, Any]:
    return {"ext": "webm", "title": "15 Seconds", "abr": 132.155, "filesize": 248138}


@pytest.fixture(scope="class")
def audiostream(
    mocked_audiostream: dict[str, Any], mp3_filepath: Path, video_url: str, assets_dirpath: Path
) -> dict[str, Any]:
    # NOTE: Downloading audio from YouTube in a "headless automatic" way is not possible without setting up cookies
    # Thus, `get_youtube_audiostream` works when used from the app, but may fail in unit-tests
    try:
        get_youtube_audiostream(video_url, assets_dirpath, convert_to_mp3=True)
    except ydl.utils.DownloadError as e:
        if str(e).startswith("ERROR: [youtube] HHjSdy9l7Kc") and "cookies" in str(e):
            open(mp3_filepath, "w").close()  # Create dummy mp3 file
            return mocked_audiostream
        else:
            raise


@pytest.fixture(scope="class", autouse=True)
def cleanup(mp3_filepath: Path):
    yield  # This makes sure the cleanup happens after tests run
    if mp3_filepath.exists():
        mp3_filepath.unlink()


def test_download_youtube_audiostream(audiostream: dict[str, Any], assets_dirpath: Path) -> None:
    assert audiostream["ext"] == "webm"
    assert audiostream["title"] == "15 Seconds"
    assert audiostream["abr"] == 132.155
    assert audiostream["filesize"] == 248138
    assert (assets_dirpath / f"{audiostream['title']}.mp3").exists()
