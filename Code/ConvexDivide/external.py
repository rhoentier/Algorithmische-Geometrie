import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.problem import Problem
import external
import math

import numpy as np

def side(p, LS, LE):
    epsilon = 0.03  # epsilon nicht direkt als Abstand
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
    # V = list with polygon points (of class Point)
    # LS = starting point (class Point)
    # LE = ending point (class Point)
    # Basic idea can be found here: https://geidav.wordpress.com/2015/03/21/splitting-an-arbitrary-polygon-by-a-line/

    PrL = []
    PlL = []

    # Special case if LS and LE are on the same line and all other points are to the left
    if side(V[0], LS, LE) == "o" and side(V[1], LS, LE) == "o":
        PrL = [V[0], LE]
        PlL = V
        return PrL, PlL
    # Special case if LS and LE are on the same line and all other points are to the right
    elif side(V[0], LS, LE) == "o" and side(V[-1], LS, LE) == "o":
        PrL = V
        PlL = []
        return PrL, PlL
    else:
        for i, v in enumerate(V):
            j = (i + 1) % len(V)

            si = side(V[i], LS, LE)
            sj = side(V[j], LS, LE)

            if si == "o" or si == "r":
                PrL.append(v)
            if si == "o" or si == "l":
                PlL.append(v)

            tmp = si + sj
            if tmp == "lr" or tmp == "rl":
                p_inter = intersection(V[i], V[j], LS, LE)
                PrL.append(p_inter)
                PlL.append(p_inter)

    # returns two lists with objects of class point
    return PrL, PlL

def length(p1, p2):
    return math.sqrt((p2.x-p1.x)^2 + (p2.y-p1.y)^2)

def move(p, V, direction, dist):
    num_pts = len(V)
    on_point = False

    i = 0
    for i in range(num_pts):
        if p.equal(V[i]):
            on_point = True
            break

    if on_point == True:
        if direction == "CW":
            j = (i - 1 + num_pts) % num_pts

        elif direction == "CCW":
            j = (i + 1) % num_pts

    elif on_point == False:
        for i, v in enumerate(V):
            von = V[i]
            zu = V[(i+1) % num_pts]
            s = side(p, V[i], V[(i+1) % num_pts])
            if s == "o":
                break
            i += 1

        if direction == "CW":
            j = i
            i = (i + 1) % num_pts
        elif direction == "CCW":
            j = (i + 1) % num_pts


    #if direction == "CW":
    dx = p.x - V[j].x
    dy = p.y - V[j].y
    l = math.sqrt(dx ** 2 + dy ** 2)
    dx = dx * (l-dist)/l
    dy = dy * (l-dist)/l
    p.x = V[j].x + dx
    p.y = V[j].y + dy
    #elif direction == "CCW":
    #    dx = V[i].x - V[j].x
    #    dy = V[i].y - V[j].y
    #    l = math.sqrt(dx ** 2 + dy ** 2)
    #    dx = dx * (l - dist) / l
    #    dy = dy * (l - dist) / l
    #    p.x = V[j].x + dx
    #    p.y = V[j].y + dy

    return p

def numSites(W_main):
    for i, w in enumerate(W_main):
        if w.getNumSites() > 1:
            return i
    return -1