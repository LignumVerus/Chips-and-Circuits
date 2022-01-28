import queue
import copy

from helper import *
from options import *

def find_random_route(
    start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap
):
    """
    creates route 
    """
    # route can not cross another chip
    invalid_chip_coords = list(chips_dict.values())

    if end_coordinate in invalid_chip_coords:
        invalid_chip_coords.remove(end_coordinate)
    
    return astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)


def astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap):
    q = queue.Queue()
    q.put([start_coordinate])

    # (route, distance)
    best_unfinished_children = [([start_coordinate], manhattan_distance(start_coordinate, end_coordinate))]

    while not q.empty():
        route = q.get()

        costs = []

        for i in valid_directions(
            route[-1], invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap
        ):
            child = copy.deepcopy(route)
            child.append(i[0])

            # if end is found, return this route
            if i[0] == end_coordinate:
                return child, True

            g = route_costs(board, child)
            h = manhattan_distance(i[0], end_coordinate) + i[1]
            f = g + h

            costs.append((child, f))

        # put child with lowest cost
        if len(costs) > 0:
            best_child = sorted(costs, key=lambda x: x[1])[0]
            best_child_path = best_child[0]

            # save 10 best children
            if len(best_unfinished_children) < 20:
                best_unfinished_children.append((best_child_path, manhattan_distance(best_child_path[-1], end_coordinate)))
            else:
                # vervang plek met tuple index 1 waar waarde het hoogst is
                best_unfinished_children = sorted(best_unfinished_children, key=lambda x:x[1])
                
                best_unfinished_children[-1] = (best_child_path, manhattan_distance(best_child_path[-1], end_coordinate))

            #TODO: idee: in begin wind en down kosten 1 en zodra niveau 7 is bereikt alles 0?

            q.put(best_child_path)

    # no route found, return unfinished route (last child)
    # try with other children closest to end coordinate?
    try:
        return sorted(best_unfinished_children, key=lambda x:x[1]), False
    except UnboundLocalError:
        return [], False


def closest_line_index(route, netlist, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board, overlap):

    wind = 0
    up = 0
    down = 0

    routes_found = []

    # get optimal search range
    if route[0][0] > end_coordinate[0]:
        x_range = (end_coordinate[0], route[0][0])

    else:
        x_range = (route[0][0], end_coordinate[0])
    
    if route[0][1] > end_coordinate[1]:
        y_range = (end_coordinate[1], route[0][1])
    
    else:
        y_range = (route[0][1], end_coordinate[1])


    for index, line in enumerate(netlist):

        closest_point = []

        for point in line.route:

            # point ligt tussen end_coordinate en huidige punt
            # find closest point in optimal search range
            if (point[0] >= x_range[0] and point[0] <= x_range[1]) and (point[1] >= y_range[0] and point[1] <= y_range[0]): 
                found = find_random_route(route[-1], point, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)

                if found[1]:
                    closest_point.append(len(found[0]))
        
        if closest_point:
            routes_found.append((index, min(closest_point)))

    if routes_found:
        routes_found = sorted(routes_found, key=lambda x: x[1])
        return routes_found[0][0]

    return False
