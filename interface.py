import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from maps import Maps


class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.maps = Maps()
        self.image = self.place = self.layer = None

        self.button_connect()
        self.setFocus()

    def button_connect(self):
        self.find_button.clicked.connect(self.find_place)

    def find_place(self):
        self.layer = self.layer_chooser.currentText()
        if self.layer == 'Схема':
            self.layer = 'map'
        if self.layer == 'Спутник':
            self.layer = 'sat'
        if self.layer == 'Гибрид':
            self.layer = 'sat,skl'

        self.place = (self.longitude.text(), self.latitude.text())
        self.image = QPixmap(self.maps.getImage(*self.place, self.layer))
        self.map_label.setPixmap(self.image)
        self.setFocus()

    def keyPressEvent(self, event):
        keyD = False
        speed = 0.002
        if event.key() == Qt.Key_Up:
            self.maps.pos[1] -= speed
            keyD = True
        if event.key() == Qt.Key_Down:
            self.maps.pos[1] += speed
            keyD = True
        if event.key() == Qt.Key_Left:
            self.maps.pos[0] -= speed
            keyD = True
        if event.key() == Qt.Key_Right:
            self.maps.pos[0] += speed
            keyD = True
        if keyD:
            self.find_place()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
