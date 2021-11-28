from shapely import geometry
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import random
import math

###
# Beschreibung:     Erzeugt eine zufällige Punktemenge und bildet die konvexe Hülle dieser Menge.
# Eingabe:          num_of_points {int}:    Anzahl der Punkte, die im Polygon liegen sollen
#                   border{int}:            Grenzen, in denen die Punkte liegen sollen 
# Ausgabe:          {shapely.geometry.Polygon} Konvexes Polygon
###
def get_random_convex_polygon(num_of_points, border):

    if num_of_points < 3:
        print("ACHTUNG: Es müssen mindestens 3 Punkte im Polygon sein. Es wird deswegen auf 3 erhöht")
        num_of_points = 3

    point_set = set()
    for vertice in range(num_of_points):
        new_point = (random.randint(0, border), random.randint(0, border))
        point_set.add(new_point)

    if len(point_set) < 3:
        while len(point_set) < 3:
            new_point = (random.randint(0, border), random.randint(0, border))
            point_set.add(new_point)

    points = []
    points.extend(point_set)
    points.sort(key=get_x_coordinate)
    points = get_outer_hull(points)
    polygon = Polygon(points)
    polygon = polygon.convex_hull
    polygon = geometry.polygon.orient(polygon, sign=1.0)
    return polygon


###
# Beschreibung:     Erzeugt eine zufällige Punktemenge und bildet die konvexe Hülle dieser Menge. (Angelehnt an Algorithmische Geometrie [Klein] (S.167))
# Eingabe:          points {list(tuple(int,int))}:    Menge von Punkten, aus denen eine äußere Hülle gebildet werden soll
# Ausgabe:          {list(tuple(int,int))} Äußere Hülle einer Punktemenge. Punkte sind in CCW-Folge sortiert
###
def get_outer_hull(points):

    if len(points) == 3:
        return points

    min_so_far = points[0]
    max_so_far = points[0]

    lower_left = []
    lower_right = []
    upper_right = []
    upper_left = []

    outer_hull = []
    #outer_hull left side
    for point in points:
        if point[1] <= min_so_far[1]:
            min_so_far = point
            lower_left.append(min_so_far)
        if point[1] >= max_so_far[1]:
            max_so_far = point
            upper_left.insert(0, max_so_far)


    #outer_hull right side
    min_so_far = points[len(points)-1]
    max_so_far = points[len(points)-1]
    points.sort(reverse = True, key=get_x_coordinate)
    for point in points:
        if point[1] <= min_so_far[1]:
            min_so_far = point
            lower_right.insert(0, min_so_far)
        if point[1] >= max_so_far[1]:
            max_so_far = point
            upper_right.append(max_so_far)

    if len(lower_right) > 0:
        lower_right.pop(0)
    if len(upper_right) > 0:
        upper_right.pop(0)
    if len(upper_left) > 0:
        upper_left.pop(0)
    if len(upper_left) > 0:
        upper_left.pop(len(upper_left)-1)
    outer_hull.extend(lower_left)
    outer_hull.extend(lower_right)
    outer_hull.extend(upper_right)
    outer_hull.extend(upper_left)

    return outer_hull
    


###
# Beschreibung:     Erzeugt für ein Polygon eine zufällige Menge von festen Standorten auf dem Polygon.
# Eingabe:          polygon {shapely.geometry.Polygon} Konvexes Polygon  
#                   num_of_sites (int) Anzahl der festen Standorte
# Ausgabe:          {list(tuple(int,int))} Liste von festen Standorten auf dem Rand eines Polygons
###
def create_sites(polygon, num_of_sites):

    polygon = list(polygon.exterior.coords)
    sites = []

    for i in range(num_of_sites):
        position = random.uniform(0, len(polygon) - 1)
        index = math.floor(position)
        position = position - index
        if polygon[index][0] < polygon[index + 1][0]:
            gradient = (polygon[index + 1][1] - polygon[index][1]) / (polygon[index + 1][0] - polygon[index][0])
            site = (polygon[index][0] + position, polygon[index][1] + (gradient * position))
        if polygon[index][0] > polygon[index + 1][0]:
            gradient = (polygon[index][1] - polygon[index + 1][1]) / (polygon[index][0] - polygon[index + 1][0])
            site = (polygon[index + 1][0] + position, polygon[index + 1][1] + (gradient * position))
        if polygon[index][0] == polygon[index + 1][0]:
            site = (polygon[index][0], polygon[index][1])
        plt.scatter(site[0], site[1]) 
        sites.append(site)


###
# Beschreibung:     convex_divide implementiert den Algorithmus "ConvexDivide" (S.6) [Hert, Lumelsky]. Ein Polygon wird in zwei flächen-vollständige-Polygone geteilt.
#                   In unserem Fall sind alle Flächen gleich groß.
# Eingabe:          Ein Polygon, deren Knoten in CCC-Folge gegeben sind
# Ausgabe:          Zwei Polygone, die flächen-vollständig sind
###
def convex_divide(polygon):
    pass


###
# Beschreibung:     Gibt die X-Koordinate eines Punktes wieder
# Eingabe:          {tuple(int, int)} Punkt
# Ausgabe:          {int} X-Coordinate eines Punktes
###
def get_x_coordinate(point):
    return point[0]


###
# Beschreibung:     Gibt mithilfe von Matplotlib ein Polygon aus
# Eingabe:          {shapely.geometry.Polygon} Polygon
# Ausgabe:          
###
def plot_polygon(polygon):
    #get exterior lines
    x,y = polygon.exterior.xy
    plt.plot(x,y)

    #get current axes
    ax = plt.gca()

    #hide frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    #hide x-axis
    ax.get_xaxis().set_visible(False)
    #hide y-axis 
    ax.get_yaxis().set_visible(False)

    plt.show()


if __name__ == "__main__":
    for i in range(8):
        polygon = get_random_convex_polygon(12,30)
        #print(list(polygon.exterior.coords))
        sites = create_sites(polygon, 4)
        plot_polygon(polygon)