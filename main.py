import math
import numpy as np
import matplotlib.pyplot as plt


class Grid:

    def __init__(self, length, height, xline_amount, yline_amount):
        self.length = length
        self.height = height
        self.xline_amount = xline_amount
        self.yline_amount = yline_amount
        self.xy = np.zeros([self.xline_amount * self.yline_amount, 2], float)

    def create(self):
        xgap = self.length / self.xline_amount  # расстояние между перекладинами по вертикали
        ygap = self.height / self.yline_amount  # расстояние между перекладинами по горизонтали
        index = 0
        for y in np.arange(0, self.height, ygap):
            for x in np.arange(0, self.length, xgap):
                self.xy[index, 0] = x
                self.xy[index, 1] = y
                index += 1


class GridSlope:

    def __init__(self, length, height, xline_amount, yline_amount):
        self.length = length
        self.height = height
        self.xline_amount = xline_amount
        self.yline_amount = yline_amount
        self.xy = np.zeros([self.xline_amount * self.yline_amount, 2], float)

    def create(self):
        xgap = self.length / (self.xline_amount - 1)  # расстояние между перекладинами по вертикали
        ygap = self.height / (self.yline_amount - 1)  # расстояние между перекладинами по горизонтали
        k = 0
        index = 0
        for y in np.arange(0, self.height + ygap, ygap):
            k += 1
            for x in np.arange(0, self.length + ygap, xgap):
                self.xy[index, 1] = y
                if k % 2 == 0:
                    self.xy[index, 0] = x + xgap * 0.5
                else:
                    self.xy[index, 0] = x
                index += 1


class Snow:

    def __init__(self, radius, dots_amount, lines_amount):
        self.radius = radius
        self.dots_amount = dots_amount
        self.lines_amount = lines_amount
        self.xy = np.zeros([lines_amount * dots_amount + 1, 2], float)

    def create(self):
        gap = self.radius / self.dots_amount
        angle = 360 / self.lines_amount
        index = 1
        for line in range(0, self.lines_amount):
            for value in np.arange(gap, self.radius + gap, gap):
                self.xy[index, 1] = value * math.cos(math.radians(angle * line))
                self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * line))
                index += 1


class SnowAdvanced:

    def __init__(self, radius, dots_amount, lines_amount):
        self.radius = radius
        self.dots_amount = dots_amount
        self.lines_amount = lines_amount
        self.xy = np.zeros([lines_amount * dots_amount + 1, 2], float)

    def create(self):
        angle = 360 / self.lines_amount
        gap = self.radius / self.dots_amount
        index = 1
        for line in np.arange(0, self.lines_amount * 2, 1):
            if line % 2 == 0:
                for value in np.arange(gap, self.radius + gap, gap):
                    self.xy[index, 1] = value * math.cos(math.radians(angle * line/2))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * line/2))
                    index += 1
            if line % 2 != 0:
                for value in np.arange(gap * 0.5, self.radius, gap):
                    self.xy[index, 1] = value * math.cos(math.radians(angle * 0.5 * line))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(angle * 0.5 * line))
                    index += 1


def rotate(degree, xy):
    for index in range(len(xy)):
        xy[index, 0] = (xy[index, 0] * math.cos(math.radians(degree))) - (xy[index, 1] * math.sin(math.radians(degree)))
        xy[index, 1] = (xy[index, 0] * math.sin(math.radians(degree))) + (xy[index, 1] * math.cos(math.radians(degree)))
    return xy


def display(xy):
    x, y = np.split(xy, 2, axis=1)
    plt.scatter(x, y)
    plt.show()


def export(dots_massive):
    np.savetxt('xy.txt', dots_massive)


def main():
    test = GridSlope(10, 5, 3, 2)
    test.create()
    display(test.xy)


if __name__ == '__main__':
    main()
