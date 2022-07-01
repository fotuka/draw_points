import math
import numpy as np
import matplotlib.pyplot as plt




class Grid:

    def create(self):
        length = int_input_variable("Введите длину ")
        height = int_input_variable("Введите высоту ")
        xline_amount = int_input_variable("Введите кол-во вертикальных перекладин ")
        yline_amount = int_input_variable("Введите кол-во горизонтальных перекладин ")
        self.xy = np.zeros([xline_amount * yline_amount, 2], float)
        xgap = length / xline_amount  # расстояние между перекладинами по вертикали
        ygap = height / yline_amount  # расстояние между перекладинами по горизонтали
        index = 0
        for y in np.arange(0, height, ygap):
            for x in np.arange(0, length, xgap):
                self.xy[index, 0] = x
                self.xy[index, 1] = y
                index += 1


class GridSlope:

    def create(self):
        lenght = int_input_variable("Введите длину ")
        height = int_input_variable("Введите высоту ")
        xline_amount = int_input_variable("Введите кол-во вертикальных перекладин ")
        yline_amount = int_input_variable("Введите кол-во горизонтальных перекладин ")
        self.xy = np.zeros([xline_amount * yline_amount, 2], float)
        xgap = lenght / (xline_amount - 1)  # расстояние между перекладинами по вертикали
        ygap = height / (yline_amount - 1)  # расстояние между перекладинами по горизонтали
        k = 0
        index = 0
        for y in np.arange(0, height + ygap, ygap):
            k += 1
            for x in np.arange(0, lenght + ygap, xgap):
                self.xy[index, 1] = y
                if k % 2 == 0:
                    self.xy[index, 0] = x + xgap * 0.5
                else:
                    self.xy[index, 0] = x
                index += 1


class Snow:

    def create(self):
        radius = int_input_variable("Введите радиус ")
        dots_amount = int_input_variable("Введите количество точек ")
        lines = int_input_variable("Введите количество лучей ")
        gap = radius / dots_amount
        angle = 360 / lines
        self.xy = np.zeros([lines * dots_amount + 1, 2], float)
        index = 1
        for line in range(0, lines):
            for value in np.arange(gap, radius + gap, gap):
                self.xy[index, 1] = value * math.cos(math.radians(angle * line))
                self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * line))
                index += 1


class SnowAdvanced:

    def create(self):
        radius = int_input_variable("Введите радиус ")
        dots_amount = int_input_variable("Введите количество точек ")
        lines = int_input_variable("Введите количество лучей ")
        angle = 360 / lines
        gap = radius / dots_amount
        self.xy = np.zeros([lines * 2 * dots_amount + 1, 2], float)
        index = 1
        for line in np.arange(0, lines * 2, 1):
            if line % 2 == 0:
                for value in np.arange(gap, radius + gap, gap):
                    self.xy[index, 1] = value * math.cos(math.radians(angle * line/2))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * line/2))
                    index += 1
            if line % 2 != 0:
                for value in np.arange(gap * 0.5, radius, gap):
                    self.xy[index, 1] = value * math.cos(math.radians(angle * 0.5 * line))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * 0.5 * line))
                    index += 1



def rotate(degree, xy):
    for i in range(len(xy)):
        xy[i, 0] = (xy[i, 0] * math.cos(math.radians(degree))) - (xy[i, 1] * math.sin(math.radians(degree)))
        xy[i, 1] = (xy[i, 0] * math.sin(math.radians(degree))) + (xy[i, 1] * math.cos(math.radians(degree)))
    return xy


def display(xy):
    x, y = np.split(xy, 2, axis=1)
    plt.scatter(x,y)
    plt.show()


def export(xy):
    np.savetxt('x.txt', xy)


def int_input_variable(text):
    variable = int(input(text))
    return variable


def main():
    test = SnowAdvanced()
    test.create()
    display(test.xy)


if __name__ == '__main__':
    main()
