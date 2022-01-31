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

def find_routes(chips_dict, netlist, wind, up, down, board, options = 5, len_choices = 50, shuffels = 5):
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

    empty = not_found(netlist)
   
    print("Hill climber")

    # allow intersections for routes that couldn't initially be found
    overlap = True

    manhattan_routes = []

    wind = 0
    up = 0
    down = 0

    for index, line in enumerate(netlist):
        if not line.route:
            start_coordinate = chips_dict[line.start]
            end_coordinate = chips_dict[line.end]
            
            line.route = find_random_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)[0]

            board.lines.extend(line.route[1:-1])

            manhattan_routes.append(index)


    #(wind, up, down)
    print("start value cost: ", costs(netlist))

    all_routes = [x for x in range(len(netlist))]
    if manhattan_routes:

        for i in range(shuffels):
            print(i)
            combis = []

            #TODO: try range 10, bigger RNG?
            choices = [x for x in range(options)]
            # and also try range 100, more options to try
            for _ in range(len_choices):
                #TODO: find which combis provide improvement
                wind_option = random.choice(choices)
                up_option = random.choice(choices)
                down_option = random.choice(choices)
                
                # in virtually all cases, relatively high up-values don't result in improvement
                while wind_option < up_option and down_option < up_option:
                    wind_option = random.choice(choices)
                    up_option = random.choice(choices)
                    down_option = random.choice(choices)

                combis.append( (random.choice(choices), random.choice(choices), random.choice(choices)) )

            combis = set(combis)
            random.shuffle(all_routes)
            for index in all_routes:
                
                for cost in combis:
                    wind = cost[0]
                    up = cost[1]
                    down = cost[2]
                    line = netlist[index]

                    old_cost = route_costs(board, line.route)

                    temp_board = copy.deepcopy(board)

                    for coordinate in line.route[1:-1]:
                        temp_board.lines.remove(coordinate)
                    
                    new_route = find_random_route(line.route[0], line.route[-1], chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, temp_board, overlap)

                    if new_route[1]:
                        temp_board.lines.extend(new_route[0][1:-1])
                        
                        new_cost = route_costs(temp_board, new_route[0])

                        if new_cost < old_cost:
                            print("Good wind, up, down: ", wind, up, down)
                            line.route = new_route[0]
                            board = temp_board
                            print("new netlist cost:", costs(netlist))


    # for every manhattan route, remove it, use x different heuristic methods and save the best route.


    # optie: lijnstuk weghalen en daartussen nieuwe route leggen met semirandomheid
    # optie: op recht stuk 2 aangrenzende coordinaten samen 1 stap een loodrechte richting op laten maken (dit voor verschillende situaties hardcoden) (poep)
    # optie: heuristiek kosten aanpassen en dan de lijn nemen met de beste heuristiek in die situatie!

    # probeer x aantal keer te verbeteren (muteren)

    return netlist, empty

#
def recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap):
    global recursion_counter
    recursion_counter += 1

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

        return route

    else:
        # add board lines     
        board.lines.extend(route[0][1:-1])
        return route[0]


def main(chip, net, wind = 0, up = 0, down = 0, options = 5, len_choices = 50, shuffels = 5, draw = True):
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    
    netlist_routes = find_routes(chips_dict, netlist, wind, up, down, board, options, len_choices, shuffels)

    if draw:
        create_grid(chips_dict, netlist_routes[0])
    
    cost = create_output(netlist_routes[0], chip, net)

    # output how many not found and cost
    return netlist_routes[1], cost
