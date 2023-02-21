import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from neural_network import NeuralNetwork
from draw_widget import DrawWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("1LayerNN_App")
        self.resize(800, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.init_menu_bar()
        self.init_buttons()


        self.pix_size = (28, 28)  # поле для хранения конечных размеров изображения
        self.default_file = "C:/Users/nikit/PycharmProjects/1LAyerNN/data/zodiac_data.csv"
        self.default_num_epochs = 3
        self.default_lr = 0.01
        self.default_activation_value = 0
        self.nn = NeuralNetwork(self.default_num_epochs, self.default_lr,
                                self.default_activation_value)

        # инициализация объекта класса DrawWidget, отвечающего за окно рисования
        self.draw_widget = DrawWidget(self.central_widget, 4, self.nn)
        self.draw_widget.setObjectName("draw_widget")
        # self.draw_widget.installEventFilter(self)

    def init_menu_bar(self):
        menu_bar = self.menuBar()
        # Creating menus using a QMenu object
        menu_bar.addMenu("File")
        menu_bar.addMenu("Edit")
        menu_bar.addMenu("Help")

    def init_buttons(self):
        button_train = QPushButton(self)
        button_train.setText("Train")
        button_train.move(305, 95)
        button_train.clicked.connect(self.button_train_clicked)

    def button_train_clicked(self):
        # self.nn = NeuralNetwork(int(self.epochs_label.toPlainText()), float(self.lr_label.toPlainText()),
        #                         float(self.activ_label.toPlainText()))
        self.nn.data_csv_name = self.default_file
        self.nn.train()
        self.draw_widget.nn = self.nn


app = QApplication(sys.argv)

window = MainWindow()
window.show()

# Запускаем цикл событий.
app.exec()
