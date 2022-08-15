import os
import pafy

from PyQt5 import QtWidgets as qtw
from pydub import AudioSegment as convert
from shazamio import Shazam
from git.cmd import Git


shazam = Shazam()

async def shazam_find_track_info(filepath):
            
            return await shazam.recognize_song(filepath)


def convert2mp3(filepath, original_extension, save_filepath=None, remove_old_audio=True):
    track = convert.from_file(filepath, format=original_extension)
    save_filepath = save_filepath if save_filepath else os.path.splitext(filepath)[0] + '.mp3'
    track.export(save_filepath, format='mp3', id3v2_version='3') # Version 3 to display cover in WIN explorer
    if remove_old_audio:
        os.remove(filepath)

    
def get_youtube_audiostreams(url, get_best_audio=False):
    video = pafy.new(url)

    return video.getbestaudio() if get_best_audio else video.audiostreams


def download_youtube_audiostream(audiostream, save_filepath=None, quiet=True, callback=None):
    if save_filepath:
        audiostream.download(save_filepath if save_filepath else None, quiet=quiet, callback=callback)
    else:
        audiostream.download()


def update_app_git():
    status = Git().pull('https://github.com/jriverosesma/mp3-autotagger','main')

    return status


def get_open_files_and_dirs(parent=None, caption='', directory='', filter='', initialFilter='', options=None):

    def updateText():
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append(index.data())
        lineEdit.setText(' '.join(selected))

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
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

    result = dialog.exec_()
    if result:
        return dialog.selectedFiles()
