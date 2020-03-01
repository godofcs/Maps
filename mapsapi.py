import requests
import os
import pprint
from io import BytesIO
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit,QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.zoom = 0.001
        self.delta = 0.0001
        adres = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": "Владивосток",
            "format": "json"
        }
        resque = requests.get(adres, params=params).json()
        obect = resque["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.obect_coord = obect["Point"]["pos"].split()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.maps()
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom > 0.001:
            self.zoom -= 0.005
            self.delta += 0.005
        if event.key() == Qt.Key_PageDown and self.zoom < 20:
            self.zoom += 0.005
            self.delta += 0.005
        elif event.key() == Qt.Key_Left:
            self.obect_coord[0] = str(float(self.obect_coord[0]) - self.delta)
        elif event.key() == Qt.Key_Right:
            self.obect_coord[0] = str(float(self.obect_coord[0]) + self.delta)
        elif event.key() == Qt.Key_Up:
            self.obect_coord[1] = str(float(self.obect_coord[1]) + self.delta)
        elif event.key() == Qt.Key_Down:
            self.obect_coord[1] = str(float(self.obect_coord[1]) - self.delta)
        else:
            return
        print(self.zoom)
        self.maps()
        self.pixmap = QPixmap('map.png')
        self.image.setPixmap(self.pixmap)

    def maps(self):
        adres2 = "https://static-maps.yandex.ru/1.x/"
        params2 = {
            "l": "map",
            "ll": ",".join(self.obect_coord),
            "spn": ",".join([str(self.zoom), str(self.zoom)])
        }
        resque2 = requests.get(adres2, params=params2)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(resque2.content)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())