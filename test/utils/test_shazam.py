import asyncio
from pathlib import Path

import pytest
import validators

from mp3_autotagger.utils.shazam import shazam_find_track_info


@pytest.fixture(scope="class")
def assets_dirpath() -> Path:
    return Path("test/assets")


def test_shazam_find_track_info(assets_dirpath: Path) -> None:
    shazam_out = asyncio.run(shazam_find_track_info(assets_dirpath / "example_0.mp3"))
    cover_url = shazam_out["track"]["images"]["coverarthq"]

    assert shazam_out["track"]["subtitle"].upper() == "RED HOT CHILI PEPPERS"
    assert shazam_out["track"]["title"] == "Scar Tissue"
    assert shazam_out["track"]["sections"][0]["metadata"][0]["text"] == "Californication (Remastered)"
    assert shazam_out["track"]["genres"]["primary"] == "Alternative"
    assert shazam_out["track"]["sections"][0]["metadata"][2]["text"] == "1999"
    assert isinstance(cover_url, str) and validators.url(cover_url)
