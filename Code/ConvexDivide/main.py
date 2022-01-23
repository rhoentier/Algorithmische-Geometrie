import matplotlib.pyplot as plt
from objects.point import Point
from objects.site import Site
from objects.convexpiece import ConvexPolygon
from external import move, numSites, cut
import random
import numpy as np

output_configs = {
  "example1": {
      "annotateStatus": False,
      "annotateArea": False,
      "drawPoly1": False,
      "drawPolyn": False,
      "drawInit": False,
      "drawRaw1": False,
      "drawRawIterative": False,
      "drawRawResult": False,
      "drawIterative": False,
      "drawResult": True,
      "drawFinal": True,
      "example": 4
  },
  "example2": {
      "annotateStatus": False,
      "annotateArea": False,
      "drawPoly1": False,
      "drawPolyn": False,
      "drawInit": True,
      "drawRaw1": False,
      "drawRawIterative": False,
      "drawRawResult": True,
      "drawIterative": False,
      "drawResult": True,
      "drawFinal": False,
      "example": 2
  },
  "example3": {
      "annotateStatus": False,
      "annotateArea": False,
      "drawPoly1": False,
      "drawPolyn": True,
      "drawInit": False,
      "drawRaw1": False,
      "drawRawIterative": False,
      "drawRawResult": False,
      "drawIterative": False,
      "drawResult": True,
      "drawFinal": True,
      "example": 4
  },
  "video": {
      "annotateStatus": True,
      "annotateArea": True,
      "drawPoly1": True,
      "drawPolyn": True,
      "drawInit": True,
      "drawRaw1": True,
      "drawRawIterative": False,
      "drawRawResult": True,
      "drawIterative": True,
      "drawResult": True,
      "drawFinal": True,
      "example": 4
  }
}

example_configs = {
  "example1": {
      "polygon": 1,
      "output_config": "example1"
  },
  "example2.1": {
      "polygon": 2,
      "output_config": "example2"
  },
  "example2.2": {
      "polygon": 3,
      "output_config": "example2"
  },
  "example2.3": {
      "polygon": 4,
      "output_config": "example2"
  },
  "example3": {
      "polygon": 5,
      "output_config": "example3"
  },
  "video": {
      "polygon": 1,
      "output_config": "video"
  }
}

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
        P_init.addSite(Site(0, 5, 0.05, 1))
        P_init.addSite(Site(1, 2, 0.55, 2))
        P_init.addSite(Site(3, 0, 0.18, 3))
        P_init.addSite(Site(8, 1, 0.22, 4))
    elif index == 2:
        P_init.addSite(Site(1, 2, 0.20, 1))
        P_init.addSite(Site(8, 1, 0.80, 2))
    elif index == 3:
        P_init.addSite(Site(1, 2, 0.70, 1))
        P_init.addSite(Site(8, 1, 0.30, 2))
    elif index == 4:
        P_init.addSite(Site(1, 2, 0.95, 1))
        P_init.addSite(Site(8, 1, 0.05, 2))

    elif index == 5:
        P_init.addSite(Site(6, 8.5, 0.125, 1))
        P_init.addSite(Site(1, 7.25, 0.125, 2))
        P_init.addSite(Site(0, 5, 0.125, 3))
        P_init.addSite(Site(3, 0, 0.125, 4))
        P_init.addSite(Site(6, 0, 0.125, 5))
        P_init.addSite(Site(8, 1, 0.125, 6))
        P_init.addSite(Site(9, 2, 0.125, 7))
        P_init.addSite(Site(8.333333, 8, 0.125, 8))
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

    plt.xlim(-1, 11)
    plt.ylim(-1, 11)
    plt.xticks(np.arange(-1, 12, step=1))
    plt.yticks(np.arange(-1, 12, step=1))
    plt.grid(zorder=0)
    plt.tight_layout()

def compare(val1, val2, operator):
    if operator == ">":
        return val1 > val2
    elif operator == "<":
        return val1 < val2
    else:
        print("not defined")
        exit()

