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
class Problem:
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

    #def __str__(self):
        # to be done, should output a nice representation with vertices and sites >
        #return str(self)
        #pass

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
            j = (i + 1) % len(self.W)
            if side(s, self.W[i], self.W[j]) == "o":
                if (s.x >= self.W[i].x and s.x <= self.W[j].x) or (s.x <= self.W[i].x and s.x >= self.W[j].x):
                    self.W.insert(i + 1, s)
                    break
        self.updateS()
        self.renameSites()
        return
    def appendPoint(self, p):
        self.V.append(p)
        self.updateW()

    def appendSite(self, s):
        self.S.append(s)
        self.updateW()
    def area(self):
        x = [p.x for p in self.V]
        y = [p.y for p in self.V]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def calcArea(self):
        for s in self.S:
            s.AreaRequired = s.c * self.area()

    def numSites(self):
        return len(self.S)

    def plotS(self):
        [s.plot(marker="x", size=70) for s in self.S]

    def plotV(self):

        xs = [p.x for p in self.V]
        ys = [p.y for p in self.V]

        xs.append(xs[0])
        ys.append(ys[0])

        plt.plot(xs, ys, color = "skyblue", zorder=5)

        for p in self.V:
            p.plot()

    def print(self):
        print(self)

    def renameSites(self):
        i = 1
        for s in self.S:
            s.name = "S" + str(i)
            i += 1

    def requiredArea(self):
        return sum([s.AreaRequired for s in self.S])

    def updateS(self):
        self.S = [x for x in self.W if x.type() == "Site"]

    def updateW(self):
        self.W = []
        for i, v in enumerate(self.V):
            j = (i + 1) % len(self.V)
            self.W.append(self.V[i])
            tmpS = [s for s in self.S if side(s, self.V[i], self.V[j]) == "o"]
            tmpS.sort(key=lambda x: self.V[i].distance(x))
            self.W = self.W + tmpS