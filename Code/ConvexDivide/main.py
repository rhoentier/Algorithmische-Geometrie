import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.polygon import Polygon
from objects.pl import PL
import math

import numpy as np

def side(p, LS, LE):
    epsilon = 0.001
    d = (p.x - LS.x)*(LE.y-LS.y)-(p.y-LS.y)*(LE.x-LS.x)
    if d > -epsilon and d < epsilon:
        return "o"
    if d < 0:
        return "l"
    if d > 0:
        return "r"

def intersection(p1, p2, p3, p4):
    # https://en.wikipedia.org/wiki/Line–line_intersection
    t = ((p1.x-p3.x)*(p3.y-p4.y)-(p1.y-p3.y)*(p3.x-p4.x))/((p1.x-p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x-p4.x))
    u = ((p1.x-p3.x)*(p1.y-p2.y)-(p1.y-p3.y)*(p1.x-p2.x))/((p1.x-p2.x)*(p3.y-p4.y)-(p1.y-p2.y)*(p3.x-p4.x))
    return Point(p1.x + t*(p2.x-p1.x), p1.y + t * (p2.y-p1.y), "Intersection")

def cut(V, LS, LE):
    # https://geidav.wordpress.com/2015/03/21/splitting-an-arbitrary-polygon-by-a-line/

    V.append(V[0])
    PrL = []
    PlL = []
    prevSide = None
    prevPoint = None

    for i, v in enumerate(V):
        s = side(v, LS, LE)

        if i > 0:
            tmp = prevSide + s
            if tmp == "lr" or tmp == "rl":
                p_inter = intersection(prevPoint, v, LS, LE)
                PrL.append(p_inter)
                PlL.append(p_inter)

        if i < len(V) - 1:
            if s == "o":
                PrL.append(v)
                PlL.append(v)
            elif s == "r":
                PrL.append(v)
            elif s == "l":
                PlL.append(v)

            prevPoint = v
            prevSide = s

    V.pop()
    return PrL, PlL

def length(p1, p2):
    return math.sqrt((p2.x-p1.x)^2 + (p2.y-p1.y)^2)

def move(p, V, direction, dist):
    num_pts = len(V)
    on_point = False

    i = 0
    for v in V:
        if p.equal(v):
            on_point = True
            break
        i += 1

    if direction == "CW":
        j = (i - 1 + num_pts) % num_pts
    elif direction == "CCW":
        j = (i + 1) % num_pts

    if on_point == False:
        i = 0
        for v in V:
            s = side(p, V[i], V[(i+1) % num_pts])
            if s == "o":
                break
            i += 1

        if direction == "CW":
            j = i
            i = (i + 1) % num_pts
        elif direction == "CCW":
            j = (i + 1) % num_pts

    dx = V[j].x - V[i].x
    dy = V[j].y - V[i].y
    l = math.sqrt(dx**2 + dy**2)
    dx = dx * dist/l
    dy = dy * dist/l

    p.x = p.x + dx
    p.y = p.y + dy

    return p

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

    # Input
    W = [Point(8, 9, "P1"), Point(0, 7, "P2"), Point(0, 4, "P3"), Site(1, 2, "S1", 0.7), Point(2, 0, "P4"), Point(7, 0, "P5"),Site(8, 1, "S3", 0.3), Point(10, 3, "P6")]
    V = [x for x in W if x.type() == "Point"]
    S = [x for x in W if x.type() == "Site"]

    [s.plot("r", marker="^", size=70) for s in S]   # Plot sites
    P = Polygon(V)                                  # Plot polygon
    P.plot(color = "skyblue")

    # Step 1
    # Assume S1 = wk, assign new Line from w1 to wk

    LS = W[0].copy("LS")

    k0 = 0                   # find site with name "S1" and copy it to new point "LE"
    for w in W:
        if w.name == "S1":
            LE = w.copy("LE")
            break
        k0 += 1              # calculate k (index of S1 in list W)

    L = Line(LS, LE)
    L.plot()

    PrL, PlL = cut(V, LS, LE)


    # Step 2

    # Init PrL
    PrL = PL(PrL, "r", [S[0]])

    # Move line CCW

    k = 0
    while PrL.area() < PrL.requiredArea(P.area()) and LE.notEqual(S[-1]):
        if k > 1 and W[k0 + k - 1].type() == "Site":
            PrL.appendSite(W[k0 + k - 1])
        k += 1
        LE = W[k0 + k].copy("LE")
        PrL.appendPoint(W[k0 + k])

        L = Line(LS, LE)
        L.plot()

    if LE.equal(S[0]) and PrL.area() > PrL.requiredArea(P.area()):
        while PrL.area() > PrL.requiredArea(P.area()):
            move(LS, V, "CCW", 0.01)
            PrL, PlL = cut(V, LS, LE)
            PrL = PL(PrL, "r", [S[0]])
    elif LE.equal(S[-1]) and PrL.area() < PrL.requiredArea(P.area()):
        while PrL.area() < PrL.requiredArea(P.area()):
            move(LS, V, "CW", 0.01)
            PrL, PlL = cut(V, LS, LE)
            PrL = PL(PrL, "r", [S[0]])
    else:
        while PrL.area() > PrL.requiredArea(P.area()):
            move(LE, V, "CW", 0.01)
            PrL, PlL = cut(V, LS, LE)
            PrL = PL(PrL, "r", [S[0]])

    print(PrL.area())
    PlL = PL(PlL, "l", [])
    print(PlL.area())
    L = Line(LS, LE)
    L.plot(color = "r")

    # Save figure
    plt.savefig('polygon.png')