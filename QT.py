import sys
from time import sleep
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 300, 300)
        self.setWindowTitle('test_window_1.0')
        self.knopka1 = QPushButton('Кнопка 1', self)
        self.knopka2 = QPushButton('Кнопка 2', self)
        self.knopka1.resize(100, 50)
        self.knopka1.move(45, 100)
        self.knopka2.resize(100, 50)
        self.knopka2.move(165, 100)
        self.knopka1.clicked.connect(self.privet)

    def privet(self):
        self.knopka2.setText('Привет')
        sleep(5)
        self.knopka1.setText('Кнопка')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
