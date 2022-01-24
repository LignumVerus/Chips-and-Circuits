"""
* main.py
* Finds the best routes between chips using [insert algorithm here]
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from bcrypt import re
import numpy as np
import sys
import random
import queue
import copy

from classes import Chip, Line, Board
from helper import *
from loader import *
from output import *


def find_routes(chips_dict, netlist, board):
    """
    needs to return list of Line
    """
    # gets board size
    min_x, max_x, min_y, max_y, min_z, max_z = get_board_size(chips_dict)

    netlist = sorted_manhattan_distance(chips_dict, netlist)

    print(len(netlist))
    count = 0
    not_found = 0
    
    # find from which to which coordinate the line has to go
    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        line.route = find_random_route(
            start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board
        )

        board.lines.extend(line.route[1:-1])

        count += 1
        print(count)
        if len(line.route) == 0:
            not_found += 1

    print("not found: ", not_found)


    print("START OPTIMIZING")
    
    optimized_routes = 0

    for line in netlist: 

        current_route = line.route

        better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board)
        
        while len(better) < len(current_route):
            current_route = better
            better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board)
        
        optimized_routes += 1
        print(optimized_routes)
        line.route = current_route
        
        

    # board.add_lines(route1, route2)
    return netlist

    
    # find_route(x_start, y_start x_end, y_end)
    # pass

# algorithm route
# *prevent self collisions
# *prevent collisions with other routes
# give crossing last priority (except when it would be longer than 300 steps?) (currently forbidden)
# prioritize x and y directions over z directions
# *sort netlist on manhattan distance
# *place shortest manhattan distance routes first, then increasingly longer?
# *xmax-xmin + ymax-ymin + zmax-zmin
# 

def optimize_route(route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board):
    for i, point_one in enumerate(route):
        # idee: laat punt 2 bij de laatste beginnen
        for j, point_two in enumerate(route[i:]):
            distance = manhattan_distance(point_one, point_two)
            route_distance = j - i

            if distance > 1 and route_distance > distance:
                new_route = find_random_route(point_one, point_two, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board)

                if len(new_route) < route_distance and len(new_route) > 0:

                    if len(route[:i]) > 0 and len(route[j:]) > 0: 
                        temp = route[:i]

                        temp.extend(new_route)
                        temp.extend(route[j + 1:])

                        route = temp
                    
                    elif len(route[:i]) > 0:
                        temp = route[:i]

                        temp.extend(new_route)

                        route = temp
                    
                    elif len(route[j:]) > 0:
                        temp = route[j + 1:]
                        
                        new_route.extend(temp)

                        route = new_route
                    
                    else:
                        route = new_route
                    
                    return route
    
    return route
            




def find_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z):

    pass


def find_random_route(
    start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board
):
    """
    creates random route
    """
    # route = []
    # route.append(start_coordinate)

    # gets list of chips not on start and end coordinate
    invalid_chip_coords = list(chips_dict.values())

    if end_coordinate in invalid_chip_coords:
        invalid_chip_coords.remove(end_coordinate)

    q = queue.Queue()
    q.put([start_coordinate])

    # g = cost? of the route travelled
    # h = manhattan distance between current coord and end coord
    # f = g + h (total cost)

    while not q.empty():
        route = q.get()

        costs = []

        for i in valid_directions(
            route[-1], invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, board
        ):
            child = copy.deepcopy(route)
            child.append(i)

            if i == end_coordinate:
                # print(len(board.lines))
                return child

            g = route_costs(board, child)
            # meer kosten als het op dezelfde laag blijft voor meer ruimte onderin
            # meer kosten als de route dicht bij een andere lijn komt
            # lijnen (random, langste, grootste afwijking met man_dis) weghalen, kijken of er dan een andere lijn wel kan
            h = manhattan_distance(i, end_coordinate)
            f = g + h

            costs.append((child, f))

        # put child with lowest cost
        if len(costs) > 0:
            best_child = sorted(costs, key=lambda x: x[1])[0]
            best_child_path = best_child[0]
            q.put(best_child_path)

    # TO DO: error melding! 
    return []

    # while current_coordinate != end_coordinate:


    #     # get all valid directions
    #     choices = 

    #     # update current coord with random choice
    #     if choices:
    #         print("full", choices)
    #         current_coordinate = random.choice(choices)
    #     # if there are no choices left, get directions for the previous coord, remove the bad coord and remove it from the route
    #     else:
    #         while not choices:
    #             choices = valid_directions(route[-2], invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, board)
    #             print("empty", choices)
    #             route.remove(current_coordinate)
    #             choices.remove(current_coordinate)

    #         current_coordinate = random.choice(choices)

    #     # add coord to route
    #     route.append(current_coordinate)

    # return route

def valid_directions(
    current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, board
):
    """
    finds all possible directions from point in grid
    """
    choices = []

    # west
    if (
        # can't go out of board
        current_coordinate[0] - 1 >= min_x
        # can't go over another chip
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        # can't collide with another line
        and is_not_collision((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]), board)
        # can't collide with own route
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]))

    # east
    if (
        current_coordinate[0] + 1 <= max_x
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), board)
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]))

    # north
    if (
        current_coordinate[1] - 1 >= min_y
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]))

    # south
    if (
        current_coordinate[1] + 1 <= max_y
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]))

    # down
    if (
        current_coordinate[2] - 1 >= min_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1))

    # up
    if (
        current_coordinate[2] + 1 <= max_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1))

    # check if coord is backtracking
    if len(route) > 2:
        # cannot go back to previous coordinate
        for choice in choices:
            if choice == route[-2]:
                # delete invalid choice from choices
                choices.remove(choice)

    return choices


def main(chip, net):
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    netlist_routes = find_routes(chips_dict, netlist, board)
    create_grid(chips_dict, netlist_routes)

    create_output(netlist_routes, chip, net)


# arg1 = chip , arg2 = net
main(sys.argv[1], sys.argv[2])
