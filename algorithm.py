import queue
import copy

from helper import *
from options import *

def astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board):
    q = queue.Queue()
    q.put([start_coordinate])

    while not q.empty():
        route = q.get()

        costs = []

        for i in valid_directions(
            route[-1], invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
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
            q.put(best_child_path)

    # no route found, return unfinished route (last child)
    # try with other children closest to end coordinate?
    try:
        return child, False
    except UnboundLocalError:
        # print("HOI")
        return [start_coordinate], False

