import math
import numpy as np
import matplotlib.pyplot as plt




class Grid:

    def create(self):
        x = int_input_variable("Введите длину ")
        y = int_input_variable("Введите высоту ")
        xline = int_input_variable("Введите кол-во вертикальных перекладин ")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин ")
        self.xy = np.zeros([xline * yline, 2], float)
        xgap = x / xline  # расстояние между перекладинами по вертикали
        ygap = y / yline  # расстояние между перекладинами по горизонтали
        index = 0
        for i in np.arange(0, y, ygap):  # i=y
            for j in np.arange(0, x, xgap):  # j=x
                self.xy[index, 0] = j
                self.xy[index, 1] = i
                index += 1


class GridSlope:

    def create(self):
        x = int_input_variable("Введите длину ")
        y = int_input_variable("Введите высоту ")
        xline = int_input_variable("Введите кол-во вертикальных перекладин ")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин ")
        self.xy = np.zeros([xline * yline, 2], float)
        xgap = x / (xline - 1)  # расстояние между перекладинами по вертикали
        ygap = y / (yline - 1)  # расстояние между перекладинами по горизонтали
        k = 0
        index = 0
        for i in np.arange(0, y + ygap, ygap):
            k += 1
            for j in np.arange(0, x + ygap, xgap):
                self.xy[index, 1] = i  # y
                if k % 2 == 0:
                    self.xy[index, 0] = j + xgap * 0.5  # x
                else:
                    self.xy[index, 0] = j  # x
                index += 1


class Snow:

    def create(self):
        radius = int_input_variable("Введите радиус ")
        gap = int_input_variable("Введите Расстояние между точками ")
        lines = int_input_variable("Введите кол-во лучей ")
        angle = 360 / lines
        self.xy = np.zeros([lines * ( radius // gap  ) + 1, 2], float)
        index = 1
        for k in range(0, lines):
            for j in np.arange(gap, radius + 0.001, gap):
                self.xy[index, 0] = j * math.cos(math.radians(angle * k))
                self.xy[index, 1] = 0 - j * math.sin(math.radians(angle * k))
                index += 1


class SnowAdvanced:

    def create(self):
        radius = int_input_variable("Введите радиус ")
        gap = int_input_variable("Введите Расстояние между точками ")
        lines = int_input_variable("Введите кол-во лучей ")
        angle = 360 / lines
        self.xy = np.zeros([lines * 2 * ( radius // gap  ) + 1, 2], float)
        index = 0
        for k in np.arange(0, lines * 2, 1):
            if k % 2 == 0:
                for j in np.arange(gap, radius + 0.0001, gap):
                    self.xy[index, 1] = j * math.cos(math.radians(angle * k/2))
                    self.xy[index, 0] = 0 - j * math.sin(math.radians(angle * k/2))
                    index += 1
            if k % 2 != 0:
                for j in np.arange(gap * 0.5, radius + 0.0001, gap):
                    self.xy[index, 1] = j * math.cos(math.radians(angle * 0.5 * k))
                    self.xy[index, 0] = 0 - j * math.sin(math.radians(angle * 0.5 * k))
                    index += 1



def rotate(degree, xy):
    for i in range(len(xy)):
        xy[i, 0] = (xy[i, 0] * math.cos(math.radians(degree))) - (xy[i, 1] * math.sin(math.radians(degree)))
        xy[i, 1] = (xy[i, 0] * math.sin(math.radians(degree))) + (xy[i, 1] * math.cos(math.radians(degree)))
    return xy


def display(xy, xmin=0, xmax=0, ymin=0, ymax=0):
    x, y = np.split(xy, 2, axis=1)
    plt.scatter(x,y)
    if (xmin or xmax or ymin or ymax) != 0:
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
    plt.show()


def export(xy):
    np.savetxt('x.txt', xy)
    return True


def int_input_variable(text):
    variable = int(input(text))
    return variable


def main():
    test = SnowAdvanced()
    test.create()
    display(test.xy, -10, 10, -10, 10)


if __name__ == '__main__':
    main()