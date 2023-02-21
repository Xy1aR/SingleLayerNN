# класс c инициализацией нейрона
class Neuron:
    def __init__(self, name):
        self.name = name  # поле для хранения класса, которому соответствует нейрон
        self.weights = []  # поле для хранения массива весов связей между нейронами

    # метод для расчета значения выхода нейрона
    def calc_net(self, inputs):
        net = 0

        # цикл для расчета выходного значения
        for i in range(len(self.weights)):
            net += self.weights[i] * inputs[i]

        return net
