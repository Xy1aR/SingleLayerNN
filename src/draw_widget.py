from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel
from PIL import ImageQt
import numpy as np


# класс с инициализацией окна рисования
class DrawWidget(QLabel):
    def __init__(self, s, pen_size, nn):
        super().__init__(s)
        self.init_ui()
        canvas = QtGui.QPixmap(280, 280)
        canvas.fill(QtGui.QColor('#FFFFFF'))
        self.setPixmap(canvas)
        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')
        self.pen_size = pen_size
        self.nn = nn
        self.answer = ''

    def init_ui(self):
        self.setStyleSheet('border-style: solid; border-width: 1px; border-color: black; background-color: white')
        self.setGeometry(10, 10, 280, 280)

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def clear(self):
        self.pixmap().fill(QtGui.QColor('#000000'))
        self.update()

    def mouseMoveEvent(self, e):
        try:
            if self.last_x is None:
                self.last_x = e.position().x()
                self.last_y = e.position().y()
                return

            canvas = self.pixmap()
            painter = QtGui.QPainter(canvas)
            p = painter.pen()
            p.setWidth(self.pen_size)
            p.setColor(self.pen_color)
            painter.setPen(p)
            painter.drawLine(self.last_x, self.last_y, e.position().x(), e.position().y())
            painter.end()
            self.setPixmap(canvas)
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            image = self.grab()
            resized_image = image.scaled(28, 28).toImage()
            test_image = ImageQt.fromqimage(resized_image).convert('L')
            self.answer = self.nn.test(np.asarray(test_image.getdata()))
        except Exception as e:
            print(e)

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
