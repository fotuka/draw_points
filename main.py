from setuptools import setup
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
        radius = int_input_variable("Введите радиус")
        gap = int_input_variable("Введите Расстояние между точками")
        lines = int_input_variable("Введите кол-во лучей")
        angle = 360 / lines
        self.xdots = np.array([0], float)  # x
        self.ydots = np.array([0], float)  # y
        for k in range(0, lines):
            for j in np.arange(gap, radius, gap):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * k))) + (j * math.cos(math.radians(angle * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * k))) - (j * math.sin(math.radians(angle * k)))])


class SnowAdvanced():

    def create(self):
        radius = int_input_variable("Введите радиус")
        gap = int_input_variable("Введите Расстояние между точками")
        lines = int_input_variable("Введите кол-во лучей")
        angle = 360 / lines
        self.xdots = np.array([0], float)  # x
        self.ydots = np.array([0], float)  # y
        pop = -1
        ror = 1
        for k in range(0, lines):
            for j in np.arange(gap, radius, gap):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * k))) + (j * math.cos(math.radians(angle * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * k))) - (j * math.sin(math.radians(angle * k)))])
        for k in range(0, lines * 2):
            ror = ror * -1
            if ror == 1:
                for j in np.arange(gap * 0.5, radius, gap * 0.5):
                    pop = pop * -1
                    if pop == 1:
                        self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * 0.5 * k))) + (j * math.cos(math.radians(angle * 0.5 * k)))])
                        self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * 0.5 * k))) - (j * math.sin(math.radians(angle * 0.5 * k)))])
                pop = -1


def rotate(degree, xdots, ydots):
    x = np.array([], float)
    y = np.array([], float)
    for i in range(len(xdots)):
        x = np.append(x, [(xdots[i] * math.cos(math.radians(degree))) - (ydots[i] * math.sin(math.radians(degree)))])
    for i in range(len(ydots)):
        y = np.append(y, [(xdots[i] * math.sin(math.radians(degree))) + (ydots[i] * math.cos(math.radians(degree)))])
    # carozzera.xdots = x
    # carozzera.ydots = y


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


test = Snow()
test.create()
display(test.xdots,test.ydots,-20,20,-20,20)