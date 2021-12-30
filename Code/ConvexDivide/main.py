import copy
import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.convexpiece import ConvexPolygon
from external import move, numSites, cut
import random
import numpy as np
import time

<<<<<<< Updated upstream
def getRandom_c(num):
    # Returns a list of length <num> with c-values in range 0.01 to 0.99
    # The list containts no duplicates and no 0's. The sum of all elements is 1.0
=======
vid = True
>>>>>>> Stashed changes

    randomlist = random.sample(range(1, 99), num - 1)
    randomlist.append(0)
    randomlist.append(100)
    randomlist.sort()
    for i in range(len(randomlist) - 1):
        randomlist[i] = randomlist[i + 1] - randomlist[i]
    randomlist.pop(-1)
    randomlist = [x / 100 for x in randomlist]
    return randomlist

<<<<<<< Updated upstream
step = 0.005
if __name__ == '__main__':

    # Initialize plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

=======
def getExample(index: int, *args: int) -> ConvexPolygon:
    """
    Takes the predefined ConvexPolygon (see below) and adds random(index == 0) or predefined (index >= 1) sites
    :param index: Integer >= 1 describing specific example / 0 returns a random example (see also next parameter)
    :param args: If index == 0, second Integer must be passed to describe number of random sites
    :return: ConvexPolygon incl. sites
    """

    P_init = ConvexPolygon(V=[Point(8, 9, "V01"),
                        Point(0, 7, "V02"),
                        Point(0, 4, "V03"),
                        Point(2, 0, "V04"),
                        Point(7, 0, "V05"),
                        Point(10, 3, "V06")],
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
        P_init.addSite(Site(1, 2, 0.20, 1))
        P_init.addSite(Site(8, 1, 0.80, 2))
    elif index == 2:
        P_init.addSite(Site(1, 2, 0.70, 1))
        P_init.addSite(Site(8, 1, 0.30, 2))
    elif index == 3:
        P_init.addSite(Site(1, 2, 0.95, 1))
        P_init.addSite(Site(8, 1, 0.05, 2))
    elif index == 4:
        P_init.addSite(Site(0, 5, 0.05, 1))
        P_init.addSite(Site(1, 2, 0.38, 2))
        P_init.addSite(Site(3, 0, 0.50, 3))
        P_init.addSite(Site(8, 1, 0.07, 4))
    elif index == 5:
        P_init.addSite(Site(6, 8.5, 0.15, 1))
        P_init.addSite(Site(1, 7.25, 0.20, 5))
        P_init.addSite(Site(0, 6, 0.08, 3))
        P_init.addSite(Site(0, 5, 0.04, 2))
        P_init.addSite(Site(1, 2, 0.27, 4))
        P_init.addSite(Site(1.5, 1, 0.02, 6))
        P_init.addSite(Site(5, 0, 0.01, 7))
        P_init.addSite(Site(9, 2, 0.04, 10))
        P_init.addSite(Site(9.333333, 5, 0.12, 9))
        P_init.addSite(Site(8.333333, 8, 0.07, 8))
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

>>>>>>> Stashed changes
    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.xticks(np.arange(-1, 12, step=1))
    plt.yticks(np.arange(-1, 12, step=1))
    plt.grid(zorder=0)
<<<<<<< Updated upstream
    ax.set_xlabel('x-Achse')
    ax.set_ylabel('y-Achse')

    num = 9
    random_c = getRandom_c(num)

    P_init = Problem(V=[Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 4, "P3"), Point(2, 0, "P4"), Point(7, 0, "P5"),
                        Point(10, 3, "P6")], S=[])

    #for i in range(num):
    #    P_init.addRandomSite(random_c.pop())

    # img1
    # P_init.addSite(Site(1, 2, 0.20))
    # P_init.addSite(Site(8, 1, 0.80))

    # img2
    # P_init.addSite(Site(1, 2, 0.70))
    # P_init.addSite(Site(8, 1, 0.30))

    # img3
    # P_init.addSite(Site(1, 2, 0.95))
    # P_init.addSite(Site(8, 1, 0.05))

    # serie
    # P_init.addSite(Site(4, 8, 0.30))
    # P_init.addSite(Site(0, 5, 0.20))
    # P_init.addSite(Site(3, 0, 0.35))
    # P_init.addSite(Site(9, 2, 0.15))

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

    P_init.calcArea()

    P_init.plotV(color="skyblue")
    [s.plot(marker="x", size=70) for s in P_init.S]  # Plot sites
    plt.savefig('polygon.png')

    for s in P_init.S:
        print(s)

    openProblems = []
    finishedProblems = []
    openProblems.append(P_init)
    pl = 0
    while len(openProblems) > 0:   # As long as there are Problems with more than one Site
        print(pl)
        pl += 1
        P = openProblems.pop()

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
        PrL = Problem(V = V_PrL, S = [S[0]])

        # Move line CCW from point to point

        prlarea = PrL.area()
        prlreq = PrL.requiredArea()




=======

