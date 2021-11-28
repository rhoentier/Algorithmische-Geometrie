from objects import polygon
import numpy as np

# PL class
class PL(polygon.Polygon):
    def __init__(self, points_init, direction_init, sites_init):
        self.points = points_init
        self.direction = direction_init
        self.sites = sites_init

    def get_PlL(self):
        pass

    def __repr__(self):
        return "".join(["P", self.direction, "L(Area:, ", str(self.area), ", AreaRequired", str(self.areaRequired), ")"])

    def type(self):
        return "PL"

    def plot(self):
        print("Not yet implemented in subclass")
        pass

    def requiredArea(self, P_area):
        return sum([s.c * P_area for s in self.sites])

    def appendPoint(self, p):
        self.points.append(p)

    def appendSite(self, s):
        self.sites.append(s)