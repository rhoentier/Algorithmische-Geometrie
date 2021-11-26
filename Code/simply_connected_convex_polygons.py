from shapely.geometry import Point, LineString, Polygon
import matplotlib.pyplot as plt
import random


def get_random_convex_polygon(num_of_points, border):

    point_set = set()
    for vertice in range(num_of_points):
        new_point = (random.randint(0, border), random.randint(0, border))
        point_set.add(new_point)

    points = []
    points.extend(point_set)
    points.sort(key=get_x_coordinate)
    points = get_outer_shell(points)
    polygon = Polygon(points)
    return polygon

def get_outer_shell(points):
    print (points)

    min_so_far = points[0]
    max_so_far = points[0]

    lower_left = []
    lower_right = []
    upper_right = []
    upper_left = []

    outer_shell = []
    #outer_shell left side
    for point in points:
        if point[1] <= min_so_far[1]:
            min_so_far = point
            lower_left.append(min_so_far)
        if point[1] >= max_so_far[1]:
            max_so_far = point
            upper_left.append(max_so_far)


    #outer_shell right side
    min_so_far = points[len(points)-1]
    max_so_far = points[len(points)-1]

    points.sort(reverse = True, key=get_x_coordinate)
    print(points)
    for point in points:
        if point[1] <= min_so_far[1]:
            min_so_far = point
            lower_right.append(min_so_far)
        if point[1] >= max_so_far[1]:
            max_so_far = point
            upper_right.append(max_so_far)
   
    lower_right.reverse()
    upper_left.reverse()
    lower_right.pop(0)
    upper_right.pop(0)
    upper_left.pop(0)
    if len(upper_left) > 0:
        upper_left.pop(len(upper_left)-1)
    outer_shell.extend(lower_left)
    outer_shell.extend(lower_right)
    outer_shell.extend(upper_right)
    outer_shell.extend(upper_left)
    print(outer_shell)
    return outer_shell
    
def get_x_coordinate(point):
    return point[0]

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
    for i in range(10):
        polygon = get_random_convex_polygon(13, 20)
        plot_polygon(polygon)