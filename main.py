"""
* main.py
* Finds the best routes between chips using [insert algorithm here]
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from tracemalloc import start
import numpy as np
import random
import queue
import copy

# TODO: Change import * to functions
from classes import Line, Board
from helper import *
from loader import *
from output import *
from algorithm import *
from optimize import *

recursion_counter = 0

def find_routes(chips_dict, netlist, wind, up, down, board, options = 5, len_choices = 50, shuffels = 5):
    """
    needs to return list of Line
    """
    # get board size
    board_size = get_board_size(chips_dict)
    
    # sort the netlist as to place presumed shorter routes first
    netlist = sorted_manhattan_distance(chips_dict, netlist)

    # overlap is (initially) not allowed
    overlap = False
   
    # solve all routes
    for line in netlist:
        # get start and end coordinate
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        # finds a route
        line.route = reroute(netlist, start_coordinate, end_coordinate, chips_dict, board_size, wind, up, down, board, overlap)

        # optimizes the route
        optimize(line, chips_dict, board_size, board)

    # TODO not needed
    empty = not_found(netlist)
   
    # prepare for hillclimber
    print("Hill climber")

    netlist, board = hill_climber(netlist, chips_dict, board_size, board, options, len_choices, shuffels)

    for line in netlist:
        optimize(line, chips_dict, board_size, board)

    # TODO do hill climber again

    # empty not needed
    return netlist, empty, board


def reroute(netlist, start_coordinate, end_coordinate, chips_dict, board_size, wind, up, down, board, overlap):
    """
    Finds route and optimizes it. If route cannot be found, remove the closest line, call the function again, place the removed route and optimize it.
    """
    route = find_route(
        start_coordinate, end_coordinate, chips_dict, board_size, board, overlap, wind, up, down)

    # route can be found
    if route[1]:
        # add board lines     
        board.lines.extend(route[0][1:-1])

        return route[0]

    # route cannot be found
    else:
        index_line = closest_line_index(route[0], netlist, end_coordinate, chips_dict, board_size, board, overlap)

        if index_line is False:
            print("geen lijn gevonden")
            return []

        line = netlist[index_line]

        # remove the route from the board 
        board.remove_route(line)
      
        line.route = []

        # print("line removed, try finding new line")
        route = reroute(netlist, start_coordinate, end_coordinate, chips_dict, board_size, wind, up, down, board, overlap)

        # print("put removed line back on the board")
        line.route = reroute(netlist, chips_dict[line.start], chips_dict[line.end], chips_dict, board_size, wind, up, down, board, overlap)  
        optimize(line, chips_dict, board_size, board)

        return route


def main(chip, net, wind = 0, up = 0, down = 0, draw = True, options = 5, len_choices = 50, shuffels = 5):
    """
    """
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    
    netlist_routes = find_routes(chips_dict, netlist, wind, up, down, board, options, len_choices, shuffels)

    if draw:
        create_grid(chips_dict, netlist_routes[0])
    
    # TODO cost does not need to be a variable
    cost = create_output(netlist_routes[0], chip, net, netlist_routes[2])

    # output how many not found and cost
    # TODO remove return
    return netlist_routes[1], cost
