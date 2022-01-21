"""
* main.py
* Finds the best routes between chips using [insert algorithm here]
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
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

    # find from which to which coordinate the line has to go
    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]
        line.route = find_random_route(
            start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board
        )

        board.lines.extend(line.route)
    
    # hier moet iets?
    # Herhaal:
        # Doe een kleine random aanpassing
        # Als de state is verslechterd:
            # Maak de aanpassing ongedaan

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

def find_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z):

    pass


def find_random_route(
    start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board
):
    """
    creates random route
    """
    route = []
    route.append(start_coordinate)
    current_coordinate = start_coordinate

    # gets list of chips not on start and end coordinate
    invalid_chip_coords = list(chips_dict.values())
    invalid_chip_coords.remove(end_coordinate)

    while current_coordinate != end_coordinate:

        # get all valid directions
        choices = valid_directions(current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, board)

        # update current coord with random choice
        if choices:
            current_coordinate = random.choice(choices)
        # if there are no choices left, get directions for the previous coord, remove the bad coord and remove it from the route
        else:
            while not choices:
                choices = valid_directions(route[-2], invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, board)
                route.remove(current_coordinate)
                choices.remove(current_coordinate)

            current_coordinate = random.choice(choices)

        # add coord to route
        route.append(current_coordinate)

    return route

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
        # and is_not_collision((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]), board)
        # can't collide with own route
        # and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]))

    # east
    if (
        current_coordinate[0] + 1 <= max_x
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        # and is_not_collision((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), board)
        # and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]))

    # north
    if (
        current_coordinate[1] - 1 >= min_y
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in invalid_chip_coords
        # and is_not_collision((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), board)
        # and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]))

    # south
    if (
        current_coordinate[1] + 1 <= max_y
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in invalid_chip_coords
        # and is_not_collision((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), board)
        # and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]))

    # down
    if (
        current_coordinate[2] - 1 >= min_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in invalid_chip_coords
        # and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), board)
        # and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1) not in route
    ):
        choices.append((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1))

    # up
    if (
        current_coordinate[2] + 1 <= max_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in invalid_chip_coords
        # and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), board)
        # and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1) not in route
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
