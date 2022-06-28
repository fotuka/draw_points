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
        xgap = (x / (xline - 1))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline - 1))  # расстояние между перекладинами по горизонтали
        for i in np.arange(0, y + ygap, ygap):  # i=y
            for j in np.arange(0, x + ygap, xgap):  # j=x
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
        xgap = (x / (xline - 1))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline - 1))  # расстояние между перекладинами по горизонтали
        k = 0   # сделать как в классе Snow и SnowAdvanced не получилось, там целые числа и они деляется хорошо,
        for i in np.arange(0, y + ygap, ygap):  # i=y а тут дробные и при делении после запятой белиберда возникает и
            k += 1 # четность через шаг не получается отслеживать, поэтому оставил тут счетчик
            for j in np.arange(0, x + ygap, xgap):  # j=x может быть можно как то по другому реализовать но я не придумал
                self.ydots = np.append(self.ydots, [i])  # y  но я не придумал
                if k % 2 == 0:
                    self.xdots = np.append(self.xdots, [j + xgap * 0.5])  # x
                else:
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
        for k in range(0, lines):
            for j in np.arange(gap, radius, gap):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * k))) + (j * math.cos(math.radians(angle * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * k))) - (j * math.sin(math.radians(angle * k)))])
        for k in range(0, lines * 2):
            if k % 2 != 0:
                for j in np.arange(gap * 0.5, radius, gap * 0.5):
                    if j % gap * 0.5 != 0:
                        self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * 0.5 * k))) + (j * math.cos(math.radians(angle * 0.5 * k)))])
                        self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * 0.5 * k))) - (j * math.sin(math.radians(angle * 0.5 * k)))])


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


test = Grid()
test.create()
display(test.xdots,test.ydots,-1,20,-1,20)