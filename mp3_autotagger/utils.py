import os
import subprocess
import sys

from pydub import AudioSegment as convert
from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon, QPixmap
from pytube import YouTube
from shazamio import Shazam

shazam = Shazam()


async def shazam_find_track_info(filepath):
    return await shazam.recognize_song(filepath)


def convert2mp3(filepath, original_extension, save_filepath=None, remove_old_audio=True):
    track = convert.from_file(filepath, format=original_extension)
    save_filepath = save_filepath if save_filepath else os.path.splitext(filepath)[0] + ".mp3"
    track.export(save_filepath, format="mp3", id3v2_version="3")  # Version 3 to display cover in WIN explorer
    if remove_old_audio:
        os.remove(filepath)


def get_youtube_audiostreams(url, get_best_audio=False):
    video = YouTube(url)

    return video.getbestaudio() if get_best_audio else video.audiostreams


def download_youtube_audiostream(audiostream, save_filepath=None, quiet=True, callback=None):
    if save_filepath:
        audiostream.download(save_filepath if save_filepath else None, quiet=quiet, callback=callback)
    else:
        audiostream.download()


def update_app(package_name="mp3-autotagger"):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
    except subprocess.CalledProcessError as e:
        return f"Error occurred while updating {package_name}. Error: {e}"
    else:
        return f"{package_name} updated successfully!"


def qt_get_open_files_and_dirs(parent=None, caption="", directory="", filter="", initialFilter="", options=None):
    _translate = QtCore.QCoreApplication.translate

    def updateText():
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append(index.data())
        lineEdit.setText(_translate("Main Window", " ".join(selected)))

    dialog = qtw.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    dialog.accept = lambda: qtw.QDialog.accept(dialog)

    stackedWidget = dialog.findChild(qtw.QStackedWidget)
    view = stackedWidget.findChild(qtw.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(qtw.QLineEdit)
    dialog.directoryEntered.connect(lambda: lineEdit.setText(_translate("Main Window", "")))

    result = dialog.exec_()
    if result:
        return dialog.selectedFiles()


def qt_get_about_widget():
    about_message_box = qtw.QMessageBox()
    about_message_box.setWindowIcon(QIcon("assets/main_icon.png"))
    about_message_box.setIconPixmap(QPixmap("assets/main_icon.png").scaled(75, 75))

    return about_message_box
