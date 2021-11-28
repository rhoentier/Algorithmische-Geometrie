import numpy as np
import matplotlib.pyplot as plt

# Polygon class
class Polygon:
    def __init__(self, arr_init):
        self.points = arr_init

    def area(self):
        x = [p.x for p in self.points]
        y = [p.y for p in self.points]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def __repr__(self):
        return "".join(["Line(LS: ", str(self.LS), ", LE: ", str(self.LE), ")"])

    def type(self):
        return "Line"

    def plot(self, **kwargs):

        color = kwargs.get('color', "k")

        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        xs.append(xs[0])
        ys.append(ys[0])
        plt.plot(xs, ys, color = color, zorder=5)

        for p in self.points:
            p.plot(color)

