from pathlib import Path
from typing import Any

import pytest

from mp3_autotagger.utils.youtube import get_youtube_audiostream


@pytest.fixture(scope="class")
def assets_dirpath() -> Path:
    return Path("test/assets")


@pytest.fixture(scope="class")
def mp3_filepath(assets_dirpath: Path) -> Path:
    return assets_dirpath / "tmp.mp3"


@pytest.fixture(scope="class")
def video_url() -> str:
    return "https://www.youtube.com/watch?v=HHjSdy9l7Kc"


@pytest.fixture(scope="class")
def audiostream(video_url: str, assets_dirpath: Path) -> dict[str, Any]:
    return get_youtube_audiostream(video_url, assets_dirpath, convert_to_mp3=True)


@pytest.fixture(scope="class", autouse=True)
def cleanup(mp3_filepath: Path, assets_dirpath: Path) -> None:
    yield  # This makes sure the cleanup happens after tests run
    if mp3_filepath.exists():
        mp3_filepath.unlink()
    if (assets_dirpath / "15 Seconds.mp3").exists():
        (assets_dirpath / "15 Seconds.mp3").unlink()


def test_download_youtube_audiostream(audiostream: dict[str, Any], assets_dirpath: Path) -> None:
    assert audiostream["ext"] == "webm"
    assert audiostream["title"] == "15 Seconds"
    assert audiostream["abr"] == 132.155
    assert audiostream["filesize"] == 248138
    assert (assets_dirpath / f"{audiostream['title']}.mp3").exists()
