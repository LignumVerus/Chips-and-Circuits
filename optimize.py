"""
* optimize.py
* Optimizes a line to generate lower costs
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from algorithm import find_route 
from helper import manhattan_distance, route_costs


def optimize(line, chips_dict, board_size, board, overlap = False):
    """
    Optimizes a line in-place.
    """
    # route that is going to be optimzed
    current_route = line.route

    # remove the route from the board
    board.remove_route(line)

    # optimze the route
    better = optimize_route(current_route, chips_dict, board_size, board, overlap)
    
    # keep trying to optimize route while better routes are found
    while len(better) < len(current_route):
        current_route = better
        better = optimize_route(current_route, chips_dict, board_size, board, overlap)

    # put the coordinates of the optimized route on the board
    board.lines.extend(current_route[1:-1])
    line.route = current_route


def optimize_route(route, chips_dict, board_size, board, overlap = False):
    """
    Tries to find one optimization for a route.
    """
    # loop from outer ends of route to the middle
    middle = int(len(route)/2)
    for i, point_one in enumerate(route[:middle]):
        for j, point_two in reversed(list(enumerate(route[middle:]))):
            distance = manhattan_distance(point_one, point_two)
            route_distance = j - i

            if distance > 1 and route_distance > distance:

                # find the shortest possible A* route between two points
                possible_new_route = find_route(point_one, point_two, chips_dict, board_size, board, overlap)
                new_route = possible_new_route[0]

                # check if the cost of this new route is lower than the cost of the old route
                if route_costs(board, new_route) <  route_costs(board, route[i:j]) and len(new_route) > 0 and possible_new_route[1]:
                    route = update_route(route, new_route, i, j)
                    return route

    # no better route is found
    return route

def update_route(route, new_route, i, j):
    """
    Between points i and j in route, insert new_route
    """
    # update in the middle of the old route
    if len(route[:i]) > 0 and len(route[j:]) > 0: 
        temp = route[:i]
        temp.extend(new_route)
        temp.extend(route[j + 1:])
        route = temp
    
    # update the end of the old route
    elif len(route[:i]) > 0:
        temp = route[:i]
        temp.extend(new_route)
        route = temp
    
    # update the beginning of the old route
    elif len(route[j:]) > 0:
        temp = route[j + 1:]
        new_route.extend(temp)
        route = new_route
    
    # update the whole route
    else:
        route = new_route
    
    return route