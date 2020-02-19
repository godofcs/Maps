import requests
import os
import pprint
from io import BytesIO
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtWidgets import QPushButton, QLineEdit,QLabel
from PyQt5.QtGui import QPixmap


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1000, 800)
        self.maps()
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.move(50, 50)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)

    def maps(self):
        adres = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": "Владивосток",
            "format": "json"
        }
        resque = requests.get(adres, params=params).json()
        obect = resque["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        obect_coord = obect["Point"]["pos"]
        adres2 = "https://static-maps.yandex.ru/1.x/"
        params2 = {
            "l": "map",
            "ll": ",".join(obect_coord.split()),
            "spn": "0.1,0.1"
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