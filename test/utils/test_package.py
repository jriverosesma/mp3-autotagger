import pytest

from mp3_autotagger.utils.package import is_running_as_pyinstaller_bundle


def test_is_running_as_pyinstaller_bundle() -> None:
    assert not is_running_as_pyinstaller_bundle()