def ConvexDivide(CP, num):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)

    initPlot()                      # Initialize plot
    CP.plotV()  # Plot vertices and edges of CP
    CP.plotS()  # Plot sites of CP

    if vid:
        plt.savefig('sub_' + str(num) + '_' + str(0) + '.png')  # output

    # Initialize line segment L
    LS = Point(CP.W[0].x, CP.W[0].y, "LS")      # LS at first element of list W
    k0 = CP.indexOfFirstSiteInW()
    LE = Point(CP.S[0].x, CP.S[0].y, "LE")      # LE at first site in list W
    if vid:
        L = Line(LS, LE)
        L.plot(color="royalblue", linestyle="dotted", annotate=True)
        plt.savefig('sub_' + str(num) + '_' + str(1) + '.png')  # output

    # Initial partitioning with initialized line
    V_PrL = cut(CP.V, LS, LE)
    PrL = ConvexPolygon(V=V_PrL, S=[CP.S[0]])

    # Move LE CCW from point to point if PrL is area-incomplete
    k = 0
    while PrL.area() < PrL.requiredArea() and LE.notEqual(CP.S[-1]):
        if k > 0 and CP.W[k0 + k].type() == "Site":
            PrL.appendSite(CP.W[k0 + k])
        k += 1
        LE = Point(CP.W[k0 + k].x, CP.W[k0 + k].y, "LE")
        PrL.appendPoint(CP.W[k0 + k])

    if vid:
        L = Line(LS, LE)
        L.plot(color="royalblue", linestyle="--", annotate=True)
        plt.savefig('sub_' + str(num) + '_' + str(2) + '.png')

    # Move LS/LE incrementally until area requirement is fulfilled
    iimg = 3
    if LE.equal(CP.S[0]) and PrL.area() > PrL.requiredArea():
        # Case 1: PrL too big from the beginning, Move LS CCW until PrL is small enough to fulufill requirement
        while PrL.area() > PrL.requiredArea():
            LS = move(LS, CP.V, "CCW", step)
            V_PrL = cut(CP.V, LS, LE)
            PrL = ConvexPolygon(V=V_PrL, S=PrL.S)
            if vid:
                ax.plot([LS.x, LE.x], [LS.y, LE.y], color = "royalblue")
                plt.savefig('sub_' + str(num) + '_' + str(iimg) + '.png')
                ax.lines.pop()
                iimg += 1
    elif LE.equal(CP.S[-1]) and PrL.area() < PrL.requiredArea():
        # Case 2: PrL is too small and LE reached last site, Move LS CW until PrL is big enough to fulfill requirement
        while PrL.area() < PrL.requiredArea():
            LS = move(LS, CP.V, "CW", step)
            V_PrL = cut(CP.V, LS, LE)
            PrL = ConvexPolygon(V=V_PrL, S=PrL.S)
            if vid:
                ax.plot([LS.x, LE.x], [LS.y, LE.y], color = "royalblue")
                plt.savefig('sub_' + str(num) + '_' + str(iimg) + '.png')
                ax.lines.pop()
                iimg += 1
    else:
        # Case 3: PrL over-fulfills requirement. Move LE CW (backwards) until area below requirement
        while PrL.area() > PrL.requiredArea():
            LE = move(LE, CP.V, "CW", step)
            V_PrL = cut(CP.V, LS, LE)
            PrL = ConvexPolygon(V=V_PrL, S=PrL.S)
            if vid:
                ax.plot([LS.x, LE.x], [LS.y, LE.y], color = "royalblue", zorder=110)            # draw
                plt.savefig('sub_' + str(num) + '_' + str(iimg) + '.png')   # output
                ax.lines.pop()                                              # remove
                iimg += 1

    V_PrL, V_PlL = cut(CP.V, LS, LE, direction = "both")

    PrL = ConvexPolygon(V=V_PrL, S=PrL.S)
    PlL = ConvexPolygon(V=V_PlL, S=CP.S[len(PrL.S):])

    if vid:
        L = Line(LS, LE)
        L.plot(color="red", linestyle="-", annotate=True)
        plt.savefig('sub_' + str(num) + '_' + str(iimg) + '.png')

    if PrL.numSites() > 1:
        num += 1
        #plt.clf()
        #PlL.plotV(color="silver")
        ConvexDivide(PrL, num)

    if PlL.numSites() > 1:
        num += 1
        #plt.clf()
        #PrL.plotV(color="silver")
        ConvexDivide(PlL, num)

step = 0.01
if __name__ == '__main__':
    # fig = plt.figure(figsize=(30, 10))


    CP = getExample(4)              # Get predefined or random example
>>>>>>> Stashed changes

        k = 0
        while PrL.area() < PrL.requiredArea() and LE.notEqual(S[-1]):
            if k > 0 and W[k0 + k].type() == "Site":

                PrL.appendSite(W[k0 + k])
            k += 1
            LE = Point(W[k0 + k].x, W[k0 + k].y, "LE")
            PrL.appendPoint(W[k0 + k])

            prlarea = PrL.area()
            prlreq = PrL.requiredArea()

        #L = Line(LS, LE)
        #L.plot(col="grey")

        if LE.equal(S[0]) and PrL.area() > PrL.requiredArea():
            while PrL.area() > PrL.requiredArea():
                LS = move(LS, V, "CCW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)
        elif LE.equal(S[-1]) and PrL.area() < PrL.requiredArea():
            while PrL.area() < PrL.requiredArea():
                LS = move(LS, V, "CW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)
        else:
            while PrL.area() > PrL.requiredArea():
                LE = move(LE, V, "CW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)

        V_PrL, V_PlL = cut(V, LS, LE)

        P1 = Problem(V = V_PrL, S = PrL.S)
        P2 = Problem(V = V_PlL, S = S[len(PrL.S):])

        openProblems.append(P1) if P1.numSites() > 1 else finishedProblems.append(P1)
        openProblems.append(P2) if P2.numSites() > 1 else finishedProblems.append((P2))

        L = Line(LS, LE)
        L.plot()

<<<<<<< Updated upstream
        # Save figure
        plt.savefig('polygon.png')
        plt.savefig('polygon' + str(pl) + '.png')
=======
    # plt.subplot(1, 3, 1)
    ConvexDivide(CP, 1)

    # plt.savefig('polygon.png')
>>>>>>> Stashed changes
