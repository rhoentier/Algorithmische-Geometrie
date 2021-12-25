import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.problem import Problem
from external import move, numSites, cut
import random
import numpy as np

# To do list:
# Rename P_init
# Rename Problem

def getRandom_c(n: int):
    """
    Calculates a list of n random 2-digit-decimals < 1.0, which sum up to 1.0, e.g. getRandom_c(3) -> [0.21, 0.29, 0.40]
    Value of each element is minimum 0.01 and maximum 0.99. The list contains no duplicates and no 0's
    :param n: Number of decimals to be be calulated (min value 2)
    :return: Array with n random 2-digit-decimals, which sum up to 1.0
    """

    if n <= 1:
        print("Parameter n for function getRandom_c(n) must be >= 2")
        exit()

    # Create a list [0, ... n-1 random integers between 1 and 99 ..., 100]
    randomlist = random.sample(range(1, 99), n - 1)
    randomlist.append(0)
    randomlist.append(100)
    randomlist.sort()
    # Determine distances between elements
    for i in range(len(randomlist) - 1):
        randomlist[i] = randomlist[i + 1] - randomlist[i]
    randomlist.pop(-1)
    randomlist = [x / 100 for x in randomlist]

    return randomlist

def getExample(index: int, *args: int) -> Problem:
    """
    Takes the predefined ConvexPolygon (see below) and adds random(index == 0) or predefined (index >= 1) sites
    :param index: Integer >= 1 describing specific example / 0 returns a random example (see also next parameter)
    :param args: If index == 0, second Integer must be passed to describe number of random sites
    :return: ConvexPolygon incl. sites
    """

    P_init = Problem(V=[Point(8, 9, "P1"),
                        Point(0, 7, "P2"),
                        Point(0, 4, "P3"),
                        Point(2, 0, "P4"),
                        Point(7, 0, "P5"),
                        Point(10, 3, "P6")],
                     S=[])

    # get random example with index == 0
    if index == 0:
        if args:
            num = args[0]
            random_c = getRandom_c(num)
            for i in range(num):
                P_init.addRandomSite(random_c.pop())
        else:
            print("Function getExample(0) must provide second argument describing number of random sites (int)")
            exit()
        pass

    # get specific example with index >= 1 from here downwards
    elif index == 1:
        # img1
        P_init.addSite(Site(1, 2, 0.20))
        P_init.addSite(Site(8, 1, 0.80))
    elif index == 2:
        # img2
        P_init.addSite(Site(1, 2, 0.70))
        P_init.addSite(Site(8, 1, 0.30))
    elif index == 3:
        # img3
        P_init.addSite(Site(1, 2, 0.95))
        P_init.addSite(Site(8, 1, 0.05))
    elif index == 4:
        # serie
        P_init.addSite(Site(4, 8, 0.30))
        P_init.addSite(Site(0, 5, 0.20))
        P_init.addSite(Site(3, 0, 0.35))
        P_init.addSite(Site(9, 2, 0.15))
    elif index == 5:
        # example
        P_init.addSite(Site(6, 8.5, 0.15))
        P_init.addSite(Site(1, 7.25, 0.20))
        P_init.addSite(Site(0, 6, 0.08))
        P_init.addSite(Site(0, 5, 0.04))
        P_init.addSite(Site(1, 2, 0.27))
        P_init.addSite(Site(1.5, 1, 0.02))
        P_init.addSite(Site(5, 0, 0.01))
        P_init.addSite(Site(9, 2, 0.04))
        P_init.addSite(Site(9.333333, 5, 0.12))
        P_init.addSite(Site(8.333333, 8, 0.07))
    else:
        print("getExample(" + str(index) + "), Index out of range. No example defined.")
        exit()

    P_init.calcArea()
    return P_init

def initPlot():
    """
    Initializes Plot
    :return: None
    """

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.xticks(np.arange(-1, 12, step=1))
    plt.yticks(np.arange(-1, 12, step=1))
    plt.grid(zorder=0)
    ax.set_xlabel('x-Achse')
    ax.set_ylabel('y-Achse')

def ConvexDivide(P):
    # Input
    W = P.W
    V = P.V
    S = P.S

    # Create point "LS" at first element of W
    LS = Point(W[0].x, W[0].y, "LS")

    # Find first site in W and create point "LE" there, k0 = index of first site
    for k0, w in enumerate(W):
        if w.type() == "Site":
            LE = Point(w.x, w.y, "LE")
            break

    V_PrL, V_PlL = cut(V, LS, LE)
    PrL = Problem(V=V_PrL, S=[S[0]])

    # Move line CCW from point to point

    prlarea = PrL.area()
    prlreq = PrL.requiredArea()

    k = 0
    while PrL.area() < PrL.requiredArea() and LE.notEqual(S[-1]):
        if k > 0 and W[k0 + k].type() == "Site":
            PrL.appendSite(W[k0 + k])
        k += 1
        LE = Point(W[k0 + k].x, W[k0 + k].y, "LE")
        PrL.appendPoint(W[k0 + k])

        prlarea = PrL.area()
        prlreq = PrL.requiredArea()

    # L = Line(LS, LE)
    # L.plot(col="grey")

    if LE.equal(S[0]) and PrL.area() > PrL.requiredArea():
        while PrL.area() > PrL.requiredArea():
            LS = move(LS, V, "CCW", step)
            V_PrL = cut(V, LS, LE)
            PrL = Problem(V=V_PrL[0], S=PrL.S)
    elif LE.equal(S[-1]) and PrL.area() < PrL.requiredArea():
        while PrL.area() < PrL.requiredArea():
            LS = move(LS, V, "CW", step)
            V_PrL = cut(V, LS, LE)
            PrL = Problem(V=V_PrL[0], S=PrL.S)
    else:
        while PrL.area() > PrL.requiredArea():
            LE = move(LE, V, "CW", step)
            V_PrL = cut(V, LS, LE)
            PrL = Problem(V=V_PrL[0], S=PrL.S)

    V_PrL, V_PlL = cut(V, LS, LE)

    P1 = Problem(V=V_PrL, S=PrL.S)
    P2 = Problem(V=V_PlL, S=S[len(PrL.S):])

    ConvexDivide(P1) if P1.numSites() > 1 else None
    ConvexDivide(P2) if P2.numSites() > 1 else None

    L = Line(LS, LE)
    L.plot()

    # Save figure
    plt.savefig('polygon.png')
    #plt.savefig('polygon' + str(pl) + '.png')

step = 0.005
if __name__ == '__main__':

    initPlot()                      # Initialize plot
    CP = getExample(4)              # Get predefined or random example

    CP.plotV()                      # Plot vertices and edges of CP
    CP.plotS()                      # Plot sites of CP

    CP.print()                      # Output Convex Polygon to console

    ConvexDivide(CP)