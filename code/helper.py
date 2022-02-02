"""
* helper.py
* Creates helper functions used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from scipy.spatial.distance import cityblock
import random


def f_value(board, child, start, end, extra_cost):
    """
    Calculates f-value for a* algorithm.
    """
    g = route_costs(board, child)
    h = manhattan_distance(start, end) + extra_cost
    return g + h


def route_costs(board, route):
    """
    Takes a board and a route and returns the cost of that route.
    """
    n = len(route) - 1
    counts = dict()

    for coordinate in board.lines:
        if coordinate in counts:
            counts[coordinate] += 1
        else:
            counts[coordinate] = 1

    k = sum(value - 1 for value in counts.values())

    return n + 300 * k


def costs(board, netlist):
    """
    Takes a board and netlist and returns the cost of the netlist. Does not call 'route_costs' to improve runtime.
    """
    counts = dict()

    for coordinate in board.lines:
        if coordinate in counts:
            counts[coordinate] += 1
        else:
            counts[coordinate] = 1

    k = sum(value - 1 for value in counts.values())
    n = len(board.lines) + len(netlist)

    return n + 300 * k


def manhattan_distance(start, end):
    """
    Returns the Manhattan distance between two coordinates.
    """
    a = [start[0], start[1], start[2]]
    b = [end[0], end[1], end[2]]

    return cityblock(a, b)


def sorted_manhattan_distance(chips_dict, netlist):
    """
    Takes a chips dictionary and a netlist, and returns the netlist sorted by ascending Manhattan distance.
    """
    temp = []

    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        distance = manhattan_distance(start_coordinate, end_coordinate)

        temp.append((line, distance))

    temp = sorted(temp, key=lambda x: x[1])

    return [x[0] for x in temp]


def is_not_collision(current_coordinate, board):
    """
    Returns whether a coordinate does not collide with another line.
    """
    return current_coordinate not in board.lines


def get_board_size(chips_dict):
    """
    Calculates the extremes of the x, y and z of the board.
    The board width and length are one bigger than the minimum and maximum coordinates of the chips.
    The height is always 8 (level 0 to 7).
    """
    x_list = []
    y_list = []

    for coord in chips_dict.values():
        x_list.append(coord[0])
        y_list.append(coord[1])

    min_x = min(x_list) - 1
    max_x = max(x_list) + 1
    min_y = min(y_list) - 1
    max_y = max(y_list) + 1

    return min_x, max_x, min_y, max_y, 0, 7


def search_range(route, end_coordinate):
    """
    Takes a route and a coordinate and returns the optimal search range to finish the route towards the end coordinate.
    """
    if route[0] > end_coordinate[0]:
        x_range = (end_coordinate[0], route[0])

    else:
        x_range = (route[0], end_coordinate[0])

    if route[1] > end_coordinate[1]:
        y_range = (end_coordinate[1], route[1])

    else:
        y_range = (route[1], end_coordinate[1])

    return x_range, y_range


def not_found(netlist):
    """
    Returns the number of empty routes in a netlist.
    """
    empty = 0

    for x in netlist:
        if not x.route:
            empty += 1

    return empty


def find_best_child(unfinished_route_costs, end_coordinate, best_unfinished_child):
    """
    Finds the best (unfinished) child given current best (unfinisged) child.
    """
    # find child with the lowest costs
    best_child = sorted(unfinished_route_costs, key=lambda x: x[1])[0]
    best_child_path = best_child[0]

    new_distance = manhattan_distance(best_child_path[-1], end_coordinate)

    # find child with closest manhattan distance for if route not found
    if new_distance < best_unfinished_child[1]:
        best_unfinished_child = (best_child_path, new_distance)

    return best_unfinished_child, best_child_path


def random_combis(options, len_choices):
    """
    Returns a list of lenght len_choices with tuples with 3 random numbers in range options.
    The number in the middle of the tuple can never be the highest
    """
    # TODO: try range 10, bigger RNG?
    choices = [x for x in range(options)]
    # and also try range 100, more options to try

    combis = []
    for _ in range(len_choices):
        # TODO: find which combis provide improvement
        wind_option = random.choice(choices)
        up_option = random.choice(choices)
        down_option = random.choice(choices)

        # in virtually all cases, relatively high up-values don't result in improvement
        while wind_option < up_option and down_option < up_option:
            wind_option = random.choice(choices)
            up_option = random.choice(choices)
            down_option = random.choice(choices)

        combis.append(
            (random.choice(choices), random.choice(choices), random.choice(choices))
        )

    # remove duplicates
    return set(combis)
