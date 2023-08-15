import asyncio
import os
import shutil
import unittest
import urllib

from git.cmd import Git

from mp3_autotagger.utils import (
    convert2mp3,
    download_youtube_audiostream,
    get_youtube_audiostreams,
    shazam_find_track_info,
)


class TestUtilsShazam(unittest.TestCase):
    def test_shazam_find_track_info(self):
        shazam_out = asyncio.run(shazam_find_track_info("media/example_0.mp3"))
        print(shazam_out["track"]["images"]["coverarthq"])
        assert shazam_out["track"]["subtitle"].upper() == "RED HOT CHILI PEPPERS"
        assert shazam_out["track"]["title"] == "Scar Tissue"
        assert shazam_out["track"]["sections"][0]["metadata"][0]["text"] == "Californication"
        assert shazam_out["track"]["genres"]["primary"] == "Alternative"
        assert shazam_out["track"]["sections"][0]["metadata"][2]["text"] == "1999"
        assert urllib.request.urlopen(shazam_out["track"]["images"]["coverarthq"]).status == 200  # OK


class TestUtilsYoutube(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestUtilsYoutube, cls).setUpClass()
        cls.media_dir = "media"
        cls.best_audiostream = get_youtube_audiostreams(
            "https://www.youtube.com/watch?v=HHjSdy9l7Kc", get_best_audio=True
        )
        cls.audiostreams = get_youtube_audiostreams("https://www.youtube.com/watch?v=HHjSdy9l7Kc")
        cls.mp3_filepath = os.path.join(cls.media_dir, "tmp.mp3")
        cls.webm_filepath = os.path.join(cls.media_dir, "tmp.webm")

    @classmethod
    def tearDownClass(cls):
        super(TestUtilsYoutube, cls).setUpClass()
        os.remove(cls.mp3_filepath)
        os.remove(cls.webm_filepath)

    def test_get_youtube_audiostreams(self):
        assert max([float(a.bitrate.replace("k", "e3")) for a in self.audiostreams]) == float(
            self.best_audiostream.bitrate.replace("k", "e3")
        )
        assert self.best_audiostream.extension == "webm"
        print(self.best_audiostream.filename)
        assert self.best_audiostream.filename == "15 Seconds.webm"
        assert self.best_audiostream.bitrate == "132.155k"
        assert self.best_audiostream.get_filesize() == 248138

    def test_download_youtube_audiostream(self):
        download_youtube_audiostream(self.best_audiostream, save_filepath=self.webm_filepath)
        assert os.path.exists(self.webm_filepath)

    def test_convert2mp3(self):
        shutil.copy(os.path.join(self.media_dir, "example.webm"), self.webm_filepath)
        convert2mp3(self.webm_filepath, self.best_audiostream.extension)
        assert os.path.exists(self.mp3_filepath)
        assert not os.path.exists(self.webm_filepath)


class TestUtilsUpdate(unittest.TestCase):
    def test_update_app(self):
        status = Git().fetch("https://github.com/jriverosesma/mp3-autotagger", "main")
        assert status is not None


if __name__ == "__main__":
    unittest.main()
