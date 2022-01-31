"""
* algorithm.py
* Tries to find a route from the start coordinate of a chip to the end coordinate of the chip with A* algoritm
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import queue
import copy
import random
from typing import List

from helper import *
from options import *

def find_route(
    start_coordinate, end_coordinate, chips_dict, board_size, board, overlap, wind = 0, up = 0, down = 0):
    """
    Takes a start coordinate, end coordinate, chips dictionary, board coordinate extremes, heuristics, board and overlap.
    """
    # route can not cross another chip
    invalid_chip_coords = list(chips_dict.values())

    if end_coordinate in invalid_chip_coords:
        invalid_chip_coords.remove(end_coordinate)
    
    return astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, board_size, wind, up, down, board, overlap)


def astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, board_size, wind, up, down, board, overlap):
    """
    Returns the best route between two coordinates according to an A* algorithm.
    If no route could be found, return the best unfinished route.
    """
    q = queue.Queue()
    q.put([start_coordinate])

    # (route, distance)
    best_unfinished_child = ([start_coordinate], manhattan_distance(start_coordinate, end_coordinate))

    while not q.empty():
        route = q.get()

        unfinished_route_costs = []

        # if a complete route is found return: route, True, else append the route, costs tuple to unfinished_route_costs
        # TODO: new name for a?
        a = get_finished_route_else_update_route_costs(route, invalid_chip_coords, board_size, wind, up, down, board, overlap, end_coordinate, unfinished_route_costs)
        if type(a) == tuple:
            return  a

        # put child with lowest cost
        if len(unfinished_route_costs) > 0:
            best_unfinished_child, best_child_path = find_best_child(unfinished_route_costs, end_coordinate, best_unfinished_child)

            q.put(best_child_path)

    # no route found, return best unfinished route
    return best_unfinished_child[0], False


# TODO: misschien beter functie naam? is deze funcie wel handig?
def get_finished_route_else_update_route_costs(route, invalid_chip_coords, board_size, wind, up, down, board, overlap, end_coordinate, unfinished_route_costs):
    """
    Checks if new coordinate completes the route if so it returns the route, True. Else returns false.
    For each valid direction the function appends the new possible route, costs to the unfinished_route_costs list.
    """
    for i in valid_directions(
            route[-1], invalid_chip_coords, route, board_size, wind, up, down, board, overlap
        ):
            child = copy.deepcopy(route)
            child.append(i[0])

            # if end is found, return this route
            if i[0] == end_coordinate:
                return child, True
            
            # append every unfinished route to the costs list
            unfinished_route_costs.append((child, f_value(board, child, i[0], end_coordinate, i[1])))

    return False

# TODO
def hill_climber(netlist, chips_dict, board_size, board, options, len_choices, shuffels):
    """
    """
    # allow overlap for routes that could not initially be found
    overlap = True

    manhattan_routes = []

    # find the routes that initially could not be solved without overlap
    for index, line in enumerate(netlist):
        if not line.route:
            start_coordinate = chips_dict[line.start]
            end_coordinate = chips_dict[line.end]
            
            line.route = find_route(start_coordinate, end_coordinate, chips_dict, board_size, board, overlap)[0]

            board.lines.extend(line.route[1:-1])

            manhattan_routes.append(index)

    # print the start value of the costs
    print("start value cost: ", costs(board, netlist))

    # gets all route
    all_routes = [x for x in range(len(netlist))]
    for i in range(shuffels):
        print(i)
        combis = []

        #TODO: try range 10, bigger RNG?
        choices = [x for x in range(options)]
        # and also try range 100, more options to try
        for _ in range(len_choices):
            #TODO: find which combis provide improvement
            wind_option = random.choice(choices)
            up_option = random.choice(choices)
            down_option = random.choice(choices)
            
            # in virtually all cases, relatively high up-values don't result in improvement
            while wind_option < up_option and down_option < up_option:
                wind_option = random.choice(choices)
                up_option = random.choice(choices)
                down_option = random.choice(choices)

            combis.append( (random.choice(choices), random.choice(choices), random.choice(choices)) )

        combis = set(combis)
        random.shuffle(all_routes)
        for index in all_routes:
            
            for cost in combis:
                wind = cost[0]
                up = cost[1]
                down = cost[2]
                line = netlist[index]

                old_cost = route_costs(board, line.route)

                temp_board = copy.deepcopy(board)

                # removes route
                temp_board.remove_route(line)
                
                new_route = find_route(line.route[0], line.route[-1], chips_dict, board_size, temp_board, overlap, wind, up, down)

                if new_route[1]:
                    temp_board.lines.extend(new_route[0][1:-1])
                    
                    new_cost = route_costs(temp_board, new_route[0])

                    if new_cost < old_cost:
                        print("Good wind, up, down: ", wind, up, down)
                        line.route = new_route[0]
                        board = temp_board
                        print("new netlist cost:", costs(board, netlist))

    return netlist, board



def closest_line_index(route, netlist, end_coordinate, chips_dict, board_size, board, overlap):
    """
    Returns the index from the closest line in the netlist to the current point, else false.
    """
    # get range between current point and end coordinate
    x_range, y_range = search_range(route[0], end_coordinate)

    routes_found = []

    # for each point x on each excisiting line
    for index, line in enumerate(netlist):
        closest_point = closest_point_per_line(line, x_range, y_range, route[-1], chips_dict, board_size, board, overlap)

        # if at least one reachable point is found, get distance from point closest to current point
        if closest_point:
            routes_found.append((index, min(closest_point)))
    
    # if at least one line with a reachable point is found, return index closest line
    if routes_found:
        routes_found = sorted(routes_found, key=lambda x: x[1])
        return routes_found[0][0]

    # no reachable lines in range found
    return False


def closest_point_per_line(line, x_range, y_range, coordinate, chips_dict, board_size, board, overlap):
    """
    Given a line and a coordinate, trys to find the point on the line with the clostest a* distance.
    """
    closest_point = []

    for point in line.route:
        # check if point is in range
        if (point[0] >= x_range[0] and point[0] <= x_range[1]) and (point[1] >= y_range[0] and point[1] <= y_range[0]): 
            # make sure the point is reachable from the current point
            found = find_route(coordinate, point, chips_dict, board_size, board, overlap)

            # if reachable, remember the distance from the point to the current point
            if found[1]:
                closest_point.append(len(found[0]))

    return closest_point
