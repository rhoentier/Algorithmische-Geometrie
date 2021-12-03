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

        if self.W != None and self.V == None and self.S == None:
            self.V = [x for x in self.W if x.type() == "Point"]
            self.S = [x for x in self.W if x.type() == "Site"]

        elif self.W == None and self.V != None and self.S != None:

            num_pts = len(self.V)
            tmp = []
            for i, v in enumerate(self.V):
                tmp.append(v)
                for s in self.S:

                    if side(s, v, self.V[(i + 1) % num_pts]) == "o":
                        tmp.append(s)
                        break
            self.W = tmp

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

    def shuffle(self):
        num_pts = len(self.W)
        r = random.randint(0, num_pts)
        print(r)
        print(self.W)
        for i in range(r):
            self.W.append(self.W.pop(0))
        print(self.W)
        print("")
        self.V = [x for x in self.W if x.type() == "Point"]
        self.S = [x for x in self.W if x.type() == "Site"]

    def area(self):
        x = [p.x for p in self.V]
        y = [p.y for p in self.V]
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def requiredArea(self, P_area):
        return sum([s.c * P_area for s in self.S])

    def appendPoint(self, p):
        self.V.append(p)
        self.updateW()

    def appendSite(self, s):
        self.S.append(s)
        self.updateW()

    def updateW(self):
        self.W = []
        for i, v in enumerate(self.V):
            j = (i + 1) % len(self.V)
            self.W.append(self.V[i])
            tmpS = [s for s in self.S if side(s, self.V[i], self.V[j]) == "o"]
            tmpS.sort(key=lambda x: self.V[i].distance(x))
            for s in tmpS:
                self.W.append(s)

    def plotV(self, **kwargs):

        color = kwargs.get('color', "k")

        xs = [p.x for p in self.V]
        ys = [p.y for p in self.V]

        xs.append(xs[0])
        ys.append(ys[0])
        plt.plot(xs, ys, color = color, zorder=5)

        for p in self.V:
            p.plot(color)

    def addRandomSite(self):
        pos = random.randint(0, len(self.V) - 1)

        pi = self.V[pos]
        pj = self.V[(pos + 1) % len(self.V)]

        dec = random.random()
        x = pi.x + (pj.x - pi.x) * dec
        y = pi.y + (pj.y - pi.y) * dec

        dec = random.random()
        self.S.append(Site(x, y, "R", dec))
        self.updateW()

    def addSite(self, s):
        self.S.append(s)
        self.updateW()