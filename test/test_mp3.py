import io
import os
import shutil
import unittest

from mutagen.mp3 import HeaderNotFoundError
from PIL import Image

from mp3_autotagger.mp3 import MP3


class TestMP3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestMP3, cls).setUpClass()
        cls.media_dir = "media"
        cls.tmp_filepath = os.path.join(cls.media_dir, "tmp.mp3")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.tmp_filepath)

    # .mp3 with empty ID3 tags
    def test_example_0(self):
        shutil.copyfile(os.path.join(self.media_dir, "example_0.mp3"), self.tmp_filepath)
        track = MP3(self.tmp_filepath)
        track.update_tags_shazam()
        track.save_as(self.tmp_filepath)
        new_track = MP3(self.tmp_filepath)
        cover = Image.open(io.BytesIO(new_track.tags["APIC"]))
        tmp_cover_filepath = os.path.join(self.media_dir, "tmp_cover.png")
        cover.save(tmp_cover_filepath)

        assert new_track.tags["TPE1"] == "RED HOT CHILI PEPPERS"
        assert new_track.tags["TIT2"] == "Scar Tissue"
        assert new_track.tags["TALB"] == "Californication"
        assert new_track.tags["TCON"] == "Alternative"
        assert new_track.tags["TDRC"] == "1999"
        assert new_track.tags["APIC"] != b""
        assert os.path.exists(self.tmp_filepath)
        assert os.path.exists(tmp_cover_filepath)

        os.remove(tmp_cover_filepath)

    # .mp3 with filled ID3 tags (no replace)
    def test_example_1(self):
        shutil.copyfile(os.path.join(self.media_dir, "example_1.mp3"), self.tmp_filepath)
        track = MP3(self.tmp_filepath)
        assert track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
        assert track.tags["TIT2"] == "Suzie Q"
        assert track.tags["TALB"] == ""
        assert track.tags["TCON"] == "CLASICOS"
        assert track.tags["TDRC"] == "1968"
        assert track.tags["APIC"] != b""

        track.update_tags_shazam(replace_info=False)
        track.save_as(self.tmp_filepath)
        new_track = MP3(self.tmp_filepath)

        assert new_track.tags["TPE1"] == "CREEDENCE CLEARWATER REVIVAL"
        assert new_track.tags["TIT2"] == "Suzie Q"
        assert new_track.tags["TALB"] == "Creedence Clearwater Revival"
        assert new_track.tags["TCON"] == "CLASICOS"
        assert new_track.tags["TDRC"] == "1968"
        assert new_track.tags["APIC"] != b""
        assert os.path.exists(self.tmp_filepath)

    # Corrupted .mp3 file
    def test_example_2(self):
        shutil.copyfile(os.path.join(self.media_dir, "example_2.mp3"), self.tmp_filepath)
        with self.assertRaises(HeaderNotFoundError):
            MP3(self.tmp_filepath)


if __name__ == "__main__":
    unittest.main()
