import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import yt_dlp as ydl
from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon, QPixmap
from shazamio import Shazam

shazam = Shazam()


class MP3AutotaggerException(Exception):
    pass


async def shazam_find_track_info(filepath: Path) -> dict[str, Any]:
    return await shazam.recognize_song(filepath)


def get_youtube_audiostream(
    url: str,
    save_dirpath: Path = Path("."),
    download: bool = True,
    quiet: bool = True,
    callback: Callable | None = None,
) -> dict[str, Any] | None:
    ydl_opts = {
        "quiet": quiet,
        "format": "bestaudio/best",
        "noplaylist": True,
        "progress_hooks": [callback] if callback else [],
        "outtmpl": str(save_dirpath / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    with ydl.YoutubeDL(ydl_opts) as y:
        info = y.extract_info(url, download=download)

    return info


def get_package_version(package_name: str) -> str | None:
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        for line in output.decode().splitlines():
            if line.startswith("Version:"):
                return line.split(": ")[1]
    except subprocess.CalledProcessError:
        return None


def update_package(package_name: str = "mp3-autotagger") -> str:
    initial_version = get_package_version(package_name)
    if not initial_version:
        return f"Error: Unable to determine the current version of {package_name}."

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
    except subprocess.CalledProcessError as e:
        return f"Error occurred while updating {package_name}. Error: {e}"

    updated_version = get_package_version(package_name)
    if not updated_version:
        return f"Error: Unable to determine the updated version of {package_name}."

    if initial_version == updated_version:
        return f"{package_name} is already at the latest version ({updated_version})."

    return f"{package_name} updated successfully from version {initial_version} to {updated_version}!"


def qt_get_open_files_and_dirs(
    parent: qtw.QWidget | None = None,
    caption: str = "",
    directory: str = "",
    filter: str = "",
    initialFilter: str = "",
    options: tuple[qtw.QFileDialog.Options, qtw.QFileDialog.Option] | None = None,
) -> list[str]:
    _translate = QtCore.QCoreApplication.translate

    def updateText():
        selected = [index.data() for index in view.selectionModel().selectedRows()]
        lineEdit.setText(_translate("Main Window", " ".join(selected)))

    dialog = qtw.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    dialog.setOptions(*options or ())
    dialog.setOption(dialog.DontUseNativeDialog, True)
    dialog.setDirectory(directory)
    dialog.setNameFilter(filter)
    if initialFilter:
        dialog.selectNameFilter(initialFilter)

    dialog.accept = lambda: qtw.QDialog.accept(dialog)

    stackedWidget = dialog.findChild(qtw.QStackedWidget)
    view = stackedWidget.findChild(qtw.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(qtw.QLineEdit)
    dialog.directoryEntered.connect(lambda: lineEdit.setText(_translate("Main Window", "")))

    return dialog.selectedFiles() if dialog.exec_() else []


def qt_get_about_widget() -> qtw.QMessageBox:
    about_message_box = qtw.QMessageBox()
    about_message_box.setWindowIcon(QIcon("assets/main_icon.png"))
    about_message_box.setIconPixmap(QPixmap("assets/main_icon.png").scaled(75, 75))

    return about_message_box
