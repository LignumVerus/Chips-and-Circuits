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

    # overlap is not allowed
    overlap = False
   
    # find from which to which coordinate the line has to go
    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        line.route = recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)
        optimize(line, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board, overlap)
    
    # Prepare for hillclimber
    # routes die niet gevonden zijn leggen met kruisen
    overlap = True

    for line in netlist:
        if not line.route:
            start_coordinate = chips_dict[line.start]
            end_coordinate = chips_dict[line.end]
            
            line.route = find_random_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)[0]
            board.lines.extend(line.route[0][1:-1])

    # regels voor kruisen (kunnen ook gewoon de kortste route leggen)

    # optie: lijnstuk weghalen en daartussen nieuwe route leggen met semirandomheid
    # optie: op recht stuk 2 aangrenzende coordinaten samen 1 stap een loodrechte richting op laten maken (dit voor verschillende situaties hardcoden) (poep)
    # optie: heuristiek kosten aanpassen en dan de lijn nemen met de beste heuristiek in die situatie!

    # probeer x aantal keer te verbeteren (muteren)


    print("START OPTIMIZING")

    empty = not_found(netlist)

    return netlist, empty

#
def recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap):
    global recursion_counter
    recursion_counter += 1

    # print("recursion count: ", recursion_counter)
    # print(id(netlist))

    route = find_random_route(
        start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap
    )

    # if not found
    if not route[1]:
        i = 0
        index_line = closest_line_index(route[0][i][0], netlist, end_coordinate, chips_dict, min_x, max_x,  min_y, max_y, min_z, max_z, board, overlap)

        if index_line is False:
            print("geen lijn gevonden")
            return []

        line = netlist[index_line]

        # remove board lines
        for coordinate in line.route[1:-1]:
            board.lines.remove(coordinate)
      
        line.route = []

        # print("line removed, try finding new line")
        route = recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)

        # print("put removed line back on the board")
        line.route = recursive(netlist, chips_dict[line.start], chips_dict[line.end], chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)  
        optimize(line, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board, overlap)
        #print("route2:", route)
        return route

    else:
        #print("route 1:",route)
        # add board lines
        board.lines.extend(route[0][1:-1])
        return route[0]


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
