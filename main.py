import math
import numpy as np
import matplotlib.pyplot as plt




class Grid():

    def create(self):
        x = int_input_variable("Введите длину")
        y = int_input_variable("Введите высоту")
        xline = int_input_variable("Введите кол-во вертикальных перекладин")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин")
        self.xy = np.zeros([xline * yline, 2], float)
        xgap = (x / (xline))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline))  # расстояние между перекладинами по горизонтали
        kx = 0
        for i in np.arange(0, y, ygap):  # i=y
            for j in np.arange(0, x, xgap):  # j=x
                self.xy[kx, 0] = j
                self.xy[kx, 1] = i
                kx += 1


class GridSlope():

    def create(self):
        x = int_input_variable("Введите длину")
        y = int_input_variable("Введите высоту")
        xline = int_input_variable("Введите кол-во вертикальных перекладин")
        yline = int_input_variable("Введите кол-во горизонтальных перекладин")
        self.xy = np.zeros([xline * yline, 2], float)
        xgap = (x / (xline - 1))  # расстояние между перекладинами по вертикали
        ygap = (y / (yline - 1))  # расстояние между перекладинами по горизонтали
        k = 0
        kx = 0
        for i in np.arange(0, y + ygap, ygap):
            k += 1
            for j in np.arange(0, x + ygap, xgap):
                self.xy[kx, 1] = i  # y
                if k % 2 == 0:
                    self.xy[kx, 0] = j + xgap * 0.5  # x
                else:
                    self.xy[kx, 0] = j  # x
                kx += 1


class Snow():

    def create(self):
        radius = int_input_variable("Введите радиус")
        gap = int_input_variable("Введите Расстояние между точками")
        lines = int_input_variable("Введите кол-во лучей")
        angle = 360 / lines
        self.xdots = np.array([0], float)  # x
        self.ydots = np.array([0], float)  # y
        self.xy = np.zeros([lines * ( radius // gap  ) + 1, 2], float)
        kx = 0
        for k in range(0, lines):
            for j in np.arange(gap, radius + gap, gap):
                self.ydots = np.append(self.ydots, [(0 * math.sin(math.radians(angle * k))) + (j * math.cos(math.radians(angle * k)))])
                self.xdots = np.append(self.xdots, [(0 * math.cos(math.radians(angle * k))) - (j * math.sin(math.radians(angle * k)))])
                self.xy[kx, 0] = j * math.cos(math.radians(angle * k))
                self.xy[kx, 1] = 0 - j * math.sin(math.radians(angle * k))
                kx += 1
        print(np.shape(self.xy))
        print(np.shape(self.xdots))
        print(np.shape(self.ydots))
        print(self.xy)
        print(self.xdots)
        print(self.ydots)


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


def rotate(degree, xy):
    for i in range(len(xy)):
        xy[i, 0] = (xy[i, 0] * math.cos(math.radians(degree))) - (xy[i, 1] * math.sin(math.radians(degree)))
    for i in range(len(xy)):
        xy[i, 1] = (xy[i, 0] * math.sin(math.radians(degree))) + (xy[i, 1] * math.cos(math.radians(degree)))
    return xy


def display(x, y, xmin=0, xmax=0, ymin=0, ymax=0):
    plt.scatter([x], [y])
    if (xmin or xmax or ymin or ymax) != 0:
        plt.xlim([xmin, xmax])
        plt.ylim([ymin, ymax])
    plt.show()


def export(xy):
    np.savetxt('x.txt', xy)
    return True


def int_input_variable(text):
    print(text)
    variable = int(input())
    return variable


def main():
    test = Grid()
    test.create()
    display(test.xdots,test.ydots)


if __name__ == '__main__':
    main()