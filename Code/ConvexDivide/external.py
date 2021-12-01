import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.line import Line
from objects.problem import Problem
import external
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
    # V = list with polygon points (of class Point)
    # LS = starting point (class Point)
    # LE = ending point (class Point)
    # Basic idea can be found here: https://geidav.wordpress.com/2015/03/21/splitting-an-arbitrary-polygon-by-a-line/

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

    # returns two lists with objects of class point
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

def numSites(W_main):
    for i, w in enumerate(W_main):
        if w.getNumSites() > 1:
            return i
    return -1