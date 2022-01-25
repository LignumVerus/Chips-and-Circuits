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

    # empty routes
    # reroute_list_0 = queue.Queue()
    # all other routes
    # long_routes = []
    
    # find from which to which coordinate the line has to go
    for line in netlist:
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]

        line.route = recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)
    
    print("START OPTIMIZING")
    # netlist = optimize(netlist, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board)

    empty = not_found(netlist)

    return netlist, empty

#
def recursive(netlist, start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board):
    global recursion_counter
    recursion_counter += 1 

    print("recursion count: ", recursion_counter)
    # print(id(netlist))

    route = find_random_route(
        start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
    )

    # add longest routes in comparison to manhattan distance to reroute list
    # multiplier = 1.5

    #add longest AND empty. First reroute all empty then all longest. shuffle independently?
    if not route[1]:
        # reroute_list_0.put(netlist.index(line))

        # find coordinate with shortest manhattan distance to end
        # shortest_distance = manhattan_distance(start_coordinate, end_coordinate)
        closest_coordinate_list = []
        # closest_coordinate = start_coordinate
        # closest_coordinate_list.append(closest_coordinate)

        for coordinate in route[0]:
            closest_coordinate_list.append((coordinate, manhattan_distance(coordinate, end_coordinate)))
        
        coordinates = sorted(closest_coordinate_list, key=lambda x: x[1])
            # print("*", coordinate, end_coordinate)
            # new_distance = manhattan_distance(coordinate, end_coordinate)
            # if new_distance < shortest_distance:
            #     shortest_distance = new_distance
            #     closest_coordinate = coordinate
        

        #     closest_coordinate_list.append(coordinate)
        # print("*", closest_coordinate)
                    
        # find which line blocks the path
        tem = 0

        for closest_coordinate in coordinates:
            closest_coordinate = closest_coordinate[0]

            for line in netlist:
                w = (closest_coordinate[0] - 1, closest_coordinate[1], closest_coordinate[2])
                e = (closest_coordinate[0] + 1, closest_coordinate[1], closest_coordinate[2])
                n = (closest_coordinate[0], closest_coordinate[1] - 1, closest_coordinate[2])
                s = (closest_coordinate[0], closest_coordinate[1] + 1, closest_coordinate[2])
                d = (closest_coordinate[0], closest_coordinate[1], closest_coordinate[2] - 1)
                u = (closest_coordinate[0], closest_coordinate[1], closest_coordinate[2] + 1)

                tem += 1

                if line.route and (n in line.route or e in line.route or s in line.route or w in line.route or u in line.route or d in line.route):

                    #print("old route, ", line.route)
                    # verwijder line
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


    # eerste item is het langste in vergelijking met de man_dis
    # long_routes = sorted(long_routes, key=lambda x: x[1])
    
        
        # elif len(line.route) > multiplier * manhattan_distance(line.route[0], line.route[-1]):
        #     # TODO: sorted on difference between actual length and manhattan distance
        #     reroute_list_1.append(netlist.index(line))

        # count += 1
        # print(count)

    # lijnen (random, langste, grootste afwijking met man_dis) weghalen, kijken of er dan een andere lijn wel kan

    # keep going until all routes have been made
    # i = 0
    
    # while not reroute_list_0.empty() and i < 1000:
    #     print(i)
    #     # neem een lege route (verwijder uit reroute_list_0)
    #     empty_route = reroute_list_0.get()
    #     line_empty = netlist[empty_route]
    #     # verwijder 1 lange (langste) route uit board.lines en uit line
    #     long_route = long_routes.pop(0)
    #     #           (line, index in netlist)
    #     line_long = (netlist[long_route[0]], long_route[0])
        
    #     # remove the coordinates of the long route from the board
    #     for coordinate in line_long[0].route[1:-1]:
    #         board.lines.remove(coordinate)
        
    #     # save the long routes
    #     line_long_list = []
    #     line_long_list.append(line_long)
        
    #     # remove the route
    #     line_long[0].route = []
    
    #     # probeer lege route te leggen
    #     start_coordinate = chips_dict[line_empty.start]
    #     end_coordinate = chips_dict[line_empty.end]
    #     new_route = find_random_route(
    #         start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)[0]

    #     # keep going until a route has been made for this route
    #     j = 0
    #     while not new_route and j < 1000:
    #         # verwijder nog een lange route tot het wel lukt
    #         long_route_2 = long_routes.pop(0)
    #         line_long_2 = (netlist[long_route_2[0]], long_route_2[0])

    #         for coordinate in line_long_2[0].route[1:-1]:
    #             board.lines.remove(coordinate)

    #         # remove a route
    #         line_long_2[0].route = []
    #         line_long_list.append(line_long_2)
    #         # probeer nieuwe route te vinden
    #         new_route = find_random_route(
    #             start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)[0]
            
    #         j += 1

    #     # add the new route to the board and the line class
    #     line_empty.route = new_route
    #     board.lines.extend(new_route[1:-1])

    #     # leg verwijderde routes opnieuw
    #     for line in line_long_list:
    #         # leg route voor verwijderde lange route
    #         start_long = chips_dict[line[0].start]
    #         end_long = chips_dict[line[0].end]
    #         new_route_long = find_random_route(
    #             start_long, end_long, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)[0]
    #         if not new_route_long:
    #             reroute_list_0.put(line[1])
    #         else:
    #             line[0].route = new_route_long
    #             board.lines.extend(new_route_long[1:-1])
        
    #     # krijg nieuwe scores van de lines die een route hebben
    #     long_routes = []

    #     for line in netlist:
    #         if line.route:
    #             score = manhattan_distance(line.route[0], line.route[-1])/len(line.route)
    #             long_routes.append((netlist.index(line), score))
    
    #     long_routes = sorted(long_routes, key=lambda x: x[1])
        
    #     i += 1

    # # #--------------------------
    # # temp_board = copy.deepcopy(board)
    
    # # for index in reroute_list_1:
    # #     print("reroute list: ", reroute_list_1)
    # #     # remove old routes from tempboard you want to reroute 
    # #     for coordinate in netlist[index].route[1:-1]:
    # #         temp_board.lines.remove(coordinate)
    
    # temp_board_new = copy.deepcopy(temp_board)

    #     # # remove old routes in lines
    #     # for line in netlist:
    #     #     if line.route == netlist[index].route:
    #     #         line.route = []

    # # reroute routes in reroute list
    # if reroute_list_1 or reroute_list_0:
    #     # shuffle the list 
    #     random.shuffle(reroute_list_1)
    #     # add lists together
    #     reroute_list_0.extend(reroute_list_1)

    #     for i, index in enumerate(reroute_list_0):
    #         line = netlist[index]
            
    #         if line.route:
    #             old_route = copy.deepcopy(line.route)
            
    #         if i == 0:
    #             new_board = temp_board

    #         # try to create shorter route or different route of same length
    #         start_coordinate = chips_dict[line.start]
    #         end_coordinate = chips_dict[line.end]
    #         new_route = find_random_route(
    #             start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, new_board)

    #         temp_board.lines.extend(old_route[1:-1])
    #         temp_board_new.lines.extend(new_route[1:-1])
    #         #board.lines.extend(new_route[1:-1])

    #         # go back to old board when no improvement
    #         if route_costs(temp_board_new, new_route) > route_costs(temp_board, old_route):
    #             temp_board_new.lines[:-len(new_route)]
    #             temp_board_new.lines.extend(old_route[1:-1])
    #             line.route = old_route

    #             new_board = temp_board_new
    #             #board.lines.extend(old_route[1:-1])

    #         else:
    #             temp_board.lines[:-len(old_route)]
    #             temp_board.lines.extend(new_route[1:-1])
    #             line.route = new_route
    #             # gaat fout line.route = new_route

    #             new_board = temp_board

        
    #     # TODO: kijken welk board beter is en die (overschrijven) als nieuwe board
    #     #check if total costs of new board are better
    #     board = new_board


def find_random_route(
    start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
):
    """
    creates route 
    """
    # route can not cross another chip
    invalid_chip_coords = list(chips_dict.values())

    if end_coordinate in invalid_chip_coords:
        invalid_chip_coords.remove(end_coordinate)
    
    return astar_algorithm(start_coordinate, end_coordinate, invalid_chip_coords, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)




def main(chip, net, wind = 0, up = 0, down = 0, draw = True):
    
    # create a board
    board = Board([])
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    
    netlist_routes = find_routes(chips_dict, netlist, wind, up, down, board)

    if draw:
        create_grid(chips_dict, netlist_routes[0])
        create_output(netlist_routes[0], chip, net)

    # output how many not found
    return netlist_routes[1]
