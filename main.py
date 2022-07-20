import math
import numpy as np
# import matplotlib.pyplot as plt


FULL_ANGLE = 360


class Coordinates:
    def __init__(self):
        self.xy = np.array([])

    def create(self):
        pass

    def rotate(self, degree):
        for index in range(len(self.xy)):
            self.xy[index, 0] = (self.xy[index, 0] * math.cos(math.radians(degree))) - (self.xy[index, 1] * math.sin(math.radians(degree)))
            self.xy[index, 1] = (self.xy[index, 0] * math.sin(math.radians(degree))) + (self.xy[index, 1] * math.cos(math.radians(degree)))
        return self.xy

    def move_x(self, x):
        for index in range(len(self.xy)):
            self.xy[index, 0] = self.xy[index, 0] + x
        return self.xy

    def move_y(self, y):
        for index in range(len(self.xy)):
            self.xy[index, 1] = self.xy[index, 1] + y
        return self.xy

    # def display(self):
    #     x, y = np.split(self.xy, 2, axis=1)
    #     plt.scatter(x, y)
    #     plt.show()

    def export(self, path):
        np.savetxt(path, self.xy)
        self.xy.tofile('path', sep=' ')

class Rectangle(Coordinates):
    def __init__(self, length, height, xline_amount, yline_amount):
        super().__init__()
        self.length = length
        self.height = height
        self.xline_amount = xline_amount
        self.yline_amount = yline_amount
        self.xy = np.zeros([self.xline_amount * self.yline_amount, 2], float)
        self.xgap = self.length / self.xline_amount  # расстояние между перекладинами по вертикали
        self.ygap = self.height / self.yline_amount  # расстояние между перекладинами по горизонтали


class Grid(Rectangle):
    def create(self):
        index = 0
        for y in np.arange(0, self.height, self.ygap):
            for x in np.arange(0, self.length, self.xgap):
                self.xy[index, 0] = x
                self.xy[index, 1] = y
                index += 1


class GridSlope(Rectangle):
    def create(self):
        self.xgap = self.length / (self.xline_amount - 1)  # расстояние между перекладинами по вертикали
        self.ygap = self.height / (self.yline_amount - 1)  # расстояние между перекладинами по горизонтали
        k = 0
        index = 0
        for y in np.arange(0, self.height + self.ygap, self.ygap):
            k += 1
            for x in np.arange(0, self.length + self.ygap, self.xgap):
                self.xy[index, 1] = y
                if k % 2 == 0:
                    self.xy[index, 0] = x + self.xgap * 0.5
                else:
                    self.xy[index, 0] = x
                index += 1


class Circle(Coordinates):
    def __init__(self, radius, dots_amount, lines_amount):
        super().__init__()
        self.radius = radius
        self.dots_amount = dots_amount
        self.lines_amount = lines_amount
        self.xy = np.zeros([lines_amount * dots_amount + 1, 2], float)
        self.gap = self.radius / self.dots_amount
        self.angle = FULL_ANGLE / self.lines_amount


class Snow(Circle):
    def create(self):
        index = 1
        for line in range(0, self.lines_amount):
            for value in np.arange(self.gap, self.radius + self.gap, self.gap):
                self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                self.xy[index, 0] = 0 - value * math.sin(math.radians(self.angle * line))
                index += 1


class SnowAdvanced(Circle):
    def create(self):
        index = 1
        for line in range(0, self.lines_amount):
            if line % 2 == 0:
                for value in np.arange(self.gap, self.radius + self.gap, self.gap):
                    self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(self.angle * line))
                    index += 1
            if line % 2 != 0:
                for value in np.arange(self.gap * 0.5, self.radius, self.gap):
                    self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                    self.xy[index, 0] = 0 - value * math.sin(math.radians(self.angle * line))
                    index += 1


def main():
    pass
    # test = SnowAdvanced(10, 3, 12)
    # test.create()
    # test.display()
    # test.rotate(0)
    # test.export()


if __name__ == '__main__':
    main()
