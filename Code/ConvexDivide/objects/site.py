from objects import point
import matplotlib.pyplot as plt

# Site class (inherit from Point)
class Site(point.Point):
    def __init__(self, x_init, y_init, name_init, c_init):
        self.x = x_init
        self.y = y_init
        self.name = name_init
        self.c = c_init
        self.areaRequired = 0.0

    def __repr__(self):
        return "".join(["Site(", str(self.x), ",", str(self.y), ",", self.name, ",", str(self.c), ")"])

    def type(self):
        return "Site"

    def plot(self, **kwargs):

        pos = kwargs.get('pos', [1, 1])
        marker = kwargs.get('marker', "o")
        size = kwargs.get("size", 30)
        col = kwargs.get("col", "r")
        plt.scatter(self.x, self.y, color = col, s = size, marker = marker, zorder=6)

        delta = 0.25
        plt.annotate(self.name, (self.x + pos[0] * delta, self.y + pos[0] * delta), ha = "center", va = "center", color = col, zorder = 11)
        #plt.annotate(self.name + ", c = " + "{:.2f}".format(self.c), (self.x + pos[0] * delta, self.y + pos[0] * delta), ha = "center", va = "center", color = col, zorder = 11)
