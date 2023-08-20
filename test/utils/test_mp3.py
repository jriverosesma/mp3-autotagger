import io
import shutil
from pathlib import Path

import pytest
from mutagen.mp3 import HeaderNotFoundError
from PIL import Image

from mp3_autotagger.utils.mp3 import MP3


@pytest.fixture(scope="class")
def setup_class_data() -> tuple[Path, Path]:
    assets_dirpath = Path("test/assets")
    tmp_filepath = assets_dirpath / "tmp.mp3"
    yield assets_dirpath, tmp_filepath
    tmp_filepath.unlink()


def test_example_0(setup_class_data: tuple[Path, Path]) -> None:
    assets_dirpath, tmp_filepath = setup_class_data
    shutil.copyfile(assets_dirpath / "example_0.mp3", tmp_filepath)
    track = MP3(tmp_filepath)
    track.tags["TPE1"] = "RED-HOT-CHILI-PEPPERS"
    track.update_tags_shazam(replace_existing_tags=True)
    track.save_as(tmp_filepath)
    new_track = MP3(tmp_filepath)
    cover = Image.open(io.BytesIO(new_track.tags["APIC"]))
    tmp_cover_filepath = assets_dirpath / "tmp_cover.png"
    cover.save(tmp_cover_filepath)

    assert new_track.tags["TPE1"] == "RED HOT CHILI PEPPERS"
    assert new_track.tags["TIT2"] == "Scar Tissue"
    assert new_track.tags["TALB"] == "Californication (Remastered)"
    assert new_track.tags["TCON"] == "Alternative"
    assert new_track.tags["TDRC"] == "1999"
    assert new_track.tags["APIC"] != b""
    assert tmp_filepath.exists()
    assert tmp_cover_filepath.exists()

    tmp_cover_filepath.unlink()


def test_example_1(setup_class_data: tuple[Path, Path]) -> None:
    assets_dirpath, tmp_filepath = setup_class_data
    shutil.copyfile(assets_dirpath / "example_1.mp3", tmp_filepath)
    track = MP3(tmp_filepath)
    assert track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
    assert track.tags["TIT2"] == "Suzie Q"
    assert track.tags["TALB"] == ""
    assert track.tags["TCON"] == "CLASICOS"
    assert track.tags["TDRC"] == "1968"
    assert track.tags["APIC"] != b""

    track.update_tags_shazam()
    track.save_as(tmp_filepath)
    new_track = MP3(tmp_filepath)

    assert new_track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
    assert new_track.tags["TIT2"] == "Suzie Q"
    assert new_track.tags["TALB"] == "Creedence Clearwater Revival"
    assert new_track.tags["TCON"] == "CLASICOS"
    assert new_track.tags["TDRC"] == "1968"
    assert new_track.tags["APIC"] != b""
    assert tmp_filepath.exists()


def test_example_2(setup_class_data: tuple[Path, Path]) -> None:
    assets_dirpath, tmp_filepath = setup_class_data
    shutil.copyfile(assets_dirpath / "example_2.mp3", tmp_filepath)
    with pytest.raises(HeaderNotFoundError):
        MP3(tmp_filepath)
