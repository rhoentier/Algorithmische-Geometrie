from objects import point

# Site class (inherit from Point)
class Site(point.Point):
    def __init__(self, x_init, y_init, name_init, c_init):
        self.x = x_init
        self.y = y_init
        self.name = name_init
        self.c = c_init
        self.areaRequired = 0.0

    def __repr__(self):
        return "".join(["Site(", str(self.x), ",", str(self.y), ",", str(self.c), ")"])

    def type(self):
        return "Site"