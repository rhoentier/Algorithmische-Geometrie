from math import sqrt
import matplotlib.pyplot as plt
import copy
import numpy as np

# Point class
class Point:
    def __init__(self, x_init, y_init, name_init):
        self.x = x_init
        self.y = y_init
        self.name = name_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def distance(self, otherPoint):
        return sqrt((self.x - otherPoint.x) ** 2 + (self.y - otherPoint.y) ** 2)

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    def type(self):
        return "Point"

    def plot(self, **kwargs):
        col = kwargs.get("col", "skyblue")
        pos = kwargs.get('pos', [1, 1])
        marker = kwargs.get('marker', "o")
        size = kwargs.get("size", 30)

        col = np.random.rand(3,)

        plt.scatter(self.x, self.y, color = col, s = size, marker = marker, zorder=6)

        delta = 0.25
        plt.annotate(self.name, (self.x + pos[0] * delta, self.y + pos[0] * delta), ha = "center", va = "center", color = col, zorder = 11)

    def copy(self, name_new):
        tmp = copy.deepcopy(self)
        tmp.name = name_new
        return tmp

    def equal(self, otherPoint):
        delta = 0.01
        if self.x == otherPoint.x and self.y == otherPoint.y:
            return True

        if self.distance(otherPoint) < delta:
            return True

        return False

    def notEqual(self, otherPoint):
        return not self.equal(otherPoint)