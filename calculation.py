import math
import numpy as np


FULL_ANGLE = 360


class Coordinates:
    def __init__(self) -> 'Initializing array':
        self.xy = np.array([])

    def create(self) -> 'Creating an array of points':
        pass

    def rotate(self, degree: 'Angle of rotation (float)') -> 'np.ndarray':
        for index in range(len(self.xy)):
            self.xy[index, 0] = (self.xy[index, 0] * math.cos(math.radians(degree))) - (self.xy[index, 1] * math.sin(math.radians(degree)))
            self.xy[index, 1] = (self.xy[index, 0] * math.sin(math.radians(degree))) + (self.xy[index, 1] * math.cos(math.radians(degree)))
        return self.xy

    def move_x(self, x: 'Distance (float)') -> 'Moved array along x':
        for index in range(len(self.xy)):
            self.xy[index, 0] = self.xy[index, 0] + x
        return self.xy

    def move_y(self, y: 'Distance (float)') -> 'Moved array along y':
        for index in range(len(self.xy)):
            self.xy[index, 1] = self.xy[index, 1] + y
        return self.xy

    def export(self, path: 'Path to folder (str)') -> 'Saves array to folder':
        np.savetxt(path, self.xy)
        self.xy.tofile('path', sep=' ')


class Rectangle(Coordinates):
    def __init__(self,
                 length: 'Length of rectangle (float)',
                 height: 'Height of rectangle (float)',
                 xline_amount: 'Amount of horizontal lines (int)',
                 yline_amount: 'Amount of vertical lines (int)') -> 'Initializing an empty rectangle array of points':
        super().__init__()
        self.length = length
        self.height = height
        self.xline_amount = xline_amount
        self.yline_amount = yline_amount
        self.xy = np.zeros([self.xline_amount * self.yline_amount, 2], float)
        self.xgap = self.length / (self.xline_amount - 1)  # gap between vertical lines
        self.ygap = self.height / (self.yline_amount - 1)  # gap between horizontal lines


class Grid(Rectangle):
    def create(self) -> 'Creating an array of points':
        index = 0
        for y in np.arange(0, self.height + self.ygap, self.ygap):
            for x in np.arange(0, self.length + self.xgap, self.xgap):
                self.xy[index, 0] = x
                self.xy[index, 1] = y
                index += 1


class GridSlope(Rectangle):
    def create(self) -> 'Creating an array of points':
        self.xgap = self.length / (self.xline_amount - 1)  # gap between vertical lines
        self.ygap = self.height / (self.yline_amount - 1)  # gap between horizontal lines
        k = 0
        index = 0
        for y in np.arange(0, self.height + self.ygap, self.ygap):
            k += 1
            for x in np.arange(0, self.length + self.xgap, self.xgap):
                self.xy[index, 1] = y
                if k % 2 == 0:
                    self.xy[index, 0] = x + self.xgap * 0.5
                else:
                    self.xy[index, 0] = x
                index += 1


class Circle(Coordinates):
    def __init__(self,
                 radius: ' Radius of circle (float)',
                 dots_amount: 'Amount of dots on single line (int)',
                 lines_amount: 'Amount of lines (int)') -> 'Initializing an empty circle array of points':
        super().__init__()
        self.radius = radius
        self.dots_amount = dots_amount
        self.lines_amount = lines_amount
        self.xy = np.zeros([lines_amount * dots_amount + 1, 2], float)
        self.gap = self.radius / self.dots_amount
        self.angle = FULL_ANGLE / self.lines_amount


class Snow(Circle):
    def create(self) -> 'Creating an array of points':
        index = 1
        for line in range(0, self.lines_amount):
            for value in np.arange(self.gap, self.radius + self.gap, self.gap):
                self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                self.xy[index, 0] = 0 - value * math.sin(math.radians(self.angle * line))
                index += 1


class SnowAdvanced(Circle):
    def create(self) -> 'Creating an array of points':
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
