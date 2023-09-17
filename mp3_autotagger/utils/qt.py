from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon, QPixmap

from mp3_autotagger.utils.assets import RESOURCE_PATHS


def qt_get_open_files_and_dirs(
    parent: qtw.QWidget | None = None,
    caption: str = "",
    directory: str = "",
    filter: str = "",
    initialFilter: str = "",
    options: tuple[qtw.QFileDialog.Options, qtw.QFileDialog.Option] | None = None,
) -> list[str]:
    """
    Open a QFileDialog allowing users to select multiple files and directories.

    Args:
        parent (qtw.QWidget, optional): The parent widget. Defaults to None.
        caption (str, optional): The dialog caption. Defaults to an empty string.
        directory (str, optional): Initial directory. Defaults to an empty string.
        filter (str, optional): Filtering for file extensions. Defaults to an empty string.
        initialFilter (str, optional): Initially selected filter. Defaults to an empty string.
        options (tuple[qtw.QFileDialog.Options, qtw.QFileDialog.Option], optional): Dialog options. Defaults to None.

    Returns:
        list[str]: List of selected files and directories.
    """

    def updateText():
        """Update the text in the dialog with the selected items."""
        selected = [index.data() for index in view.selectionModel().selectedRows()]
        lineEdit.setText(" ".join(selected))

    # Create a file dialog
    dialog = qtw.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options is not None:
        dialog.setOptions(*options or ())
    # Ensure the Qt dialog is used, not a native dialog
    dialog.setOption(dialog.DontUseNativeDialog, True)
    dialog.setDirectory(directory)
    dialog.setNameFilter(filter)
    if initialFilter:
        dialog.selectNameFilter(initialFilter)

    # Override the accept method of the dialog to use QDialog's accept
    dialog.accept = lambda: qtw.QDialog.accept(dialog)

    # Find the list view within the stacked widget in the dialog
    stackedWidget = dialog.findChild(qtw.QStackedWidget)
    view = stackedWidget.findChild(qtw.QListView)
    # Connect the selection changed signal to the update text function
    view.selectionModel().selectionChanged.connect(updateText)

    # Find the line edit widget in the dialog and connect it to clear its content when the directory is entered
    lineEdit = dialog.findChild(qtw.QLineEdit)
    dialog.directoryEntered.connect(lambda: lineEdit.setText(""))

    # Show the dialog and return the selected files if "Open" is clicked; otherwise, return an empty list
    return dialog.selectedFiles() if dialog.exec_() else []


def qt_get_about_widget() -> qtw.QMessageBox:
    """
    Create and configure an "About" QMessageBox with the application's main icon.

    Returns:
        qtw.QMessageBox: Configured "About" message box.
    """

    about_message_box = qtw.QMessageBox()
    # Set the main icon for the about message box
    about_message_box.setWindowIcon(QIcon(RESOURCE_PATHS["main_icon"]))
    # Set a scaled pixmap of the main icon as the main icon of the message box
    about_message_box.setIconPixmap(QPixmap(RESOURCE_PATHS["main_icon"]).scaled(75, 75))

    return about_message_box
