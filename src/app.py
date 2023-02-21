from PIL import ImageQt
from PyQt6 import QtWidgets
from PyQt6.QtGui import QFont, QFontMetrics
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from draw_widget import DrawWidget
from mydesign import Ui_MainWindow
import sys
import numpy as np
from neural_network import NeuralNetwork


# основной класс приложения с инициализацией окна, интерфейса и его функций
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # наследование из класса MainWindow для инициализации окна
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # создание объекта класса Ui_MainWindow
        self.ui.setupUi(self)  # вызов метода setupUi из объекта ui
        self.menuBar().addMenu(QMenu("File", self))
        self.setMenuBar(self.menuBar())

        self.pix_size = (28, 28)  # поле для хранения конечных размеров изображения
        self.default_file = "C:/Users/nikit/PycharmProjects/1LAyerNN/data/zodiac_data.csv"
        self.default_num_epochs = 3
        self.default_lr = 0.01
        self.default_activation_value = 0

        # инициализация кнопки вызова метода для тренирвоки нейронной сети
        button_train = QtWidgets.QPushButton(self)
        button_train.setText("Train")
        button_train.move(305, 95)
        button_train.clicked.connect(self.button_train_clicked)

        # инициализация кнопки вызова метода для тренирвоки нейронной сети
        button_recognize = QtWidgets.QPushButton(self)
        button_recognize.setText("Recognize")
        button_recognize.move(305, 135)
        button_recognize.clicked.connect(self.button_recognize_clicked)

        # инициализация кнопки вызова метода для выбора файла с данными
        button_file = QtWidgets.QPushButton(self)
        button_file.setText("Choose file")
        button_file.move(305, 15)
        button_file.clicked.connect(self.button_file_clicked)

        # инициализация текстового поля, в котором отображается имя файла
        self.file_label = QTextEdit('', self, )
        self.file_label.setPlaceholderText("Search...")
        self.file_label.setText(self.default_file)
        font = QFont(self.default_file)
        fm = QFontMetrics(font)
        pixels_width = fm.horizontalAdvance(self.default_file)
        self.file_label.setGeometry(305, 55, pixels_width, self.file_label.height())
        self.file_label.move(305, 55)

        # инициализация текстового поля, в котором отображается имя файла
        self.epochs_label = QTextEdit('', self, )
        # self.epochs_label.setOverwriteMode(True)
        self.epochs_label.setPlaceholderText("Search...")
        self.epochs_label.setText(str(self.default_num_epochs))
        self.epochs_label.move(455, 95)

        # инициализация текстового поля, в котором отображается имя файла
        self.lr_label = QTextEdit('', self, )
        self.lr_label.setPlaceholderText("Search...")
        self.lr_label.setText(str(self.default_lr))
        self.lr_label.move(455, 195)

        # инициализация текстового поля, в котором отображается имя файла
        self.activ_label = QTextEdit('', self, )
        self.activ_label.setPlaceholderText("Search...")
        self.activ_label.setText(str(self.default_activation_value))
        self.activ_label.move(455, 295)

        self.answers_label = QTextEdit('', self, )
        self.answers_label.move(600, 400)

        # инициализация кнопки вызова метода очистки окна рисования
        button_clear = QtWidgets.QPushButton(self)
        button_clear.setText("Clear")
        button_clear.move(170, 300)
        button_clear.clicked.connect(self.button_clear_clicked)

        # инициализация слайдера для настройки ширины кисти
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.move(25, 300)
        self.slider.setRange(1, 15)
        self.slider.setValue(10)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider.valueChanged.connect(self.update_pen)  # вызов метода для отображения размера кисти

        # инициализация надписи с информацией о ширине кисти
        self.result_label = QLabel('', self)
        self.result_label.setText(f'Pen size: {self.slider.value()}')
        self.result_label.move(25, 330)

        self.nn = NeuralNetwork(int(self.epochs_label.toPlainText()), float(self.lr_label.toPlainText()),
                                float(self.activ_label.toPlainText()))

        # инициализация объекта класса DrawWidget, отвечающего за окно рисования
        self.draw_widget = DrawWidget(self.ui.centralwidget, self.slider.value(), self.nn)
        self.draw_widget.setObjectName("draw_widget")
        self.draw_widget.installEventFilter(self)

    def eventFilter(self, source, event):
        try:
            if source is self.draw_widget and event.type() == 2:
                print(self.draw_widget.answer)
            return super(MainWindow, self).eventFilter(source, event)
        except Exception as e:
            print(e)
            pass

    # метод для изменения отображения размера кисти
    def update_pen(self, value):
        self.result_label.setText(f'Current pen size: {value}')
        self.draw_widget.pen_size = value

    # метод для тренировки нейронной сети при нажатии на кнопку
    def button_train_clicked(self):
        self.nn = NeuralNetwork(int(self.epochs_label.toPlainText()), float(self.lr_label.toPlainText()),
                                float(self.activ_label.toPlainText()))
        self.nn.data_csv_name = self.file_label.toPlainText()
        self.nn.train()
        self.draw_widget.nn = self.nn

    # метод для распознавания нарисованного изображения
    def button_recognize_clicked(self):
        image = self.draw_widget.grab()
        resized_image = image.scaled(self.pix_size[0], self.pix_size[1]).toImage()
        test_image = ImageQt.fromqimage(resized_image).convert('L')
        if self.nn is not None:
            self.nn.test(np.asarray(test_image.getdata()))
        else:
            print('sosi')

    # метод для отображения выбранного файла в текстовом поле
    def button_file_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, "Выберите файл",
                                                           "../data",
                                                           "Csv Files(*.csv)")
        font = QFont(file_name)
        fm = QFontMetrics(font)
        pixels_width = fm.horizontalAdvance(file_name)
        self.file_label.setGeometry(305, 55, pixels_width, self.file_label.height())
        self.file_label.setText(file_name)

    # метод для вызова метода очистки окна рисования из объекта draw_widget
    def button_clear_clicked(self):
        self.draw_widget.clear()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
