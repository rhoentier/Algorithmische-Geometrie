import matplotlib.pyplot as plt

# Line class
class Line:
    def __init__(self, LS_init, LE_init):
        self.LS = LS_init
        self.LE = LE_init

    def length(self):
        return self.LS.distance(self.SE)

    def __repr__(self):
        return "".join(["Line(LS: ", str(self.LS), ", LE: ", str(self.LE), ")"])

    def type(self):
        return "Line"

    def plot(self, **kwargs):

        alpha = kwargs.get('alpha', 1.0)
        color = kwargs.get('color', "g")
        linestyle = kwargs.get('linestyle', "--")
        annotate = kwargs.get("annotate", False)

        if annotate:
            self.LS.plot(pos = [-1, -1], color = color)
            self.LE.plot(pos = [-1, -1], color = color)

        return plt.plot([self.LS.x, self.LE.x], [self.LS.y, self.LE.y], color = color, linestyle = linestyle, zorder=6, alpha = alpha)