import sys

from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

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
        self.layer_chooser.currentTextChanged.connect(self.find_place)
        self.undo_button.clicked.connect(self.find_place)

    def mousePressEvent(self, mouse):
        x = mouse.pos().x()
        y = mouse.pos().y()

        if self.map_label.pos().x() < x < self.map_label.pos().x() + self.map_label.width() and \
                self.map_label.pos().y() < y < self.map_label.pos().y() + self.map_label.height():
            x = (x - self.map_label.pos().x()) - (self.map_label.width() / 2)
            y = (y - self.map_label.pos().y()) - (self.map_label.height() / 2)

            # TODO

            self.maps.pt[1] = (c1, c2)
            self.find_place()

    def find_place(self):
        if type(self.sender()).__name__ == 'QPushButton':
            if self.sender().text() == 'Undo':
                self.maps.show_pt = False
                self.geodata_text.setText("")
                self.adress_label.setText("")

                self.longitude.setText("")
                self.latitude.setText("")
                self.geodata_text.setText("")
                return
            elif self.sender().text() == "Find":
                self.maps.show_pt = True
        self.layer = self.layer_chooser.currentText()
        if self.layer == 'Схема':
            self.layer = 'map'
        if self.layer == 'Спутник':
            self.layer = 'sat'
        if self.layer == 'Гибрид':
            self.layer = 'sat,skl'
        if self.longitude.text() and self.latitude.text():
            self.place = (self.longitude.text(), self.latitude.text())
            self.image = QPixmap(self.maps.getImage(self, c1=self.place[0], c2=self.place[1], layer=self.layer))
        if self.geodata_text.text():
            self.place = self.geodata_text.text()
            self.image = QPixmap(self.maps.getImage(self, geo=self.place, layer=self.layer))
        self.map_label.setPixmap(self.image)
        self.setFocus()

    def keyPressEvent(self, event):
        keyD = False
        speed = 0.002
        if event.key() == Qt.Key_PageUp:
            self.maps.spn += speed
            keyD = True
        if event.key() == Qt.Key_PageDown:
            self.maps.spn -= speed
            keyD = True
        if event.key() == Qt.Key_Up:
            self.maps.pos[1] += self.maps.spn * 2
            keyD = True
        if event.key() == Qt.Key_Down:
            self.maps.pos[1] -= self.maps.spn * 2
            keyD = True
        if event.key() == Qt.Key_Left:
            self.maps.pos[0] -= self.maps.spn * 2
            keyD = True
        if event.key() == Qt.Key_Right:
            self.maps.pos[0] += self.maps.spn * 2
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
