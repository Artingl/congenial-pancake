import sys
import requests

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from maps import Maps


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.maps = Maps()
        self.image = None
        self.place = None

        self.button_connect()

    def button_connect(self):
        self.find_button.clicked.connect(self.find_place)

    def find_place(self):
        self.place = (self.latitude.text(), self.longitude.text())
        self.image = QPixmap(self.maps.getImage(*self.place))
        self.map_label.setPixmap(self.image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.exit(app.exec_())
