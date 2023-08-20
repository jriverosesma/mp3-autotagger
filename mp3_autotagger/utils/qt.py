from PyQt5 import QtCore
from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QIcon, QPixmap

from .assets import main_icon_path


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
    if options is not None:
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
    about_message_box.setWindowIcon(QIcon(str(main_icon_path)))
    about_message_box.setIconPixmap(QPixmap(str(main_icon_path)).scaled(75, 75))

    return about_message_box
