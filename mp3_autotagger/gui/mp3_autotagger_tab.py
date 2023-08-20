import io
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Thread

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QPixmap

from ..utils.assets import no_cover_path
from ..utils.mp3 import MP3
from ..utils.qt import qt_get_open_files_and_dirs


class MP3AutotaggerGUI:
    def __init__(self, gui) -> None:
        self._gui = gui
        self._mp3_filepaths: list[Path] = []
        self._current_track: MP3 | None = None
        self._cover_bytes: bytes | None = None
        self._log_folder: Path = Path.home() / "mp3-autotagger/logs"
        self._log_folder.mkdir(parents=True, exist_ok=True)

    def _load_cover(self):
        if self._current_track.tags["APIC"]:
            self._cover_bytes = self._current_track.tags["APIC"]
        else:
            with open(no_cover_path, mode="rb") as f:
                self._cover_bytes = f.read()
        self._set_cover()

    def _set_cover(self) -> None:
        cover = QPixmap()
        cover.loadFromData(io.BytesIO(self._cover_bytes).read())
        self._gui.label_cover.setPixmap(cover)

    def track_clicked(self, item) -> None:
        self._load_mp3(self._mp3_filepaths[self._gui.listWidget_tracks.currentRow()])
        if self._current_track:
            self._set_track_info()

    def browse_mp3(self) -> None:
        selected_files_mp3 = qt_get_open_files_and_dirs(
            caption="Select directory or .mp3", filter="All files (*)\nMP3 files (*.mp3)"
        )

        if not selected_files_mp3:
            return

        self._mp3_filepaths = []
        for selected_file in selected_files_mp3:
            self._mp3_filepaths += self._find_all_mp3(Path(selected_file))

        if self._mp3_filepaths:
            self._gui.pushButton_find_and_save_all_tags.setEnabled(True)
            self._populate_mp3_list(selected_files_mp3)

        if self._current_track:
            self._unset_track_info()

        self._gui.progressBar_find_and_save_all_tags.setValue(0)

    def _populate_mp3_list(self, selected_files_mp3):
        self._gui.listWidget_tracks.clear()
        self._gui.lineEdit_mp3_dir.setText(self._gui.translate("Main Window", str(selected_files_mp3)))

        for filepath in self._mp3_filepaths:
            self._gui.listWidget_tracks.addItem(filepath.stem)
        self._gui.label_mp3_count.setText(
            self._gui.translate("Main Window", f"{len(self._mp3_filepaths)} .mp3 files found")
        )

    def _set_widget_text(self, widget, tag_key):
        widget.setText(self._gui.translate("Main Window", self._current_track.tags[tag_key]))

    def _unset_track_info(self) -> None:
        widgets_to_clear = [
            self._gui.lineEdit_artist,
            self._gui.lineEdit_title,
            self._gui.lineEdit_album,
            self._gui.lineEdit_genre,
            self._gui.lineEdit_year,
            self._gui.label_cover,
        ]
        for widget in widgets_to_clear:
            widget.clear()
            widget.setEnabled(False)

        self._gui.pushButton_find_tags.setEnabled(False)
        self._gui.pushButton_save_tags.setEnabled(False)

    def _set_track_info(self) -> None:
        tags_and_widgets = {
            "TPE1": self._gui.lineEdit_artist,
            "TIT2": self._gui.lineEdit_title,
            "TALB": self._gui.lineEdit_album,
            "TCON": self._gui.lineEdit_genre,
            "TDRC": self._gui.lineEdit_year,
        }
        for tag_key, widget in tags_and_widgets.items():
            self._set_widget_text(widget, tag_key)

        self._load_cover()

        for widget in tags_and_widgets.values():
            widget.setEnabled(True)

        self._gui.label_cover.setEnabled(True)
        self._gui.pushButton_find_tags.setEnabled(True)
        self._gui.pushButton_save_tags.setEnabled(True)
        self._gui.pushButton_find_and_save_all_tags.setEnabled(True)

    def manually_add_cover(self, event) -> None:
        try:
            selected_cover = qtw.QFileDialog.getOpenFileName(
                self._gui, "Select image", "", "Image files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.eps)"
            )[0]
            if selected_cover:
                self._load_cover_from_path(selected_cover)
                self._set_cover()
        except Exception:
            self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", "Error adding new cover"))

    def _load_cover_from_path(self, path: str) -> None:
        with open(path, mode="rb") as f:
            self._cover_bytes = f.read()

    def _find_all_mp3(self, find_path: Path) -> list[Path]:
        if find_path.is_file() and find_path.suffix == ".mp3":
            return [find_path]

        return sorted([filepath for filepath in find_path.rglob("*.mp3")])

    def _load_mp3(self, filepath: Path, raise_exception: bool = False) -> None:
        try:
            self._current_track = MP3(filepath)
            self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", ""))
        except Exception:
            self._current_track = None
            self._unset_track_info()
            self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", "Unable to load .mp3"))
            if raise_exception:
                raise

    def find_tags(self, thread_shazam: bool = True, raise_exception: bool = False) -> None:
        self._gui.tabWidget.widget(0).setEnabled(False)
        try:
            success = self._shazam_update_tags(thread_shazam)
            if success:
                self._set_track_info()
            else:
                self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", "Song not found"))
                raise
        except Exception:
            self._gui.label_autotagger_status.setText(
                self._gui.translate("Main Window", "Unexpected error finding tags with Shazam")
            )
            if raise_exception:
                raise

        self._gui.tabWidget.widget(0).setEnabled(True)

    def _shazam_update_tags(self, thread_shazam: bool) -> bool:
        def worker(queue):
            result = self._current_track.update_tags_shazam()
            queue.put(result)

        if thread_shazam:
            q = Queue()
            thread_update_tags_shazam = Thread(target=worker, args=(q,))
            thread_update_tags_shazam.start()
            while thread_update_tags_shazam.is_alive():
                qtw.QApplication.processEvents()
            success = q.get()
        else:
            success = self._current_track.update_tags_shazam()

        return success

    def save_tags(self, raise_exception: bool = False) -> None:
        try:
            self._update_current_track_tags()

            new_filepath = self._current_track.filepath
            if self._gui.checkBox_rename_file.isChecked():
                artist = self._current_track.tags["TPE1"].upper()
                title = self._current_track.tags["TIT2"]
                if artist != "" and title != "":
                    new_filename = artist + " - " + title + ".mp3"
                new_filepath = self._current_track.filepath.parent / new_filename

            self._current_track.save_as(new_filepath=new_filepath)

            self._update_displayed_filepath()
            self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", "Saved succesfully"))
        except Exception:
            self._gui.label_autotagger_status.setText(
                self._gui.translate("Main Window", "Unexpected error saving tags")
            )
            if raise_exception:
                raise

    def _update_current_track_tags(self):
        self._current_track.tags["TPE1"] = self._gui.lineEdit_artist.text()
        self._current_track.tags["TIT2"] = self._gui.lineEdit_title.text()
        self._current_track.tags["TALB"] = self._gui.lineEdit_album.text()
        self._current_track.tags["TCON"] = self._gui.lineEdit_genre.text()
        self._current_track.tags["TDRC"] = self._gui.lineEdit_year.text()
        self._current_track.tags["APIC"] = io.BytesIO(self._cover_bytes).read()

    def _update_displayed_filepath(self):
        self._mp3_filepaths[self._gui.listWidget_tracks.currentRow()] = self._current_track.filepath
        self._gui.listWidget_tracks.currentItem().setText(
            self._gui.translate(
                "Main Window",
                self._current_track.filepath.stem,
            )
        )

    def find_and_save_all_tags(self) -> None:
        log_filepath = self._initialize_log()
        n_files = len(self._mp3_filepaths)

        for i, filepath in enumerate(self._mp3_filepaths):
            self._process_individual_file(i, filepath, log_filepath, n_files)

        self._gui.label_autotagger_status.setText(
            self._gui.translate("Main Window", f"Done. Log saved to {log_filepath}")
        )
        self._gui.listWidget_tracks.unsetCursor()
        self._unset_track_info()

    def _initialize_log(self) -> Path:
        log_filepath = self._log_folder / f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        return log_filepath

    def _process_individual_file(self, index: int, filepath: Path, log_filepath: Path, total_files: int) -> None:
        self._gui.listWidget_tracks.setCurrentRow(index)
        try:
            self._load_mp3(filepath, raise_exception=True)
            self._gui.label_autotagger_status.setText(self._gui.translate("Main Window", "Tagging files..."))
            self.find_tags(raise_exception=True)
            self.save_tags(raise_exception=True)
            with open(log_filepath, "a") as log:
                log.writelines({str(self._current_track.filepath) + ": OK\n"})
        except Exception:
            with open(log_filepath, "a") as log:
                log.writelines({str(filepath) + ": FAILED\n"})

        self._gui.progressBar_find_and_save_all_tags.setValue(round((index + 1) / total_files * 100))
