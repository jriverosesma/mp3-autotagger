import io
import os
import shutil

import pytest
from mutagen.mp3 import HeaderNotFoundError
from PIL import Image

from mp3_autotagger.mp3 import MP3


@pytest.fixture(scope="class")
def setup_class_data():
    media_dir = "test/assets"
    tmp_filepath = os.path.join(media_dir, "tmp.mp3")
    yield media_dir, tmp_filepath
    os.remove(tmp_filepath)


def test_example_0(setup_class_data):
    media_dir, tmp_filepath = setup_class_data
    shutil.copyfile(os.path.join(media_dir, "example_0.mp3"), tmp_filepath)
    track = MP3(tmp_filepath)
    track.update_tags_shazam()
    track.save_as(tmp_filepath)
    new_track = MP3(tmp_filepath)
    cover = Image.open(io.BytesIO(new_track.tags["APIC"]))
    tmp_cover_filepath = os.path.join(media_dir, "tmp_cover.png")
    cover.save(tmp_cover_filepath)

    assert new_track.tags["TPE1"] == "RED HOT CHILI PEPPERS"
    shutil.copyfile(os.path.join(media_dir, "example_0.mp3"), tmp_filepath)
    track = MP3(tmp_filepath)
    track.update_tags_shazam()
    track.save_as(tmp_filepath)
    new_track = MP3(tmp_filepath)
    cover = Image.open(io.BytesIO(new_track.tags["APIC"]))
    tmp_cover_filepath = os.path.join(media_dir, "tmp_cover.png")
    cover.save(tmp_cover_filepath)

    assert new_track.tags["TPE1"] == "RED HOT CHILI PEPPERS"
    assert new_track.tags["TIT2"] == "Scar Tissue"
    assert new_track.tags["TALB"] == "Californication (Deluxe Edition)"
    assert new_track.tags["TCON"] == "Alternative"
    assert new_track.tags["TDRC"] == "1999"
    assert new_track.tags["APIC"] != b""
    assert os.path.exists(tmp_filepath)
    assert os.path.exists(tmp_cover_filepath)

    os.remove(tmp_cover_filepath)


def test_example_1(setup_class_data):
    media_dir, tmp_filepath = setup_class_data
    shutil.copyfile(os.path.join(media_dir, "example_1.mp3"), tmp_filepath)
    track = MP3(tmp_filepath)
    assert track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
    assert track.tags["TIT2"] == "Suzie Q"
    assert track.tags["TALB"] == ""
    assert track.tags["TCON"] == "CLASICOS"
    assert track.tags["TDRC"] == "1968"
    assert track.tags["APIC"] != b""

    track.update_tags_shazam(replace_info=False)
    track.save_as(tmp_filepath)
    new_track = MP3(tmp_filepath)

    assert new_track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
    assert new_track.tags["TIT2"] == "Suzie Q"
    assert new_track.tags["TALB"] == "Creedence Clearwater Revival"
    assert new_track.tags["TCON"] == "CLASICOS"
    assert new_track.tags["TDRC"] == "1968"
    assert new_track.tags["APIC"] != b""
    assert os.path.exists(tmp_filepath)


def test_example_2(setup_class_data):
    media_dir, tmp_filepath = setup_class_data
    shutil.copyfile(os.path.join(media_dir, "example_2.mp3"), tmp_filepath)
    with pytest.raises(HeaderNotFoundError):
        MP3(tmp_filepath)
