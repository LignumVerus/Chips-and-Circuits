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
import random
import queue
import copy

from classes import Chip, Line, Board
from helper import *
from loader import *
from output import *


def find_routes(chips_dict, netlist, wind, up, down, board):
    """
    needs to return list of Line
    """
    # gets board size
    min_x, max_x, min_y, max_y, min_z, max_z = get_board_size(chips_dict)

    netlist = sorted_manhattan_distance(chips_dict, netlist)
    
    not_found = 0

    reroute_list = []
    
    # find from which to which coordinate the line has to go
    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        line.route = find_random_route(
            start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
        )


        board.lines.extend(line.route[1:-1])
        
        # add longest routes in comparison to manhattan distance to reroute list
        multiplier = 1.5

        #add longest AND empty. First reroute all empty then all longest. shuffle independently?.
        
        try:
            if len(line.route) > multiplier * manhattan_distance(line.route[0], line.route[-1]):
                reroute_list.append(netlist.index(line))
        except IndexError:
            pass

        if len(line.route) == 0:
            not_found += 1

    print("not found: ", not_found)

    # lijnen (random, langste, grootste afwijking met man_dis) weghalen, kijken of er dan een andere lijn wel kan

    temp_board = copy.deepcopy(board)
    
    for index in reroute_list:
        print("reroute list: ", reroute_list)
        # remove old routes from tempboard you want to reroute 
        for coordinate in netlist[index].route[1:-1]:
            temp_board.lines.remove(coordinate)
    
    temp_board_new = copy.deepcopy(temp_board)

    # reroute routes in reroute list
    if reroute_list:
        # shuffle the list 
        random.shuffle(reroute_list)

        for i, index in enumerate(reroute_list):
            line = netlist[index]
            old_route = copy.deepcopy(line.route)
            
            if i == 0:
                new_board = temp_board

            # try to create shorter route or different route of same length
            start_coordinate = chips_dict[line.start]
            end_coordinate = chips_dict[line.end]
            new_route = find_random_route(
                start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, new_board)

            temp_board.lines.extend(old_route[1:-1])
            temp_board_new.lines.extend(new_route[1:-1])

            # go back to old board when no improvement
            if route_costs(temp_board_new, new_route) > route_costs(temp_board, old_route):
                temp_board_new.lines[:-len(new_route)]
                temp_board_new.lines.extend(old_route[1:-1])
                line.route = old_route

                new_board = temp_board_new

            else:
                temp_board.lines[:-len(old_route)]
                temp_board.lines.extend(new_route[1:-1])
                line.route = new_route

                new_board = temp_board

        #check if total costs of new board are better
        board = new_board
            


    print("START OPTIMIZING")
    
    wind = 0
    up = 0
    down = 0

    for line in netlist: 

        current_route = line.route

        better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)
        
        while len(better) < len(current_route):
            current_route = better
            better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)

        line.route = current_route
   
    return netlist, not_found


def optimize_route(route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board):
    for i, point_one in enumerate(route):
      
        for j, point_two in enumerate(route[i:]):
            distance = manhattan_distance(point_one, point_two)
            route_distance = j - i

            if distance > 1 and route_distance > distance:
                new_route = find_random_route(point_one, point_two, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)

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
    start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
):
    """
    creates random route
    """

    # gets list of chips not on start and end coordinate
    invalid_chip_coords = list(chips_dict.values())

    if end_coordinate in invalid_chip_coords:
        invalid_chip_coords.remove(end_coordinate)

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

            if i[0] == end_coordinate:
                return child

            g = route_costs(board, child)
            h = manhattan_distance(i[0], end_coordinate) + i[1]
            f = g + h

            costs.append((child, f))

        # put child with lowest cost
        if len(costs) > 0:
            best_child = sorted(costs, key=lambda x: x[1])[0]
            best_child_path = best_child[0]
            q.put(best_child_path)

    return []


def valid_directions(
    current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
):
    """
    finds all possible directions from point in grid
    """
    choices = []

    cost_west = wind
    cost_east = wind
    cost_north = wind
    cost_south = wind
    cost_up = up
    cost_down = down

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
        choices.append(((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]), cost_west))

    # east
    if (
        current_coordinate[0] + 1 <= max_x
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), board)
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), cost_east))

    # north
    if (
        current_coordinate[1] - 1 >= min_y
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), cost_north))

    # south
    if (
        current_coordinate[1] + 1 <= max_y
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), cost_south))

    # down
    if (
        current_coordinate[2] - 1 >= min_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), cost_down))

    # up
    if (
        current_coordinate[2] + 1 <= max_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), cost_up))

    # check if coord is backtracking
    if len(route) > 2:
        # cannot go back to previous coordinate
        for choice in choices:
            if choice[0] == route[-2]:
                # delete invalid choice from choices
                choices.remove(choice)

    return choices


def main(chip, net, wind = 0, up = 0, down = 0, draw = True):
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    netlist_routes = find_routes(chips_dict, netlist, wind, up, down, board)

    if draw:
        create_grid(chips_dict, netlist_routes[0])
        create_output(netlist_routes[0], chip, net)

    # output how many found
    return netlist_routes[1]
