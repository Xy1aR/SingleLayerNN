import random
import numpy as np
from neuron import Neuron


# класс скрытого слоя
class Layer:
    def __init__(self, num_of_inputs):
        self.num_of_inputs = num_of_inputs  # поле для хранения количества связей на входе нейрона
        # (равно размеру изображения)

        self.neurons = []  # поле для хранения массив нейронов этого слоя
        self.weights = []  # поле для хранения массива значения весов нейронов

    # метод для инициализации нейронов
    def set_neurons(self, names):
        # цикл для создания объектов класса Neuron внутри массива с установкой их имен
        for i in range(len(names)):
            self.neurons.append(Neuron(names[i]))

    # метод для генерации случайных весов в диапазоне от -1 до 1
    def create_weights(self):
        for i in range(len(self.neurons)):
            for k in range(self.num_of_inputs):
                self.weights.append(random.random() * 2 - 1)
                self.neurons[i].weights = self.weights
            self.weights = []

    # метод для получения ответа сети
    def get_answer(self, inputs):
        nets = []

        for neuron in self.neurons:
            nets.append(neuron.calc_net(inputs))

        answers = np.array(nets)
        exponential = np.exp(answers)
        probabilities = exponential / np.sum(exponential)

        return probabilities
        # max_value = max(nets)
        # answer = nets.index(max_value)

    # метод для корректировки весов
    def correct_weights(self, train_size, train_data, train_labels, lr, activation_value):
        for pic in range(train_size):
            for neuron in self.neurons:
                net = neuron.calc_net(train_data[pic])

                if train_labels[pic] != neuron.name and net > activation_value:
                    for index in range(self.num_of_inputs):
                        if train_data[pic][index] == 1:
                            neuron.weights[index] -= lr
                elif train_labels[pic] == neuron.name and net <= activation_value:
                    for index in range(self.num_of_inputs):
                        if train_data[pic][index] == 1:
                            neuron.weights[index] += lr
