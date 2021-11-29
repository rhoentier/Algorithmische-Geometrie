from shapely import geometry
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import random
import math

###
# Beschreibung:     Erzeugt eine zufällige Punktemenge und bildet die konvexe Hülle dieser Menge.
# Eingabe:          num_of_points {int}:    Anzahl der Punkte, die im Polygon liegen sollen
#                   border {int}:            Grenzen, in denen die Punkte liegen sollen 
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
# Ausgabe:          {list(tuple(float,float))} Liste von festen Standorten auf dem Rand eines Polygons
###
def create_sites(polygon, num_of_sites):

    polygon = list(polygon.exterior.coords)
    sites = []

    for i in range(num_of_sites):
        position = random.uniform(0, len(polygon) - 1)
        index = math.floor(position)
        position = position - index
        if polygon[index][0] < polygon[index + 1][0]:
            x_distance = polygon[index + 1][0] - polygon[index][0]
            y_distance = polygon[index + 1][1] - polygon[index][1]
            x_coord = polygon[index][0] + (x_distance * position)
            y_coord = polygon[index][1] + (y_distance * position)
            site = (x_coord, y_coord)
        if polygon[index][0] > polygon[index + 1][0]:
            x_distance = polygon[index][0] - polygon[index + 1][0]
            y_distance =polygon[index][1] - polygon[index + 1][1]
            x_coord = polygon[index + 1][0] + (x_distance * position)
            y_coord = polygon[index + 1][1] + (y_distance * position)
            site = (x_coord, y_coord)
        if polygon[index][0] == polygon[index + 1][0]:
            site = (polygon[index][0], polygon[index][1])
        plt.scatter(site[0], site[1]) 
        sites.append(site)

    return sites


###
# Beschreibung:     Fügt die Standorte in ein Polygon ein.
# Eingabe:          polygon {shapely.geometry.Polygon} Konvexes Polygon  
#                   sites {list(tuple(float,float))} Liste der festen Standorte
# Ausgabe:          {list(tuple(float,float)) , list(tuple(float,float))} Liste mit Standorten und geometrischen Punkten in CCW und Liste mit Standorten in CCW
###
def combine_sites_polygon(polygon, sites):
    
    polygon = list(polygon.exterior.coords)
    list_w = []
    sorted_sites = []
    
    for i in range(len(polygon)-1):
        list_w.append(polygon[i])
        current_sites = []
        found_site = False
        for site in sites:
            if site[0] >= polygon[i][0] and site[0] <= polygon[i + 1][0]:
                small_index = True
                if site[1] >= polygon[i][1] and site[1] <= polygon[i + 1][1]:
                    current_sites.append(site)
                    found_site = True
                elif site[1] < polygon[i][1] and site[1] > polygon[i + 1][1]:
                    current_sites.append(site)
                    found_site = True
            elif site[0] < polygon[i][0] and site[0] > polygon[i + 1][0]:
                small_index = False
                if site[1] >= polygon[i][1] and site[1] <= polygon[i + 1][1]:
                    current_sites.append(site)
                    found_site = True
                elif site[1] < polygon[i][1] and site[1] > polygon[i + 1][1]:
                    current_sites.append(site)
                    found_site = True
        if found_site:
            if small_index:
                current_sites.sort(key=get_x_coordinate)
            else:
                current_sites.sort(key=get_x_coordinate, reverse=True)
            list_w.extend(current_sites)
            sorted_sites.extend(current_sites)
    
    return list_w, sorted_sites


###
# Beschreibung:     Erzeugt für ein Polygon und eine Menge von Standorten die jeweiligen benötigten Flächen
# Eingabe:          polygon {shapely.geometry.Polygon} Konvexes Polygon
#                   sites {list(tuple(float,float))} Liste der festen Standorte
# Ausgabe:          {list(tuple(tuple(float,float), float) Liste mit Standorten und derer jeweils benötigten Fläche
###
def create_area_requirement(polygon, sites):
    
    area_requirement_p = polygon.area
    num_of_sites = len(sites)
    area_requirement_s = area_requirement_p / num_of_sites
    list_s = []

    for site in sites:
        list_s.append((site, area_requirement_s))

    return list_s


