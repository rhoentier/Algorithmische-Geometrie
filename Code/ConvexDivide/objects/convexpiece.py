import random
import numpy as np
import matplotlib.pyplot as plt
from objects.site import Site

def side(p, LS, LE):
    epsilon = 0.001
    d = (p.x - LS.x)*(LE.y-LS.y)-(p.y-LS.y)*(LE.x-LS.x)
    if d > -epsilon and d < epsilon:
        return "o"
    if d < 0:
        return "l"
    if d > 0:
        return "r"

# Problem class
# A "Problem" is defined as a set of ordered points (V) (a polygon) and a set of sites (S) positioned on the polygon
# The initialization can either be done with W (including points and sites) or separated with V (points) and S (sites)
class ConvexPolygon:
    def __init__(self, **kwargs):
        self.W = kwargs.get('W', None)
        self.V = kwargs.get('V', None)
        self.S = kwargs.get('S', None)

        if self.W != None and self.V == None and self.S == None:    # init with W
            self.V = [x for x in self.W if x.type() == "Point"]
            self.S = [x for x in self.W if x.type() == "Site"]

        elif self.W == None and self.V != None and self.S != None:  # init with V and S
            self.updateW()

        else:
            # not defined
            print("Initialization only with W or (V and S) -> exit")
            exit()

    def numSites(self):
        return len(self.S)

    def normalize(self):
        sum = 0
        for s in self.S:
            sum += s.c

        for s in self.S:
            s.c = s.c / sum

    def area(self):
        x = [p.x for p in self.V]
        y = [p.y for p in self.V]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def requiredArea(self):
        return sum([s.AreaRequired for s in self.S])

    def appendPoint(self, p):
        self.V.append(p)
        self.updateW()

    def appendSite(self, s):
        self.S.append(s)
        self.updateW()

    def renameSites(self):
        i = 1
        for s in self.S:
            s.name = "S" + str(i)
            i += 1

    def updateW(self):
        self.W = []
        for i, v in enumerate(self.V):
            j = (i + 1) % len(self.V)
            self.W.append(self.V[i])
            tmpS = [s for s in self.S if side(s, self.V[i], self.V[j]) == "o"]
            tmpS.sort(key=lambda x: self.V[i].distance(x))
            self.W = self.W + tmpS

    def updateS(self):
        self.S = [x for x in self.W if x.type() == "Site"]

    def plotV(self, **kwargs):

        col = kwargs.get('color', "k")

        xs = [p.x for p in self.V]
        ys = [p.y for p in self.V]

        xs.append(xs[0])
        ys.append(ys[0])
        plt.plot(xs, ys, color = col, zorder=5)

        for p in self.V:
            p.plot()

    def addRandomSite(self, c):
        # Find random segment of polygon
        i = random.randint(0, len(self.V) - 1)
        j = (i + 1) % len(self.V)
        pi = self.V[i]
        pj = self.V[j]
        # Find random position on segment
        dec = random.random()
        x = pi.x + (pj.x - pi.x) * dec
        y = pi.y + (pj.y - pi.y) * dec
        # Create a new Site with random numbers and add it
        self.addSite(Site(x, y, c))

    def addSite(self, s):
        for i, v in enumerate(self.W):
            if v.type() == "Site": passedFirstSite = True
            j = (i + 1) % len(self.W)
            if side(s, self.W[i], self.W[j]) == "o":
                if (s.x >= self.W[i].x and s.x <= self.W[j].x) or (s.x <= self.W[i].x and s.x >= self.W[j].x):
                    self.W.insert(i + 1, s)
                    break
        self.updateS()
<<<<<<< Updated upstream:Code/ConvexDivide/objects/problem.py
        self.renameSites()
        return

    def calcArea(self):
        for s in self.S:
            s.AreaRequired = s.c * self.area()
=======
        #self.renameSites()

    def appendPoint(self, p):
        self.V.append(p)
        self.updateW()

    def appendSite(self, s):

        self.S.append(s)
        self.updateW()

    def area(self):
        # returns area of the polygon
        x = [p.x for p in self.V]
        y = [p.y for p in self.V]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def calcArea(self):
        for s in self.S:
            s.AreaRequired = s.c * self.area()

    def indexOfFirstSiteInW(self):
        for i, w in enumerate(self.W):
           if w.type() == "Site":
               return i

    def numSites(self):
        return len(self.S)

    def plotS(self):
        [s.plot(marker="x", size=70) for s in self.S]

    def plotV(self, **kwargs):
        color = kwargs.get('color', "k")
        zorder = kwargs.get('zorder', 5)

        # build closed polygon
        xs = [p.x for p in self.V]
        ys = [p.y for p in self.V]
        xs.append(xs[0])
        ys.append(ys[0])

        # draw lines
        plt.plot(xs, ys, color = color, zorder=zorder)

        # draw vertices
        for p in self.V:
            p.plot(color = color)

        # draw area to center
        plt.annotate("Area = " + "{:.1f}".format(self.area()), (np.average(xs), np.average(ys)), ha="center", va="center", zorder=11, color = color)

    def print(self):
        print(self)

    def renameSites(self):
        i = 1
        for s in self.S:
            s.name = "S" + str(i)
            i += 1

    def requiredArea(self):
        # returns the required area based on all sites of the polygon
        return sum([s.AreaRequired for s in self.S])

    def updateS(self):
        # updates list S based on list W
        self.S = [x for x in self.W if x.type() == "Site"]

    def updateV(self):
        # updates list V based on list W
        self.V = [x for x in self.W if x.type() == "Point"]

    def updateW(self):
        # updates list W based on list S and V
        self.W = []
        for i, v in enumerate(self.V):
            j = (i + 1) % len(self.V)
            self.W.append(self.V[i])
            tmpS = [s for s in self.S if side(s, self.V[i], self.V[j]) == "o"]
            tmpS.sort(key=lambda x: self.V[i].distance(x))
            self.W = self.W + tmpS
>>>>>>> Stashed changes:Code/ConvexDivide/objects/convexpiece.py
