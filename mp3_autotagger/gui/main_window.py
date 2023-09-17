from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets as qtw

from mp3_autotagger import __version__ as package_version
from mp3_autotagger.gui.mp3_autotagger_tab import MP3AutotaggerGUI
from mp3_autotagger.gui.ui import Ui_MainWindow
from mp3_autotagger.gui.youtube2mp3_tab import Youtube2MP3GUI
from mp3_autotagger.utils.assets import RESOURCE_PATHS
from mp3_autotagger.utils.qt import qt_get_about_widget
from mp3_autotagger.utils.update import check_for_updates


class MainWindowGUI(qtw.QMainWindow, Ui_MainWindow):
    """Main Window for MP3 Autotagger and Youtube2MP3 functionalities."""

    # Constants
    ORIGINAL_SCREEN_SIZE = (1920, 1080)

    # Signals
    progressBar_find_and_save_all_tags_signal = QtCore.pyqtSignal(int)
    label_yt_status_signal = QtCore.pyqtSignal(str)
    progressBar_download_signal = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize main window and its functionalities."""

        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # Set asset resources
        self._set_icon_assets()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(RESOURCE_PATHS["main_icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # Tabs GUIs
        self._mp3_autotagger_gui: MP3AutotaggerGUI = MP3AutotaggerGUI(self)
        self._youtube2mp3_gui: Youtube2MP3GUI = Youtube2MP3GUI(self)

        # Main window settings
        self.translate = QtCore.QCoreApplication.translate
        self._trans = QtCore.QTranslator(self)
        self._set_app_scale()
        self._connect_signals_slots()

    @staticmethod
    def _get_icon_from_image_path(image_path: str) -> QtGui.QIcon:
        """Get Qt icon from image path."""

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        return icon

    def _set_icon_assets(self) -> None:
        """Sets icon assets for main window and tabs."""

        # Main window icon
        icon = MainWindowGUI._get_icon_from_image_path(RESOURCE_PATHS["main_icon"])
        self.setWindowIcon(icon)

        # Tab icons
        for tab, icon_name in zip([self.tab_autotagger, self.tab_youtube2mp3], ["autotagger_icon", "youtube2mp3_icon"]):
            icon = MainWindowGUI._get_icon_from_image_path(RESOURCE_PATHS[icon_name])
            index = self.tabWidget.indexOf(tab)
            self.tabWidget.setTabIcon(index, icon)

    def _set_app_scale(self) -> None:
        """Adjust the scale of the app based on the screen size."""

        current_screen_size = qtw.qApp.primaryScreen().geometry()

        # Compute ratios
        width_ratio = current_screen_size.width() / self.ORIGINAL_SCREEN_SIZE[0]
        height_ratio = current_screen_size.height() / self.ORIGINAL_SCREEN_SIZE[1]

        # Resize main window
        original_window_size = self.size()
        self.resize(int(original_window_size.width() * width_ratio), int(original_window_size.height() * height_ratio))

        # Adjust cover label size constraints
        self.label_cover.setMinimumWidth(int(self.checkBox_rename_file.width()))
        self.label_cover.setMinimumHeight(int(self.checkBox_rename_file.width()))
        self.label_cover.setMaximumWidth(int(width_ratio * self.label_cover.maximumWidth()))
        self.label_cover.setMaximumHeight(int(height_ratio * self.label_cover.maximumHeight()))

    def _connect_signals_slots(self) -> None:
        """Connect signals to their respective slots."""

        # Main window connections
        self.actionAbout.triggered.connect(self._show_about)
        self.actionEnglish.triggered.connect(self._set_language_english)
        self.actionSpanish.triggered.connect(self._set_language_spanish)
        self.actionUpdates.triggered.connect(self._update_app)
        self.progressBar_download_signal.connect(self.progressBar_download.setValue)
        self.label_yt_status_signal.connect(self.label_yt_status.setText)

        # Autotagger connections
        self.pushButton_browse.pressed.connect(self._mp3_autotagger_gui.browse_mp3)
        self.pushButton_find_tags.pressed.connect(self._mp3_autotagger_gui.find_tags)
        self.pushButton_save_tags.pressed.connect(self._mp3_autotagger_gui.save_tags)
        self.pushButton_find_and_save_all_tags.pressed.connect(self._mp3_autotagger_gui.find_and_save_all_tags)
        self.label_cover.mousePressEvent = self._mp3_autotagger_gui.manually_add_cover
        self.listWidget_tracks.itemClicked.connect(self._mp3_autotagger_gui.track_clicked)

        # Youtube2MP3 connections
        self.pushButton_get_audio_info.pressed.connect(self._youtube2mp3_gui.get_yt_audio_info)
        self.pushButton_download.pressed.connect(self._youtube2mp3_gui.download_yt_audio)

    def _retranslate(self, qm_filepath: str = None) -> None:
        """
        Reload the UI translations based on the provided .qm file.

        Args:
            qm_filepath (str, optional): Path to the .qm file containing translations. If not provided,
                removes the translator. Defaults to None.
        """

        if qm_filepath:
            self._trans.load(qm_filepath)
            qtw.QApplication.instance().installTranslator(self._trans)
        else:
            qtw.QApplication.instance().removeTranslator(self._trans)
        self.retranslateUi(self)

    def _show_about(self) -> None:
        """Display the 'About' window with application details."""

        about_message_box = qt_get_about_widget()
        about_message_box.setWindowTitle(self.translate("Main Window", "About MP3 Autotagger"))
        about_message_box.setText(
            self.translate(
                "Main Window",
                "<p>An application for MP3 autotagging and more.</p>"
                f"<p>Version: {package_version}</p>"
                '<p>GitHub: <a href="https://github.com/jriverosesma/mp3-autotagger">mp3-autotagger</a></p>'
                '<p>Email: <a href="mailto:jriverosesma@gmail.com">jriverosesma@gmail.com</a></p>',
            )
        )
        about_message_box.exec()

    def _show_info_message(self, message_md: str, title: str = "Info") -> None:
        """
        Display an informational message box.

        Args:
            message_md (str): The message (in markdown format) to display.
            title (str, optional): The title of the message box. Defaults to "Info".
        """

        qtw.QMessageBox.information(self, title, message_md)

    def _show_error_message(self, message_md: str = "Unknown Error", title: str = "Error") -> None:
        """
        Display an error message box.

        Args:
            message_md (str, optional): The error message (in markdown format) to display.
                Defaults to "Unknown Error".
            title (str, optional): The title of the error message box. Defaults to "Error".
        """

        qtw.QMessageBox.critical(self, title, message_md)

    def _update_app(self) -> None:
        """Check for application updates and provide user feedback."""

        try:
            status = check_for_updates()
            self._show_info_message(
                message_md=self.translate("Main Window", status),
                title=self.translate("Main Window", "Update"),
            )
        except Exception:
            self._show_error_message(
                message_md=self.translate("Main Window", "Update failed!"),
                title=self.translate("Main Window", "Update"),
            )

    def _set_language_english(self) -> None:
        """Set the application language to English."""

        self._retranslate()

    def _set_language_spanish(self) -> None:
        """Set the application language to Spanish."""

        self._retranslate(RESOURCE_PATHS["eng-es"])
