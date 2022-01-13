import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(10, 10))
plt.xlim(-1, 11)
plt.ylim(-1, 11)
plt.xticks(np.arange(-1, 12, step=1))
plt.yticks(np.arange(-1, 12, step=1))
plt.grid(zorder=0)

# Input
V = [[0, 0], [10, 0], [10, 10], [0, 10]]
S = [[5, 0, "(0.05 / 3.5)"], [10, 5], [5, 10], [0, 5]]  # 3rd parameter = optional string
L = [[2, 0], [8, 10]]
save = True # save plot?
show = True # show plot?

# draw V
xs = [p[0] for p in V]
ys = [p[1] for p in V]
an = ["V" + str(i).zfill(2) for i in range(1, len(V) + 1)]
xs.append(xs[0])
ys.append(ys[0])
plt.plot(xs, ys, color = "k", zorder=5)

plt.scatter(xs, ys, color = "k", s = 30, marker = "o", zorder=6)
for p in range(len(V)):
    plt.annotate(an[p], (V[p][0] + 0.25, V[p][1] + 0.25), ha = "center", va = "center", color = "k", zorder = 11)

# draw S
xs = [p[0] for p in S]
ys = [p[1] for p in S]

an = []
for i in range(len(S)):
    txt = "S" + str(i + 1).zfill(2)
    if len(S[i]) == 3:
        txt += " " + S[i][2]
    an.append(txt)

plt.scatter(xs, ys, color = "r", s = 70, marker = "x", zorder=6)
for p in range(len(S)):
    plt.annotate(an[p], (S[p][0] + 0.25, S[p][1] + 0.25), ha = "center", va = "center", color = "r", zorder = 11)

# draw L
xs = [p[0] for p in L]
ys = [p[1] for p in L]
plt.plot(xs, ys, color = "royalblue", zorder=5)

an = ["Ls", "Le"]
for p in range(len(L)):
    plt.annotate(an[p], (L[p][0] - 0.25, L[p][1] - 0.25), ha = "center", va = "center", color = "royalblue", zorder = 11)

# draw PrL/PlL - markers
dist = 0.5
LS = L[0]
LE = L[1]
dx = LE[0] - LS[0]
dy = LE[1] - LS[1]
len = np.sqrt(dx ** 2 + dy ** 2)
centerX = LS[0] + dx / 2
centerY = LS[1] + dy / 2
PrLX = centerX + dy * dist / len
PrLY = centerY - dx * dist / len
PlLX = centerX - dy * dist / len
PlLY = centerY + dx * dist / len

plt.annotate("PrL", (PrLX, PrLY), ha="center", va="center", color="k", zorder=11, bbox = dict(boxstyle=f"circle,pad={0.4}", fc="white", alpha=0.8))
plt.annotate("PlL", (PlLX, PlLY), ha="center", va="center", color="k", zorder=11, bbox = dict(boxstyle=f"circle,pad={0.4}", fc="white", alpha=0.8))

if save:
    plt.savefig('example.png')
if show:
    plt.show()