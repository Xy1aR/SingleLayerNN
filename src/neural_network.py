import csv
import image_upscale as iu
from layer import Layer
import numpy as np


# класс с инициализацией нейронной сети
class NeuralNetwork:
    def __init__(self, epochs, lr, activation_value):
        self.data_csv_name = ""  # поле для хранения названия файла с данными
        self.image_size = 28 * 28  # поле для хранения размера изображения
        self.epochs = 3  # поле для хранения количества эпох обучения
        self.lr = 0.01  # поле для хранения скорости обучения
        self.activation_value = 0  # поле для хранения порогового значения
        self.train_size = 0  # поле для хранения размера тренировочной выборки
        self.valid_size = 0  # поле для хранения размера валидационной выборки
        self.hidden_layer = Layer(self.image_size)  # поле для хранения объекста класса Layer

    # метод для инициализации датасета
    def get_dataset(self):
        values = []  # массив для хранения значений пикселей. Представляет собой двумерный массив,
        # где каждый элемент хранит значение всех пикселей изображения

        labels = []  # массив для хранения классов

        # открываем файл, считываем оттуда строки со значениями пикселей и классов, добавляем в соответствующие массивы
        with open(self.data_csv_name, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                values.append(list(map(int, row[:-1])))
                labels.append(row[-1])

        self.hidden_layer.set_neurons(list(set(labels)))  # вызов метода set_neurons из объекта hidden_layer
        # с именами классов в качестве аргумента
        for neuron in self.hidden_layer.neurons:
            print(neuron.name)

        dataset_size = len(values)  # получение размера датасета
        self.train_size = int(dataset_size * 0.75)  # установка размера тренировочной выборки
        self.valid_size = dataset_size - self.train_size  # установка размера валидационной выборки

        train_data = values[:self.train_size]  # создание тренировочной выборки с пикселями изображений
        train_labels = labels[:self.train_size]  # создание тренировочной выборки с именами классов

        valid_data = values[:self.valid_size]  # создание валидационной выборки с пикселями изображений
        valid_labels = labels[:self.valid_size]  # создание валидационной выборки с именами классов

        return train_data, train_labels, valid_data, valid_labels

    # метод для обучения нейронной сети
    def train(self):
        # кострукция try-exception для отслеживания ошибок и предовращения "падения" приложения
        try:
            valid_acc = []  # массив для хранения точности распознавания на валидационной выборке
            x_train, y_train, x_valid, y_valid = self.get_dataset()  # вызов метода get_dataset и запись данных в
            # переменные

            self.hidden_layer.create_weights()  # вызов метода create_weights из объекта hidden_layer

            # цикл тренировки нейронной сети
            for epoch in range(self.epochs):
                correct_counter = 0  # счетчик верных ответов сети

                # вызов метода correct_weights из объекта hidden_layer
                self.hidden_layer.correct_weights(self.train_size, x_train, y_train, self.lr, self.activation_value)

                # цикл тестирования точности распознавания обученной нейронной сети
                for index in range(self.valid_size):

                    # вызов метода get_answer из объекта hidden_layer
                    answers = self.hidden_layer.get_answer(x_valid[index])
                    answer, = np.where(answers == np.max(answers))


                    # проверка совпадения имени нейрона с максимальным значением на выходе сети с реальным классом
                    # изображения. Если выполняется, то счетчик верных ответов инкрементируется
                    if self.hidden_layer.neurons[answer[0]].name == y_valid[index]:
                        correct_counter += 1

                valid_acc.append(correct_counter / len(x_valid))  # добавления точности распознавния сети в массив
                print(correct_counter, "\n", f"Accuracy: {round(correct_counter / len(x_valid) * 100, 2)}%", "\n")
            print(valid_acc)
        except Exception as e:
            print(e)

    # метод для идентификации класса нарисованного изображения
    def test(self, image_data):
        try:
            pic = iu.pic_upscale(image_data)  # вызов метода pic_upscale из объекта iu
            answers = self.hidden_layer.get_answer(pic)
            print([self.hidden_layer.neurons[i].name for i in range(12)], '\n')
            print(np.round(answers, 2), np.sum(answers), '\n')
            answer, = np.where(answers == np.max(answers))
            print(self.hidden_layer.neurons[answer[0]].name)

            return answer
        except Exception as e:
            print(e)
            pass
