import copy
import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.problem import Problem
from external import move, numSites, cut
import random
import numpy as np

step = 0.001
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

    P_init = Problem(V=[Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 4, "P3"), Point(2, 0, "P4"), Point(7, 0, "P5"), Point(10, 3, "P6")], S=[])
    num = 5
    while num > 0:
        P_init.addRandomSite()
        num -= 1

#    P_init.addSite(Site(4, 8, "S1", 0.6))
#    P_init.addSite(Site(0, 5, "S3", 0.1))
#    P_init.addSite(Site(9, 6, "S2", 0.4))

    #P_init = Problem(V=[Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 4, "P3")], S=[Site(3.9128,7.9782,"xx", 0.180), Site(0.7864, 7.1966,"xx", 0.04230), Site(0, 5.02371, "xx", 0.1694)])
    #P_init = Problem(V=[Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 5.3037, "P3")], S=[Site(3.9128, 7.9782, "xx", 0.0971), Site(0.7864, 7.1966, "xx", 0.1902)])

    P_init.normalize()

    for s in P_init.S:
        print(s)

    openProblems = []
    finishedProblems = []
    openProblems.append(P_init)

    while len(openProblems) > 0:   # As long as there are Problems with more than one Site

        P = openProblems.pop()

        # Input
        W = P.W
        V = P.V
        S = P.S

        [s.plot("r", marker="x", size=70) for s in S]   # Plot sites
        P.plotV(color = "skyblue")
        #plt.savefig('polygon.png')
        LS = W[0].copy("LS")

        # Find first site in W and copy it to new point "LE", k0 = index of first site
        k0 = 0
        for w in W:
            if w.type() == "Site":
                LE = w.copy("LE")
                break
            k0 += 1              # index of first site

        V_PrL, V_PlL = cut(V, LS, LE)
        PrL = Problem(V = V_PrL, S = [S[0]])

        # Move line CCW from point to point

        prlarea = PrL.area()
        prlreq = PrL.requiredArea(P.area())

        k = 0
        while PrL.area() < PrL.requiredArea(P.area()) and LE.notEqual(S[-1]):
            if k > 0 and W[k0 + k].type() == "Site":

                PrL.appendSite(W[k0 + k])
            k += 1
            LE = W[k0 + k].copy("LE")
            PrL.appendPoint(W[k0 + k])

            prlarea = PrL.area()
            prlreq = PrL.requiredArea(P.area())

        if LE.equal(S[0]) and PrL.area() > PrL.requiredArea(P.area()):
            while PrL.area() > PrL.requiredArea(P.area()):
                LS = move(LS, V, "CCW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)

        elif LE.equal(S[-1]) and PrL.area() < PrL.requiredArea(P.area()):
            while PrL.area() < PrL.requiredArea(P.area()):
                LS = move(LS, V, "CW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)
                prlarea = PrL.area()
                prlreq = PrL.requiredArea(P.area())

        else:
            while PrL.area() > PrL.requiredArea(P.area()):
                prlarea = PrL.area()
                prlreq = PrL.requiredArea(P.area())
                LE = move(LE, V, "CW", step)
                V_PrL = cut(V, LS, LE)
                PrL = Problem(V = V_PrL[0], S = PrL.S)
                prlarea = PrL.area()
                prlreq = PrL.requiredArea(P.area())

        V_PrL, V_PlL = cut(V, LS, LE)

        P1 = Problem(V = V_PrL, S = PrL.S)
        P2 = Problem(V = V_PlL, S = S[len(PrL.S):])

        P1.normalize()
        P2.normalize()

        if P1.numSites() > 1:
            openProblems.append(P1)
        else:
            finishedProblems.append(P2)

        if P2.numSites() > 1:
            openProblems.append(P2)
        else:
            finishedProblems.append(P2)

        L = Line(LS, LE)
        L.plot(color = "r")

        # Save figure
        plt.savefig('polygon.png')