###
# Beschreibung:     convex_divide implementiert den Algorithmus "ConvexDivide" (S.6) [Hert, Lumelsky]. Ein Polygon wird in zwei flächen-vollständige-Polygone geteilt.
#                   In unserem Fall sind alle Flächen gleich groß.
# Eingabe:          list_w  {list(tuple(float,float))} Ein Polygon und die Standorte, deren Knoten in CCW-Folge gegeben sind
#                   list_s  {list(tuple(tuple(float,float), float) Liste mit Standorten und derer jeweils benötigten Fläche
# Ausgabe:          Zwei Polygone, die flächen-vollständig sind
###
def convex_divide(list_w, list_s):
    
    increment = 0.01
    epsilon = 1.0

    line_l = (list_w[0], list_s[0][0])
    sites_p_r = [list_s[0]]
    print(line_l)
    polygon_p_l, polygon_p_r = cut_polygon(list_w, line_l)

    if len(polygon_p_r) < 3:
        area_p_r = 0
    else:
        polygon_p_r = Polygon(polygon_p_r)
        area_p_r = polygon_p_r.area

    required_area_p_r = 0
    for site in sites_p_r:
        required_area_p_r = required_area_p_r + site[1]
    
    k = 1
    while area_p_r < required_area_p_r and line_l[1] != list_s[len(list_s) - 1][0]:
        sites_p_r.append(list_s[k])
        line_l = (list_w[0], list_s[k][0])
        k = k + 1

        polygon_p_l, polygon_p_r = cut_polygon(list_w, line_l)
        if len(polygon_p_r) < 3:
            area_p_r = 0
        else:
            polygon_p_r = Polygon(polygon_p_r)
            area_p_r = polygon_p_r.area

        required_area_p_r = 0
        for site in sites_p_r:
            required_area_p_r = required_area_p_r + site[1]

        if area_p_r != 0:
            ###### FOR DEBUGGING ######
            for site in list_s:
                plt.scatter(site[0][0], site[0][1])
            x,y = polygon_p_r.exterior.xy
            plt.plot(x,y, linestyle='--')

            polygon_p_l = Polygon(polygon_p_l)
            x,y = polygon_p_l.exterior.xy
            plt.plot(x,y, linestyle=':')
            print("")
            plt.show()
            ###### FOR DEBUGGING ######
    
    if line_l[1] == list_s[0][0] and area_p_r > required_area_p_r:
        while area_p_r > (required_area_p_r + epsilon):
            index_in_w = list_w.index(list_s[0][0])
            x_difference = list_w[index_in_w + 1][0] - list_w[index_in_w][0]
            y_difference = list_w[index_in_w + 1][1] - list_w[index_in_w][1]

            line_l = ((line_l[0][0] + x_difference * increment, line_l[0][1] + y_difference * increment), line_l[1])
            
            polygon_p_l, polygon_p_r = cut_polygon(list_w, line_l)
            if len(polygon_p_r) < 3:
                area_p_r = 0
            else:
                polygon_p_r = Polygon(polygon_p_r)
                area_p_r = polygon_p_r.area

            required_area_p_r = 0
            for site in sites_p_r:
                required_area_p_r = required_area_p_r + site[1]

    elif line_l[1] == list_s[len(list_s) - 1][0] and area_p_r > required_area_p_r:
        while area_p_r > (required_area_p_r + epsilon):
            index_in_w = list_w.index(list_s[len(list_s) - 1][0])
            x_difference = list_w[index_in_w - 1][0] - list_w[index_in_w][0]
            y_difference = list_w[index_in_w - 1][1] - list_w[index_in_w][1]

            line_l = (line_l[0], (line_l[1][0] + x_difference * increment, line_l[1][1] + y_difference * increment))
            
            polygon_p_l, polygon_p_r = cut_polygon(list_w, line_l)
            if len(polygon_p_r) < 3:
                area_p_r = 0
            else:
                polygon_p_r = Polygon(polygon_p_r)
                area_p_r = polygon_p_r.area

            required_area_p_r = 0
            for site in sites_p_r:
                required_area_p_r = required_area_p_r + site[1]



