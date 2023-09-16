import io
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import Thread

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QPixmap

from mp3_autotagger.utils.assets import RESOURCE_PATHS
from mp3_autotagger.utils.mp3 import MP3
from mp3_autotagger.utils.qt import qt_get_open_files_and_dirs


class MP3AutotaggerGUI:
    """
    GUI for the MP3 Autotagger application.
    Provides an interface for browsing, loading, editing, and saving MP3 metadata.
    """

    def __init__(self, gui) -> None:
        """Initialize the GUI components.
        Args:
            gui (MainWindowGUI): Main window GUI object.
        """

        self._gui = gui
        self._mp3_filepaths: list[Path] = []
        self._current_track: MP3 | None = None
        self._cover_bytes: bytes | None = None
        self._log_folder: Path = Path.home() / "mp3-autotagger/logs"
        self._log_folder.mkdir(parents=True, exist_ok=True)

    def _load_cover(self):
        """Load cover art from the current track or default to a 'no cover' image."""

        if self._current_track.tags["APIC"]:
            self._cover_bytes = self._current_track.tags["APIC"]
        else:
            with open(RESOURCE_PATHS["no_cover"], mode="rb") as f:
                self._cover_bytes = f.read()
        self._set_cover()

    def _set_cover(self) -> None:
        """Display cover art in the GUI."""

        cover = QPixmap()
        cover.loadFromData(io.BytesIO(self._cover_bytes).read())
        self._gui.label_cover.setPixmap(cover)

    def track_clicked(self, item) -> None:
        """Handle track item click event and set track info."""

        self._load_mp3(self._mp3_filepaths[self._gui.listWidget_tracks.currentRow()])
        if self._current_track:
            self._set_track_info()

    def browse_mp3(self) -> None:
        """Browse for MP3 files or directories and populate the GUI list with them."""

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
        """
        Fill the GUI list widget with the paths of the selected MP3 files.

        Args:
            selected_files_mp3 (list[str]): List of paths of the selected MP3 files.
        """

        self._gui.listWidget_tracks.clear()
        self._gui.lineEdit_mp3_dir.setText(self._gui.translate("Main Window", str(selected_files_mp3)))

        for filepath in self._mp3_filepaths:
            self._gui.listWidget_tracks.addItem(filepath.stem)
        self._gui.label_mp3_count.setText(
            self._gui.translate("Main Window", f"{len(self._mp3_filepaths)} .mp3 files found")
        )

    def _set_widget_text(self, widget, tag_key):
        """
        Set text for a given widget based on a tag key.

        Args:
            widget (qtw.QWidget): The widget whose text is to be set.
            tag_key (str): The metadata key for retrieving the tag value.
        """

        widget.setText(self._gui.translate("Main Window", self._current_track.tags[tag_key]))

    def _unset_track_info(self) -> None:
        """Clear the GUI's displayed track info."""

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
        """Set the displayed track info in the GUI based on the current track's metadata."""

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
        """
        Allow the user to manually select a cover image and update the GUI.

        Args:
            event (qtw.QEvent): The event triggering this function.
        """

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
        """
        Load cover bytes from a given file path.

        Args:
            path (str): Path to the image file.
        """

        with open(path, mode="rb") as f:
            self._cover_bytes = f.read()

    def _find_all_mp3(self, find_path: Path) -> list[Path]:
        """
        Find all MP3 files in the given path and return their file paths.

        Args:
            find_path (Path): Path to search for MP3 files.

        Returns:
            list[Path]: List of paths of the found MP3 files.
        """

        if find_path.is_file() and find_path.suffix == ".mp3":
            return [find_path]

        return sorted([filepath for filepath in find_path.rglob("*.mp3")])

    def _load_mp3(self, filepath: Path, raise_exception: bool = False) -> None:
        """
        Load an MP3 file and set the current track to it.

        Args:
            filepath (Path): Path to the MP3 file.
            raise_exception (bool, optional): If True, raises an exception on failure. Defaults to False.
        """

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
        """
        Find tags for the current track using Shazam.

        Args:
            thread_shazam (bool, optional): If True, uses threaded search with Shazam. Defaults to True.
            raise_exception (bool, optional): If True, raises an exception on failure. Defaults to False.
        """

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
        """
        Update the tags for the current track using Shazam.

        If thread_shazam is set to True, this method uses a worker thread to fetch
        the tags to prevent freezing of the main application.

        Args:
        - thread_shazam (bool): Whether to use threading for the Shazam update or not.

        Returns:
        - bool: True if the tags were updated successfully, False otherwise.
        """

        def worker(queue):
            """Worker function to be run on a separate thread."""
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
        """
        Save the tags for the current track.

        This method also handles file renaming if required and updates the UI.

        Args:
        - raise_exception (bool): If True, exceptions are raised, otherwise, they're handled internally.
        """

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
        """Update the tags for the current track based on the values from the GUI."""

        self._current_track.tags["TPE1"] = self._gui.lineEdit_artist.text()
        self._current_track.tags["TIT2"] = self._gui.lineEdit_title.text()
        self._current_track.tags["TALB"] = self._gui.lineEdit_album.text()
        self._current_track.tags["TCON"] = self._gui.lineEdit_genre.text()
        self._current_track.tags["TDRC"] = self._gui.lineEdit_year.text()
        self._current_track.tags["APIC"] = io.BytesIO(self._cover_bytes).read()

    def _update_displayed_filepath(self):
        """Update the filepath displayed in the GUI for the current track."""

        self._mp3_filepaths[self._gui.listWidget_tracks.currentRow()] = self._current_track.filepath
        self._gui.listWidget_tracks.currentItem().setText(
            self._gui.translate("Main Window", self._current_track.filepath.stem)
        )

    def find_and_save_all_tags(self) -> None:
        """Find and save tags for all tracks in the list and log the results."""

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
        """
        Initialize a log file for recording the results of tag fetching and saving.

        Returns:
        - Path: The filepath to the created log file.
        """

        log_filepath = self._log_folder / f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        return log_filepath

    def _process_individual_file(self, index: int, filepath: Path, log_filepath: Path, total_files: int) -> None:
        """
        Process an individual track: find its tags, save them, and log the results.

        Args:
        - index (int): The index of the track in the list.
        - filepath (Path): The filepath to the track.
        - log_filepath (Path): The filepath to the log file.
        - total_files (int): The total number of files being processed.
        """

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
