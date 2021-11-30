import random

def side(p, LS, LE):
    epsilon = 0.001
    d = (p.x - LS.x)*(LE.y-LS.y)-(p.y-LS.y)*(LE.x-LS.x)
    if d > -epsilon and d < epsilon:
        return "o"
    if d < 0:
        return "l"
    if d > 0:
        return "r"

# Line class
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

    def getNumSites(self):
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