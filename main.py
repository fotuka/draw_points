import math
import numpy as np
import matplotlib.pyplot as plt


class Grid():

    def create(self):
        self.xdots = np.array([], float)
        self.ydots = np.array([], float)
        x = int_input_variable("Введите длину")
        y = int_input_variable("Введите высоту")
        xline = int_input_variable("Введите кол-во вертикальных перекладин")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин")
        xgap = (x / (xline + 1))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline + 1))  # расстояние между перекладинами по горизонтали
        for i in np.arange(0, y + 1, ygap):  # i=y
            for j in np.arange(0, x + 1, xgap):  # j=x
                self.ydots = np.append(self.ydots, [i])  # y
                self.xdots = np.append(self.xdots, [j])  # x


class SlopeGrid():

    def create(self):
        self.xdots = np.array([], float)
        self.ydots = np.array([], float)
        x = int_input_variable("Введите длину")
        y = int_input_variable("Введите высоту")
        xline = int_input_variable("Введите кол-во вертикальных перекладин")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин")
        xgap = (x / (xline + 1))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline + 1))  # расстояние между перекладинами по горизонтали
        pop = -1
        for i in np.arange(0, y + 1, ygap):  # i=y
            pop = pop * -1
            for j in np.arange(0, x + 1, xgap):  # j=x
                self.ydots = np.append(self.ydots, [i])  # y
                if pop == 1:
                    j = j + xgap * 0.5
                self.xdots = np.append(self.xdots, [j])  # x


class Snow():

    def create(self):
        r = int_input_variable("Введите радиус")
        d = int_input_variable("Введите Расстояние между точками")
        self.xdots = np.array([0], float)  # x
        self.ydots = np.array([0], float)  # y
        for k in range(0, 8):
            for j in np.arange(d, r, d):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(45 * k))) + (j * math.cos(math.radians(45 * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(45 * k))) - (j * math.sin(math.radians(45 * k)))])


class SnowAdvanced():

    def create(self):
        r = int_input_variable("Введите радиус")
        d = int_input_variable("Введите Расстояние между точками")
        self.xdots = np.array([0], float)  # x
        self.ydots = np.array([0], float)  # y
        pop = -1
        ror = 1
        for k in range(0, 8):
            for j in np.arange(d, r, d):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(45 * k))) + (j * math.cos(math.radians(45 * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(45 * k))) - (j * math.sin(math.radians(45 * k)))])
        for k in range(0, 16):
            ror = ror * -1
            if ror == 1:
                for j in np.arange(d*0.5, r, d*0.5):
                    pop = pop * -1
                    if pop == 1:
                        self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(22.5 * k))) + (j * math.cos(math.radians(22.5 * k)))])
                        self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(22.5 * k))) - (j * math.sin(math.radians(22.5 * k)))])
                pop = -1


def rotate(degree, xdots, ydots):
    x = np.array([], float)
    y = np.array([], float)
    for i in range(len(xdots)):
        x = np.append(x, [(xdots[i] * math.cos(math.radians(degree))) - (ydots[i] * math.sin(math.radians(degree)))])
    for i in range(len(ydots)):
        y = np.append(y, [(xdots[i] * math.sin(math.radians(degree))) + (ydots[i] * math.cos(math.radians(degree)))])
    carozzera.xdots = x
    carozzera.ydots = y


def display(x, y, xmin=0, xmax=0, ymin=0, ymax=0):
    plt.scatter([x], [y])
    if (xmin or xmax or ymin or ymax) != 0:
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
    plt.show()


def export(xdots, ydots):
    np.savetxt('x.txt', xdots)
    np.savetxt('y.txt', ydots)
    np.savetxt('x,y.txt', (np.stack([xdots, ydots], axis = 1 )))


def int_input_variable(text):
    print(text)
    variable = int(input())
    return variable


carozzera = Grid()
carozzera.create()
print(carozzera.xdots)
print(carozzera.ydots)
rotate(10,carozzera.xdots,carozzera.ydots)
display(carozzera.xdots,carozzera.ydots)
export(carozzera.xdots,carozzera.ydots)