def ConvexDivide(CP, iter = 1):

    def snapshot(iimg, **kwargs):

        drawLine = kwargs.get("drawLine", True)
        drawArea = kwargs.get("drawArea", True)
        drawAnnotation = kwargs.get("drawAnnotation", True)
        removeLine = kwargs.get("removeLine", drawLine)
        removeArea = kwargs.get("removeArea", drawArea)
        removeAnnotation = kwargs.get("annotateLine", drawAnnotation)
        status = kwargs.get("status", False)

        if output.get("annotateArea") == False:
            drawArea = False
            removeArea = False

        if output.get("annotateStatus") == False:
            status = False


        highlightPoint = kwargs.get("highlightPoint", False)
        color = kwargs.get('color', "k")
        linestyle = kwargs.get("linestyle", "-")

        if drawLine:
            ax.plot([LS.x, LE.x], [LS.y, LE.y], color=color, linestyle = linestyle)

        if drawArea:
            txt1 = ax.text(-1, -2.1, 'AreaRequired(S(PrL)):', fontsize=12)
            txt2 = ax.text(-1, -2.5, 'Area(PrL):', fontsize = 12)
            txt3 = ax.text(2, -2.1, '{:.2f}'.format(PrL.requiredArea()), fontsize = 12)
            txt4 = ax.text(2, -2.5, '{:.2f}'.format(PrL.area()), fontsize = 12)

        if status != False:
            txt5 = ax.text(-1, -1.7, 'Status:', fontsize = 12)
            txt6 = ax.text(2, -1.7, status, fontsize = 12)

        if drawAnnotation:
            ann1 = plt.annotate(LS.name, (LS.x - 0.25, LS.y - 0.25), ha="center", va="center", color=color, zorder=11)
            ann2 = plt.annotate(LE.name, (LE.x - 0.25, LE.y - 0.25), ha="center", va="center", color=color, zorder=11)

            dist = 0.5
            dx = LE.x - LS.x
            dy = LE.y - LS.y
            len = np.sqrt(dx ** 2 + dy ** 2)
            centerX = LS.x + dx / 2
            centerY = LS.y + dy / 2
            PrLX = centerX + dy * dist / len
            PrLY = centerY - dx * dist / len
            PlLX = centerX - dy * dist / len
            PlLY = centerY + dx * dist / len

            ann3 = plt.annotate("PrL", (PrLX, PrLY), ha="center", va="center", color="k", zorder=11, bbox = dict(boxstyle=f"circle,pad={0.4}", fc="white", alpha=0.8))
            ann4 = plt.annotate("PlL", (PlLX, PlLY), ha="center", va="center", color="k", zorder=11, bbox = dict(boxstyle=f"circle,pad={0.4}", fc="white", alpha=0.8))
        if highlightPoint != False:
            circle1 = plt.scatter(highlightPoint[0], highlightPoint[1], color="orange", s=300, zorder=4)

        plt.savefig("out/" + example + '/' + str(iter).zfill(2) + '_' + str(iimg).zfill(4) + '.png')

        if removeLine:
            ax.lines.pop()
        if removeArea:
            txt1.remove()
            txt2.remove()
            txt3.remove()
            txt4.remove()
        if status != False:
            txt5.remove()
            txt6.remove()
        if removeAnnotation:
            ann1.remove()
            ann2.remove()
            ann3.remove()
            ann4.remove()

        if highlightPoint != False:
            circle1.remove()

        iimg += 1
        return iimg

    print("ConvexDivide: " + str(iter))
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    iimg = 0

    initPlot()                      # Initialize plot
    CP.plotV()  # Plot vertices and edges of CP
    CP.plotS()  # Plot sites of CP

    if CP.numSites() <= 1:
        if output.get("drawPoly1"):
            iimg = snapshot(iimg, drawLine = False, drawAnnotation=False, drawArea=False, status="Polygon with number of sites == 1, no partitioning needed")
        return [CP], iter

    if output.get("drawPolyn"):
        iimg = snapshot(iimg, drawLine = False, drawAnnotation=False, drawArea=False, status="Polygon with number of sites > 1, partitioning needed")

    # Initialize line segment L
    LS = Point(CP.W[0].x, CP.W[0].y, "Ls")      # LS at first element of list W
    k0 = CP.indexOfFirstSiteInW()
    LE = Point(CP.S[0].x, CP.S[0].y, "Le")      # LE at first site in list W

    # Initial partitioning with initialized line
    V_PrL = cut(CP.V, LS, LE)
    PrL = ConvexPolygon(V=V_PrL, S=[CP.S[0]])

    if output.get("drawInit"):
        iimg = snapshot(iimg, color="darkgrey", linestyle="dotted", removeLine = False, drawArea=False, status="Line initialized from w1 to first site in W")

    def xxx(iimg, **kwargs):
        highlight_pt = kwargs.get("highlight_pt", False)
        last_pt = kwargs.get("last_pt", False)
        removeLine = kwargs.get("removeLine", True)

        if PrL.area() < PrL.requiredArea():
            status = "Area(PrL) < AreaRequired(S(PrL)), move Le CCW to next w"
            linestyle = "--"
        else:
            status = "Area(PrL) >= AreaRequired(S(PrL))"
            linestyle = "-"
        if highlight_pt != False:
            status = status + ", add previous site"
        if last_pt == True:
            status = status + ", last site reached"
        iimg = snapshot(iimg, color="royalblue", linestyle=linestyle, status=status, highlightPoint=highlight_pt, removeLine=removeLine)
        return iimg + 1

    if output.get("drawRaw1"):
        iimg = xxx(iimg)

    # Move LE CCW from point to point if PrL is area-incomplete
    k = 0
    while PrL.area() < PrL.requiredArea() and LE.notEqual(CP.S[-1]):

        highlight_pt = False
        if k > 0 and CP.W[k0 + k].type() == "Site":
            PrL.appendSite(CP.W[k0 + k])
            highlight_pt = [CP.W[k0 + k].x, CP.W[k0 + k].y]

        k += 1
        LE = Point(CP.W[k0 + k].x, CP.W[k0 + k].y, "Le")
        PrL.appendPoint(CP.W[k0 + k])

        last_point = LE.equal(CP.S[-1])
        if output.get("drawRawIterative"):
            iimg = xxx(iimg, highlight_pt = highlight_pt, last_pt = last_point)

    if output.get("drawRawResult"):
        iimg = snapshot(iimg, color="royalblue", linestyle="-", removeLine=False)

    # Move LS/LE incrementally until area requirement is fulfilled

    if LE.equal(CP.S[0]) and PrL.area() > PrL.requiredArea():
        case = 1
    elif LE.equal(CP.S[-1]) and PrL.area() < PrL.requiredArea():
        case = 2
    else:
        case = 3

    switch = {1: [">", "Ls", "CCW", "reduce"], 2: ["<", "Ls", "CW", "increase"], 3: [">", "Le", "CW", "reduce"]}

    # Case 1: PrL too big from the beginning, Move LS CCW until PrL is small enough to fulfill requirement
    while compare(PrL.area(), PrL.requiredArea(), switch[case][0]):
        if switch[case][1] == "Ls":
            LS = move(LS, CP.V, switch[case][2], step)
        elif switch[case][1] == "Le":
            LE = move(LE, CP.V, "CW", step)
        V_PrL = cut(CP.V, LS, LE)
        PrL = ConvexPolygon(V=V_PrL, S=PrL.S)

        if output.get("drawIterative"):
            iimg = snapshot(iimg, color = "royalblue", status= "Move " + switch[case][1] + " in " + switch[case][2] + "-direction to " + switch[case][3] + " area of PrL")

    V_PrL, V_PlL = cut(CP.V, LS, LE, direction = "both")

    PrL = ConvexPolygon(V=V_PrL, S=PrL.S)
    PlL = ConvexPolygon(V=V_PlL, S=CP.S[len(PrL.S):])

    if output.get("drawResult"):
        iimg = snapshot(iimg, color = "red", linestyle="-", drawAnnotation=True, status="Area(PrL) == AreaRequired(S(PrL)), execute partitioning")

    CPis = []
    tmp, iter = ConvexDivide(PrL, iter+1)
    CPis += tmp
    tmp, iter = ConvexDivide(PlL, iter+1)
    CPis += tmp

    plt.close()

    return CPis, iter


step = 0.01 # 0.01
if __name__ == '__main__':

    example = "example1"
    print(example)

    example_dict = example_configs[example]
    polygon = example_dict.get("polygon")
    config  = example_dict.get("output_config")

    output = output_configs[config]

    CP = getExample(polygon)        # get predefined sites or random example

    arr, iter = ConvexDivide(CP)
    iter += 1

    initPlot()  # Initialize plot
    for CPi in arr:
        CPi.plotV()  # Plot vertices and edges of CP
        CPi.plotS()  # Plot sites of CP

    if output.get("drawFinal"):
        plt.savefig("out/" + example + '/' + str(iter).zfill(2) + '_0000.png')
    plt.close()