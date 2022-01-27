"""
* main.py
* Finds the best routes between chips using [insert algorithm here]
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import numpy as np
import random
import queue
import copy

from classes import Chip, Line, Board
from helper import *
from loader import *
from output import *
from algorithm import *
from optimize import *

recursion_counter = 0

def find_routes(chips_dict, netlist, wind, up, down, board):
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

        line.route = recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)
    
    print("START OPTIMIZING")
    netlist = optimize(netlist, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board)

    empty = not_found(netlist)

    return netlist, empty

#
def recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board):
    global recursion_counter
    recursion_counter += 1 

    # print("recursion count: ", recursion_counter)
    # print(id(netlist))

    route = find_random_route(
        start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
    )

    # if not found
    if not route[1]:
        closest_coordinate_list = []

        for coordinate in route[0]:
            closest_coordinate_list.append((coordinate, manhattan_distance(coordinate, end_coordinate)))
        
        coordinates = sorted(closest_coordinate_list, key=lambda x: x[1])

        for coordinate in coordinates:
            closest_coordinate = coordinate[0]

            for line in netlist:
                w = (closest_coordinate[0] - 1, closest_coordinate[1], closest_coordinate[2])
                e = (closest_coordinate[0] + 1, closest_coordinate[1], closest_coordinate[2])
                n = (closest_coordinate[0], closest_coordinate[1] - 1, closest_coordinate[2])
                s = (closest_coordinate[0], closest_coordinate[1] + 1, closest_coordinate[2])
                d = (closest_coordinate[0], closest_coordinate[1], closest_coordinate[2] - 1)
                u = (closest_coordinate[0], closest_coordinate[1], closest_coordinate[2] + 1)

                if line.route and (n in line.route or e in line.route or s in line.route or w in line.route or u in line.route or d in line.route):

                    for coordinate in line.route[1:-1]:
                        board.lines.remove(coordinate)
                    
                    line.route = []

                    # print("line removed, try finding new line")
                    route = recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)

                    # print("put removed line back on the board")
                    line.route = recursive(netlist, chips_dict[line.start], chips_dict[line.end], chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)  

                    #print("dit gebeurd hier voor, ", route)   
                    #print("route2:", route)         
                    board.lines.extend(route[1:-1])
                    return route
    else:
        #print("route 1:",route)
        board.lines.extend(route[0][1:-1])
        return route[0]

    # Voor elke coordinaat in de laatste willekeurige child is er niet 1 aangrensende lijn
    print("GAAT FOUT")
    return []


def main(chip, net, wind = 0, up = 0, down = 0, draw = True):
    
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    
    netlist_routes = find_routes(chips_dict, netlist, wind, up, down, board)

    if draw:
        create_grid(chips_dict, netlist_routes[0])
    
    cost = create_output(netlist_routes[0], chip, net)

    # output how many not found and cost
    return netlist_routes[1], cost
