import sys
import signal
from PySide6 import QtWidgets
from main_window import MainWindow

def load_custom_style():
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

def exit_with_sigint():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    load_custom_style()
    exit_with_sigint()
    main_window = MainWindow()
    app.exec()