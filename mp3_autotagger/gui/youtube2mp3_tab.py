import io
from pathlib import Path
from threading import Thread
from typing import Any

import requests
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont, QPixmap
from yt_dlp.utils import DownloadError

from mp3_autotagger.utils.youtube import get_youtube_audiostream

B_TO_MIB: int = 1 / (1024 * 1024)  # Bytes to Mebibyte conversion constant


class Youtube2MP3GUI:
    def __init__(self, gui) -> None:
        """Initialize the Youtube2MP3 GUI.

        Args:
            gui (MainWindowGUI): Main window GUI object.
        """

        self._gui = gui
        self._download_folder: Path = Path.home() / "mp3-autotagger/youtube"
        self._download_folder.mkdir(parents=True, exist_ok=True)
        self._url = None

        # Set new font to be able to display unicode characters
        font = QFont("Noto Color Emoji")
        font.insertSubstitution("Noto Color Emoji", "Sans Serif")
        self._gui.lineEdit_video_title.setFont(font)

    def _reset_ui_elements(self) -> None:
        """Reset UI elements to their default state."""

        self._gui.label_yt_status.clear()
        self._gui.lineEdit_video_title.clear()
        self._gui.lineEdit_audio_details.clear()
        self._gui.label_video_thumbnail.clear()
        self._gui.label_video_thumbnail.setEnabled(False)
        self._gui.label_video_thumbnail.setText("Video thumbnail")
        self._gui.pushButton_download.setEnabled(False)
        self._gui.progressBar_download_signal.emit(0)

    def _set_error_state(self, message: str) -> None:
        """Set the UI elements to reflect an error state.

        Args:
            message (str): The error message to display.
        """

        self._reset_ui_elements()
        self._gui.label_yt_status.setText(self._gui.translate("Main Window", message))

    def _set_ready_state(self) -> None:
        """Set the UI elements to reflect a ready state."""

        self._gui.label_yt_status.setText(self._gui.translate("Main Window", "Ready to download"))
        self._gui.label_video_thumbnail.setEnabled(True)
        self._gui.pushButton_download.setEnabled(True)

    def _get_thumbnail(self, audiostream: dict[str, Any]) -> bytes:
        """Retrieve thumbnail bytes for the given audiostream.

        Args:
            audiostream (dict[str, Any]): The YouTube audio stream info.

        Returns:
            bytes: The thumbnail bytes.
        """

        url = audiostream["thumbnail"]
        response = requests.get(url)
        response.raise_for_status()
        return response.content

    def _set_thumbnail(self, audiostream: dict[str, Any]) -> None:
        """Set the thumbnail for the UI using the given audiostream.

        Args:
            audiostream (dict[str, Any]): The YouTube audio stream info.
        """

        thumbnail_bytes = self._get_thumbnail(audiostream)
        thumbnail = QPixmap()
        thumbnail.loadFromData(io.BytesIO(thumbnail_bytes).read())
        self._gui.label_video_thumbnail.setPixmap(thumbnail)

    def get_yt_audio_info(self) -> None:
        """Retrieve and display YouTube audio info on the GUI."""

        self._reset_ui_elements()

        try:
            self._url = self._gui.lineEdit_url.text()
            audiostream = get_youtube_audiostream(self._gui.lineEdit_url.text(), download=False)

            self._gui.lineEdit_audio_details.setText(
                f"{audiostream['ext']} | {audiostream['abr']} kbps | {round(audiostream['filesize'] * B_TO_MIB, 2)} MB"
            )
            self._gui.lineEdit_video_title.setText(self._gui.translate("Main Window", audiostream["title"]))
            self._set_thumbnail(audiostream)
            self._set_ready_state()
        except DownloadError:
            self._set_error_state("Bad URL")
        except Exception:
            self._set_error_state("Unexpected Error")

    def callback_download_yt(self, d: dict[str, Any]) -> None:
        """Callback function to update UI during YouTube audio download.

        Args:
            d (dict[str, Any]): Download info dictionary.
        """

        percent = d.get("downloaded_bytes", 1) / d.get("total_bytes", 1)
        percent = 0 if percent is None else round(percent * 100)
        eta = d.get("eta", 0)
        eta = 0 if eta is None else round(eta)
        speed = d.get("speed", 0)
        speed = 0 if speed is None else round(speed * B_TO_MIB, 1)

        if percent == 100 and self._gui.checkBox_convert_to_mp3.isChecked():
            self._gui.label_yt_status_signal.emit("Download successful! Converting audio to .mp3...")
        else:
            self._gui.label_yt_status_signal.emit(f"Downloading... [{speed} MiB/s, ETA: {eta} s]")
        self._gui.progressBar_download_signal.emit(percent)

    def download_yt_audio(self) -> None:
        """Download YouTube audio and update the GUI."""

        self._gui.tabWidget.widget(1).setEnabled(False)
        error_text = None

        thread_download_youtube = Thread(
            target=get_youtube_audiostream,
            args=(self._url, self._download_folder),
            kwargs={
                "callback": self.callback_download_yt,
                "convert_to_mp3": self._gui.checkBox_convert_to_mp3.isChecked(),
            },
        )

        try:
            thread_download_youtube.start()
            while thread_download_youtube.is_alive():
                qtw.QApplication.processEvents()
        except Exception:
            error_text = "Error Downloading"

        if error_text:
            self._set_error_state(error_text)
        else:
            self._gui.label_yt_status.setText(
                self._gui.translate("Main Window", f"Success! Audio saved to {self._download_folder}")
            )

        self._gui.tabWidget.widget(1).setEnabled(True)
