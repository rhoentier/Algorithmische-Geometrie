import copy
import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.problem import Problem
from external import move, numSites, cut
import random
import numpy as np
import time

def getRandom_c(num):
    # Returns a list of length <num> with c-values in range 0.01 to 0.99
    # The list containts no duplicates and no 0's. The sum of all elements is 1.0

    randomlist = random.sample(range(1, 99), num - 1)
    randomlist.append(0)
    randomlist.append(100)
    randomlist.sort()
    for i in range(len(randomlist) - 1):
        randomlist[i] = randomlist[i + 1] - randomlist[i]
    randomlist.pop(-1)
    randomlist = [x / 100 for x in randomlist]
    return randomlist

step = 0.005
if __name__ == '__main__':

    # Initialize plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.xticks(np.arange(-1, 12, step=1))
    plt.yticks(np.arange(-1, 12, step=1))
    plt.grid(zorder=0)
    ax.set_xlabel('x-Achse')
    ax.set_ylabel('y-Achse')

    num = 9
    random_c = getRandom_c(num)

    P_init = Problem(V=[Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 4, "P3"), Point(2, 0, "P4"), Point(7, 0, "P5"),
                        Point(10, 3, "P6")], S=[])

    for i in range(num):
        P_init.addRandomSite(random_c.pop())

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





        k = 0
        while PrL.area() < PrL.requiredArea() and LE.notEqual(S[-1]):
            if k > 0 and W[k0 + k].type() == "Site":

                PrL.appendSite(W[k0 + k])
            k += 1
            LE = Point(W[k0 + k].x, W[k0 + k].y, "LE")
            PrL.appendPoint(W[k0 + k])

            prlarea = PrL.area()
            prlreq = PrL.requiredArea()

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

        # Save figure
        plt.savefig('polygon.png')
        plt.savefig('polygon' + str(pl) + '.png')
