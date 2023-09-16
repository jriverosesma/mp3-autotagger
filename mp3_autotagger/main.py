import sys

from PyQt5 import QtWidgets as qtw

from mp3_autotagger.gui import GUI


def main() -> None:
    app: qtw.QApplication = qtw.QApplication(sys.argv)
    app.setStyle("Fusion")

    gui: GUI = GUI()
    gui.show()

    sys.exit(app.exec_())
