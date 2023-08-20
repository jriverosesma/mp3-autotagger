import sys

from PyQt5 import QtWidgets as qtw

from .gui import GUI


def main() -> None:
    app: qtw.QApplication = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")

    gui: GUI = GUI()
    gui.show()
    gui.label_cover.setMinimumHeight(0)  # Reset cover minimum height after showing main window

    sys.exit(app.exec_())
