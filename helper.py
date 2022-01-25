"""
* helper.py
* Creates helper functions used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from scipy.spatial.distance import cityblock

def route_costs(board, route):
    n = len(route) - 1

    counts = dict()
    for coordinate in board.lines:
        if coordinate in counts:
            counts[coordinate] += 1
        else:
            counts[coordinate] = 1

    k = sum(value - 1 for value in counts.values())

    return n + 300 * k

def sorted_manhattan_distance(chips_dict, netlist):
    temp = []

    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        a = [start_coordinate[0], start_coordinate[1], start_coordinate[2]]  
        b = [end_coordinate[0], end_coordinate[1], end_coordinate[2]]  

        temp.append((line, cityblock(a, b)))
    
    temp = sorted(temp, key=lambda x: x[1])

    return [x[0] for x in temp]


def manhattan_distance(start, end):
    a = [start[0], start[1], start[2]]
    b = [end[0], end[1], end[2]]
    return cityblock(a, b)

def is_not_collision(current_coordinate, board):
    return current_coordinate not in board.lines


def get_board_size(chips_dict):
    """
    gets max and min coordinates
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

    # number of 3D layers is hardcoded (always 8)
    return min_x, max_x, min_y, max_y, 0, 7


def costs(netlist):
    """
    computes costs of whole netlist
    """
    n = 0
    route_coords = []
    for line in netlist:
        if len(line.route) > 0:
            n += len(line.route) - 1
            route_coords.append(line.route[1:-1])

    counts = dict()
    for route in route_coords:
        for coordinate in route:
            if coordinate in counts:
                counts[coordinate] += 1
            else:
                counts[coordinate] = 1

    k = sum(value - 1 for value in counts.values())

    return n + 300 * k


def not_found(netlist):
    empty = 0

    for x in netlist:
        if not x.route:
            empty += 1
    
    print("not found: ",empty)
    return empty