###
# Beschreibung:     Teilt ein Polygon durch eine Linie L
# Eingabe:          list_w  {list(tuple(float,float))} Ein Polygon und die Standorte, deren Knoten in CCW-Folge gegeben sind
#                   line_l  {tuple(tuple(float,float), tuple(float,float))} Eine Linie, die beide Endpunkte auf dem Rand des Polygons hat
# Ausgabe:          {list(tuple(float,float)), list(tuple(float,float))} Zwei Polygone
###
def cut_polygon(list_w, line_l):
    
    if line_l[0] in list_w and line_l[1] in list_w:
        index_in_w_0 = list_w.index(line_l[0])
        index_in_w_1 = list_w.index(line_l[1])

        difference = abs(index_in_w_0 - index_in_w_1)
        if difference == 1:
            if line_l[0][1] < line_l[1][1]:
                list_w_r = list_w
                list_w_l = line_l
                return list_w_l, list_w_r
            else:
                list_w_r = line_l
                list_w_l = list_w
                return list_w_l, list_w_r


    changed_direction = False
    if line_l[0][0] < line_l[1][0]:
        if line_l[0][1] < line_l[1][1]:
            list_w_r = [line_l[0]]
        elif line_l[0][1] > line_l[1][1]:
            list_w_r = [line_l[1]]
            changed_direction = True
        elif line_l[0][1] == line_l[1][1]:
            list_w_r = [line_l[1]]
            changed_direction = True
    elif line_l[0][0] > line_l[1][0]:
        if line_l[0][1] < line_l[1][1]:
            list_w_r = [line_l[0]]
        elif line_l[0][1] > line_l[1][1]:
            list_w_r = [line_l[1]]
            changed_direction = True
        elif line_l[0][1] == line_l[1][1]:
            list_w_r = [line_l[0]]
    elif line_l[0][0] == line_l[1][0]:
        if line_l[0][1] < line_l[1][1]:
            list_w_r = [line_l[0]]
        elif line_l[0][1] > line_l[1][1]:
            list_w_r = [line_l[1]]
            changed_direction = True

    starting_index = len(list_w)-1
    for i in range(len(list_w) - 1):
        if list_w_r[0] == list_w[i]:
            starting_index = i
            break
        elif list_w_r[0][0] > list_w[i][0] and list_w_r[0][0] < list_w[i + 1][0]:
            starting_index = i+1
            break
        elif list_w_r[0][0] == list_w[i][0] and list_w_r[0][0] == list_w[i + 1][0]:
            starting_index = i+1
            break
    

    if changed_direction:
        end_point = line_l[0]
        starting_point = line_l[1]
    else:
        end_point = line_l[1]
        starting_point = line_l[0]


    end_index = len(list_w) - 1
    for i in range(len(list_w) - 1):
        if end_point == list_w[i]:
            end_index = i
            break
        elif end_point[0] < list_w[i][0] and end_point[0] > list_w[i + 1][0]:
            end_index = i - 1
            break
        elif end_point[0] == list_w[i][0] and end_point[0] == list_w[i + 1][0]:
            end_index = i - 1
            break

    list_w_r.extend(list_w[starting_index:end_index])
    list_w_r.append(end_point)
    if list_w_r[0] == list_w_r[1]:
        list_w_r.pop(1)
    
    list_w_l = [end_point]
    list_w_l.extend(list_w[end_index:])
    list_w_l.extend(list_w[:starting_index])
    list_w_l.append(starting_point)
    if list_w_l[len(list_w_l) - 1] == list_w_l[len(list_w_l) - 2]:
        list_w_r.pop(len(list_w_l) - 1)

    return list_w_l, list_w_r


###
# Beschreibung:     Gibt die X-Koordinate eines Punktes wieder
# Eingabe:          {tuple(<type>, <type>)} Punkt
# Ausgabe:          {<ype>} X-Coordinate eines Punktes
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
    # ax.get_xaxis().set_visible(False)
    #hide y-axis 
    # ax.get_yaxis().set_visible(False)

    plt.show()


if __name__ == "__main__":
    for i in range(1):
        polygon = get_random_convex_polygon(12,30)
        #print(list(polygon.exterior.coords))
        sites = create_sites(polygon, 5)
        list_w, sites = combine_sites_polygon(polygon, sites)
        list_s = create_area_requirement(polygon, sites)
        convex_divide(list_w, list_s)
        #plot_polygon(polygon)