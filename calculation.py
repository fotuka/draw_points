import math
import numpy as np


FULL_ANGLE = 360


class Coordinates:
    def __init__(self):
        self.xy = np.array([])
        self.xy_data = np.array([])

    def rotate(self, degree: float) -> np.ndarray:
        xy_rotated = np.ndarray(shape=np.shape(self.xy), dtype=float)
        for index in range(len(self.xy)):
            xy_rotated[index, 0] = (self.xy[index, 0] * math.cos(math.radians(degree))) - (
                    self.xy[index, 1] * math.sin(math.radians(degree)))
            xy_rotated[index, 1] = (self.xy[index, 0] * math.sin(math.radians(degree))) + (
                    self.xy[index, 1] * math.cos(math.radians(degree)))
        return xy_rotated

    def move(self, x: float, y: float) -> np.ndarray:
        xy_moved = self.xy
        for index in range(len(self.xy)):
            xy_moved[index, 0] = self.xy[index, 0] + x
            xy_moved[index, 1] = self.xy[index, 1] + y
        return xy_moved

    def concatenate(self):
        self.xy = np.concatenate((self.xy_data, self.xy), axis=1)

    def export(self, path: str) -> None:
        np.savetxt(path, self.xy)
    def port_amount(self):
        port_amount = len(self.port_numbers)
        return port_amount

class Ports(Coordinates):
    def __init__(self, numbers: list, x: list, y: list):
        super().__init__()
        self.port_numbers = numbers
        self.port_y = y
        self.port_x = x

class Rectangle(Coordinates):
    def __init__(self, length: float, height: float, xline_amount: int, yline_amount: int):
        super().__init__()
        self.length = length
        self.height = height
        self.xline_amount = xline_amount
        self.yline_amount = yline_amount
        self.xy = np.zeros([self.xline_amount * self.yline_amount, 2], float)
        self.xy_data = np.zeros([self.xline_amount * self.yline_amount, 1], int)
        self.xgap = self.length / (self.xline_amount - 1)  # gap between vertical lines
        self.ygap = self.height / (self.yline_amount - 1)  # gap between horizontal lines


class Grid(Rectangle):
    def create(self):
        index = 0
        for y in np.arange(0, self.height + self.ygap, self.ygap):
            for x in np.arange(0, self.length + self.xgap, self.xgap):
                self.xy[index, 0] = x
                self.xy[index, 1] = y
                index += 1


class GridSlope(Rectangle):
    def create(self):
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
    def __init__(self, radius: float, dots_amount: int, lines_amount: int):
        super().__init__()
        self.ports_amount = self.port_amount()
        self.radius = radius
        self.dots_amount = dots_amount
        self.lines_amount = lines_amount
        self.xy = np.zeros([lines_amount * dots_amount, 2], float)
        self.xy_data = np.zeros([lines_amount * dots_amount, 1], int)
        self.gap = self.radius / self.dots_amount
        self.angle = FULL_ANGLE / self.lines_amount


class Snow(Circle):
    def create(self):
        index = 0
        for line in range(self.lines_amount):
            buffer = self.ports_amount + line + 1
            for value in np.arange(self.gap, self.radius + self.gap, self.gap):
                self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                self.xy[index, 0] = value * math.sin(math.radians(self.angle * line))
                self.xy_data[index, 0] = buffer
                buffer += self.lines_amount
                index += 1


class SnowAdvanced(Circle):
    def create(self):
        index = 0
        buffer = self.ports_amount + 1
        line = 0
        for value in np.arange(self.gap, self.radius + self.gap, self.gap / 2):
            for count in range(0, int(self.lines_amount/2), 1):
                self.xy[index, 1] = value * math.cos(math.radians(self.angle * line))
                self.xy[index, 0] = value * math.sin(math.radians(self.angle * line))
                self.xy_data[index, 0] = buffer
                buffer += 1
                line += 2
                index += 1
            line -= 1
