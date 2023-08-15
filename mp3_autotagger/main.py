import io
import os
import sys
from datetime import datetime
from pathlib import Path
from threading import Thread

from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QPixmap

from mp3_autotagger.exceptions import MP3AutotaggerError
from mp3_autotagger.mp3 import MP3
from mp3_autotagger.ui_main_window import Ui_MainWindow
from mp3_autotagger.utils import (
    convert2mp3,
    download_youtube_audiostream,
    get_youtube_audiostreams,
    qt_get_about_widget,
    qt_get_open_files_and_dirs,
    update_app_git,
)


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    # Autotagger
    progressBar_find_save_all_tags_signal = QtCore.pyqtSignal(int)

    # Youtube2MP3
    label_yt_status_signal = QtCore.pyqtSignal(str)
    progressBar_download_signal = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Autotagger
        self.mp3_filepaths = []
        self.log_folder = str(os.path.join(Path(__file__).parent.resolve(), "../logs"))
        self.current_track = None
        self.cover_bytes = None

        # Youtube2MP3
        self.download_folder = str(os.path.join(Path.home(), "Downloads"))

        # Main window
        self._translate = QtCore.QCoreApplication.translate
        self.trans = QtCore.QTranslator(self)
        self._set_app_scale()
        self._connect_signals_slots()

    def _set_app_scale(self):
        current_screen_size = qtw.qApp.primaryScreen().geometry()
        original_screen_size = (1920, 1080)  # (width, height)
        original_window_size = self.size()

        # Compute ratios
        width_ratio = current_screen_size.width() / original_screen_size[0]
        height_ratio = current_screen_size.height() / original_screen_size[1]

        # Resize main window
        self.resize(int(original_window_size.width() * width_ratio), int(original_window_size.height() * height_ratio))

        # Set new maximum size constraints for cover label
        self.label_cover.setMinimumWidth(int(self.checkBox_replace_info.width()))
        self.label_cover.setMinimumHeight(int(self.checkBox_replace_info.width()))
        self.label_cover.setMaximumWidth(int(width_ratio * self.label_cover.maximumWidth()))
        self.label_cover.setMaximumHeight(int(height_ratio * self.label_cover.maximumHeight()))

    def _connect_signals_slots(self):
        # Main window
        self.actionAbout.triggered.connect(self.show_about)
        self.actionEnglish.triggered.connect(self.language_english)
        self.actionSpanish.triggered.connect(self.language_spanish)
        self.actionUpdates.triggered.connect(self.update_app)

        # Autotagger
        self.pushButton_browse.pressed.connect(self.browse_mp3)
        self.pushButton_find_tags.pressed.connect(self.find_tags)
        self.pushButton_save_tags.pressed.connect(self.save_tags)
        self.pushButton_find_save_all_tags.pressed.connect(self.find_save_all_tags)
        self.label_cover.mousePressEvent = self.manually_add_cover
        self.listWidget_tracks.itemClicked.connect(self.track_clicked)

        # Youtube2MP3
        self.pushButton_get_audio_info.pressed.connect(self.get_yt_audio_info)
        self.pushButton_download.pressed.connect(self.download_yt_audio)
        self.progressBar_download_signal.connect(self.progressBar_download.setValue)
        self.label_yt_status_signal.connect(self.label_yt_status.setText)

    def _retranslate(self, qm_filepath=None):
        if qm_filepath:
            self.trans.load(qm_filepath)
            qtw.QApplication.instance().installTranslator(self.trans)
        else:
            qtw.QApplication.instance().removeTranslator(self.trans)
        self.retranslateUi(self)

    # Main window
    def show_about(self):
        about_message_box = qt_get_about_widget()
        about_message_box.setWindowTitle(self._translate("About Window", "About MP3 Autotagger"))
        about_message_box.setText(
            self._translate(
                "About Window",
                "<p>An application for MP3 autotagging and more.</p>"
                '<p>GitHub: <a href="https://github.com/jriverosesma/mp3-autotagger">mp3-autotagger</a></p>'
                '<p>Email: <a href="mailto:jriverosesma@gmail.com">jriverosesma@gmail.com</a></p>',
            )
        )
        about_message_box.exec()

    # Main window
    def show_info_message(self, message_md, title="Info"):
        qtw.QMessageBox.information(self, title, message_md)

    # Main window
    def show_error_message(self, message_md="Unknown Error", title="Error"):
        qtw.QMessageBox.critical(self, f"{title}", message_md)

    # Main window
    def update_app(self):
        try:
            status = update_app_git()
            if status == "Already up to date.":
                self.show_info_message(self._translate("Update App Window", "No new updates available", title="Update"))
            else:
                self.show_info_message(
                    self._translate(
                        "Update App Window",
                        "<p>Updated successfully!</p>" "<p>Restart application for changes to take effect</p>",
                        title="Update",
                    )
                )
        except MP3AutotaggerError("Update failed"):
            self.show_error_message(message_md="Update failed!", title="Update")

    # Main window
    def language_english(self):
        self._retranslate()

    # Main window
    def language_spanish(self):
        self._retranslate("translations/eng-es.qm")

    # Autotagger
    def track_clicked(self, item):
        self.load_mp3(self.mp3_filepaths[self.listWidget_tracks.currentRow()])
        if self.current_track:
            self.set_track_info()

    # Autotagger
    def browse_mp3(self, filepath=None):
        if filepath:
            selected_files_mp3 = filepath
        else:
            selected_files_mp3 = qt_get_open_files_and_dirs(
                caption="Select directory or .mp3", filter="All files (*)\nMP3 files (*.mp3)"
            )

        if selected_files_mp3:
            self.listWidget_tracks.clear()
            self.mp3_filepaths = []
            self.lineEdit_mp3_dir.setText(self._translate("Main Window", str(selected_files_mp3)))

            for selected_file in selected_files_mp3:
                self.mp3_filepaths += self.find_all_mp3(selected_file)

            if self.mp3_filepaths:
                self.load_mp3(self.mp3_filepaths[0])
                if self.current_track:
                    self.set_track_info()
                    self.listWidget_tracks.setCurrentRow(0)

            for i, filepath in enumerate(self.mp3_filepaths):
                self.listWidget_tracks.addItem(f"{i+1}. {os.path.basename(filepath)}")
            self.label_mp3_count.setText(self._translate("Main Window", f"{len(self.mp3_filepaths)} .mp3 files found"))

    # Autotagger
    def unset_track_info(self):
        self.current_track = None

        self.lineEdit_artist.clear()
        self.lineEdit_title.clear()
        self.lineEdit_album.clear()
        self.lineEdit_genre.clear()
        self.lineEdit_year.clear()
        self.label_cover.clear()

        self.lineEdit_artist.setEnabled(False)
        self.lineEdit_title.setEnabled(False)
        self.lineEdit_album.setEnabled(False)
        self.lineEdit_genre.setEnabled(False)
        self.lineEdit_year.setEnabled(False)
        self.label_cover.setEnabled(False)

        self.pushButton_find_tags.setEnabled(False)
        self.pushButton_save_tags.setEnabled(False)

    # Autotagger
    def set_cover(self):
        cover = QPixmap()
        cover.loadFromData(io.BytesIO(self.cover_bytes).read())
        self.label_cover.setPixmap(cover)

    # Autotagger
    def set_track_info(self):
        self.lineEdit_artist.setText(self._translate("Main Window", self.current_track.tags["TPE1"]))
        self.lineEdit_title.setText(self._translate("Main Window", self.current_track.tags["TIT2"]))
        self.lineEdit_album.setText(self._translate("Main Window", self.current_track.tags["TALB"]))
        self.lineEdit_genre.setText(self._translate("Main Window", self.current_track.tags["TCON"]))
        self.lineEdit_year.setText(self._translate("Main Window", self.current_track.tags["TDRC"]))
        if self.current_track.tags["APIC"]:
            self.cover_bytes = self.current_track.tags["APIC"]
        else:
            with open("assets/no_cover.jpg", mode="rb") as f:
                self.cover_bytes = f.read()
        self.set_cover()

        self.lineEdit_artist.setEnabled(True)
        self.lineEdit_title.setEnabled(True)
        self.lineEdit_album.setEnabled(True)
        self.lineEdit_genre.setEnabled(True)
        self.lineEdit_year.setEnabled(True)
        self.label_cover.setEnabled(True)

        self.pushButton_find_tags.setEnabled(True)
        self.pushButton_save_tags.setEnabled(True)
        self.pushButton_find_save_all_tags.setEnabled(True)

    # Autotagger
    def manually_add_cover(self, event):
        selected_cover = qtw.QFileDialog.getOpenFileName(
            self, "Select image", "", "Image files (*.png; *.jpg; *.jpeg; *.bmp; *.tif; *.tiff; *.eps)"
        )[0]
        if selected_cover:
            with open(selected_cover, mode="rb") as f:
                self.cover_bytes = f.read()
        self.set_cover()

    # Autotagger
    def find_all_mp3(self, find_path):
        filepaths = [find_path] if find_path.endswith(".mp3") else []
        for path, _, files in os.walk(find_path):
            filepaths.extend(
                [os.path.join(path, file).replace("\\", "/") for file in files if str(file).endswith(".mp3")]
            )

        return filepaths

    # Autotagger
    def load_mp3(self, filepath, raise_exception=False):
        try:
            self.current_track = MP3(filepath)
            self.label_autotagger_status.setText(self._translate("Main Window", ""))
        except MP3AutotaggerError("Unable to load .mp3"):
            self.unset_track_info()
            self.label_autotagger_status.setText(self._translate("Main Window", "Unable to load .mp3"))
            if raise_exception:
                raise

    # Autotagger
    def find_tags(self, thread_shazam=True, raise_exception=False):
        self.tabWidget.widget(0).setEnabled(False)

        try:
            if thread_shazam:
                thread_update_tags_shazam = Thread(
                    target=self.current_track.update_tags_shazam,
                    kwargs={"replace_info": self.checkBox_replace_info.isChecked()},
                )
                thread_update_tags_shazam.start()
                while thread_update_tags_shazam.is_alive():
                    qtw.QApplication.processEvents()
            else:
                self.current_track.update_tags_shazam(replace_info=self.checkBox_replace_info.isChecked())
            self.set_track_info()
        except MP3AutotaggerError("Unexpected error finding tags with Shazam"):
            self.label_autotagger_status.setText(
                self._translate("Main Window", "Unexpected error finding tags with Shazam")
            )
            if raise_exception:
                raise

        self.tabWidget.widget(0).setEnabled(True)

    # Autotagger
    def save_tags(self, new_filepath=None, raise_exception=False):
        try:
            self.current_track.tags["TPE1"] = self.lineEdit_artist.text()
            self.current_track.tags["TIT2"] = self.lineEdit_title.text()
            self.current_track.tags["TALB"] = self.lineEdit_album.text()
            self.current_track.tags["TCON"] = self.lineEdit_genre.text()
            self.current_track.tags["TDRC"] = self.lineEdit_year.text()
            self.current_track.tags["APIC"] = io.BytesIO(self.cover_bytes).read()
            self.current_track.save_as(new_filepath=new_filepath)

            self.mp3_filepaths[self.listWidget_tracks.currentRow()] = self.current_track.filepath
            self.listWidget_tracks.currentItem().setText(
                self._translate(
                    "Main Window",
                    f"{self.listWidget_tracks.currentRow()}. {os.path.basename(self.current_track.filepath)}",
                )
            )
            self.label_autotagger_status.setText(self._translate("Main Window", "Saved succesfully"))
        except MP3AutotaggerError("Unexpected error saving tags"):
            self.label_autotagger_status.setText(self._translate("Main Window", "Unexpected error saving tags"))
            if raise_exception:
                raise

    # Autotagger
    def find_save_all_tags(self):
        log_filepath = os.path.join(self.log_folder, f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        with open(log_filepath, "a") as log:
            n_files = len(self.mp3_filepaths)
            for i, filepath in enumerate(self.mp3_filepaths):
                self.listWidget_tracks.setCurrentRow(i)
                try:
                    self.load_mp3(filepath, raise_exception=True)
                    self.label_autotagger_status.setText(self._translate("Main Window", "Tagging files..."))
                    self.find_tags()
                    self.save_tags()
                    log.writelines({self.current_track.filepath + ": OK\n"})
                except MP3AutotaggerError(f"Error tagging file {filepath}"):
                    log.writelines({filepath + ": FAILED\n"})

                self.progressBar_find_save_all_tags.setValue(int((i + 1) / n_files * 100))

        self.label_autotagger_status.setText("Main Window", f"Done. Log saved to {log_filepath}")

        self.listWidget_tracks.unsetCursor()
        self.unset_track_info()

    # Youtube2MP3
    def get_yt_audio_info(self):
        self.label_yt_status.clear()
        self.lineEdit_video_title.clear()
        self.comboBox_audio_select.clear()

        try:
            get_best_audio = self.checkBox_get_bestaudio.isChecked()
            self.audiostreams = get_youtube_audiostreams(self.lineEdit_url.text(), get_best_audio=get_best_audio)
            if get_best_audio:
                self.audiostreams = [self.audiostreams]

            for aust in self.audiostreams:
                self.comboBox_audio_select.addItem(
                    f"{aust.extension} | {aust.bitrate} kbps | {round(aust.get_filesize() / 1e6, 2)} MB"
                )

            self.lineEdit_video_title.setText(self._translate("Main Window", self.audiostreams[0].title))
            self.comboBox_audio_select.setEnabled(True)
            self.pushButton_download.setEnabled(True)
            self.label_yt_status.setText(self._translate("Main Window", "Ready to download"))

        except ValueError:
            self.label_yt_status.setText(self._translate("Main Window", "Bad URL"))
            self.comboBox_audio_select.setEnabled(False)
            self.pushButton_download.setEnabled(False)

        except MP3AutotaggerError("Unexpected error"):
            self.label_yt_status.setText(self._translate("Main Window", "Unexpected Error"))
            self.comboBox_audio_select.setEnabled(False)
            self.pushButton_download.setEnabled(False)

    # Youtube2MP3
    def callback_download_yt(self, total, recvd, ratio, rate, eta):
        self.label_yt_status_signal.emit(f"Downloading... [{round(rate)} KB/s, ETA: {eta} s]")
        self.progressBar_download_signal.emit(int(ratio * 100))

    # Youtube2MP3
    def download_yt_audio(self):
        self.tabWidget.widget(1).setEnabled(False)

        selected_audiostream = self.audiostreams[self.comboBox_audio_select.currentIndex()]

        error_text = None
        try:
            thread_download_youtube = Thread(
                target=download_youtube_audiostream,
                args=(selected_audiostream, self.download_folder),
                kwargs={"callback": self.callback_download_yt},
            )
            thread_download_youtube.start()
        except MP3AutotaggerError("Error downloading audio"):
            error_text = "Error Downloading"

        while thread_download_youtube.is_alive():
            qtw.QApplication.processEvents()

        if self.checkBox_convert_audio_to_mp3.isChecked() and not error_text:
            self.label_yt_status.setText(
                self._translate("Main Window", "Download successful! Converting audio to .mp3...")
            )
            filepath = os.path.join(self.download_folder, selected_audiostream.filename)
            try:
                thread_convert2mp3 = Thread(target=convert2mp3, args=(filepath, selected_audiostream.extension))
                thread_convert2mp3.start()
                while thread_convert2mp3.is_alive():
                    qtw.QApplication.processEvents()
            except MP3AutotaggerError("Unexpected error converting audio to .mp3"):
                if not error_text:
                    error_text = "Unexpected error converting audio to .mp3"

        if error_text:
            self.label_yt_status.setText(self._translate("Main Window", error_text))
        else:
            self.label_yt_status.setText(self._translate("Main Window", "Success!"))

        self.tabWidget.widget(1).setEnabled(True)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")

    main_window = MainWindow()
    main_window.show()
    main_window.label_cover.setMinimumHeight(0)  # Reset cover minimum height after showing main window

    sys.exit(app.exec_())
