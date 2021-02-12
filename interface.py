import sys
import requests

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec_())
