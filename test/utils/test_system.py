from mp3_autotagger.utils.system import is_ffmpeg_installed


def test_ffmpeg_installed(mocker):
    """
    Test if ffmpeg is detected as installed.
    """
    mocker.patch("subprocess.run", return_value=mocker.Mock(returncode=0))
    assert is_ffmpeg_installed()


def test_ffmpeg_not_installed(mocker):
    """
    Test if ffmpeg is detected as not installed.
    """
    mocker.patch("subprocess.run", side_effect=FileNotFoundError)
    assert not is_ffmpeg_installed()
