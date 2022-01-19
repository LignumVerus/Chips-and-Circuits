'''
* main.py
* Finds best routes between chips
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
'''
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys
import random


def read_csv_chips(filename, board):
    '''
    reads csv  print_0 and create chips
    '''

    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        
        chips_dict = {}

        # creates chips with id, x coordinate and y coordinate
        for row in csvreader:
            # Chip(id, x, y), DOET NU NIKS!!
            chip = Chip(row[0], row[1], row[2])
            #chip_list.append(chip)

            # add x and y coordinate to board
            board.add_chip(chip.x, chip.y)

            # Make a dictionary of all the chips, with the id as the key and tuple of coordinates as value
            chips_dict[row[0]] = (chip.x, chip.y)

    return chips_dict


def read_csv_netlist(filename):
    '''
    reads cvc file with netlist
    '''
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        netlist = []

        for number, row in enumerate(csvreader):
            try:
                # Line(id, chip_id_1, chip_id_2)
                line = Line(number, row[0], row[1], [])
                netlist.append(line)
            except IndexError:
                pass

    return netlist


def find_routes(chips_dict, netlist):
    '''
    Needs to return list of Line
    '''
    # gets board size
    min_x, max_x, min_y, max_y = get_board_size(chips_dict)

    # find from which to which coordinate the line has to go
    for i, line in enumerate(netlist):
        start_coordinate = chips_dict[line.start]
        end_coordinate = chips_dict[line.end]
        line.route = find_random_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y)   

    #board.add_lines(route1, route2)
    return netlist

    # find_route(x_start, y_start x_end, y_end)
    # pass


# algorithm route
# def find_route(x_start, y_start x_end, y_end):
#     pass



def find_random_route(start_coordinate, end_coordinate, chips_dict, min_x, max_x, min_y, max_y):
    '''
    creates random route
    '''
    route = []
    route.append(start_coordinate)

    current_coordinate = start_coordinate

    # gets list of chips not on start and end coordinate
    invalid_chip_coords = list(chips_dict.values())
    invalid_chip_coords.remove(end_coordinate)
    
    while current_coordinate != end_coordinate:
        # get all valid directions
        choices = valid_directions(current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y)

        # update current coord with random choice
        current_coordinate = random.choice(choices)

        # add coord to route
        route.append(current_coordinate)
        
    return route


def valid_directions(current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y):
    '''
    Finds all possible directions from point in grid
    '''
    choices = []

    # left
    if current_coordinate[0] - 1 >= min_x and (current_coordinate[0] - 1, current_coordinate[1]) not in invalid_chip_coords:
        choices.append((current_coordinate[0] - 1, current_coordinate[1]))
    
    # right
    if current_coordinate[0] + 1 <= max_x and (current_coordinate[0] + 1, current_coordinate[1]) not in invalid_chip_coords:
        choices.append((current_coordinate[0] + 1, current_coordinate[1]))

    # down
    if current_coordinate[1] - 1 >= min_y and (current_coordinate[0], current_coordinate[1] - 1) not in invalid_chip_coords:
        choices.append((current_coordinate[0], current_coordinate[1] - 1))
    
    # up
    if current_coordinate[1] + 1 <= max_y and (current_coordinate[0], current_coordinate[1] + 1) not in invalid_chip_coords:
        choices.append((current_coordinate[0], current_coordinate[1] + 1))

    
    # check if coord is backtracking
    if len(route) > 2:
        # cannot go back to previous coordinate
        for choice in choices:
            if choice == route[-2]:
                # delete invalid choice from choices
                choices.remove(choice)

    return choices


def get_board_size(chips_dict):
    '''
    gets max and min coordinates
    '''
    x_list = []
    y_list = []

    for coord in chips_dict.values():
        x_list.append(coord[0])
        y_list.append(coord[1])

    min_x = min(x_list) - 1 
    max_x = max(x_list) + 1
    min_y = min(y_list) - 1
    max_y = max(y_list) + 1

    return min_x, max_x, min_y, max_y



def create_grid(chips_dict, netlist_routes):
    '''
    visualizes grid
    '''
    id_list = chips_dict.keys()
    x_list = []
    y_list = []
    for coordinate in chips_dict.values():
        x_list.append(coordinate[0])
        y_list.append(coordinate[1])


    x_lines = []
    y_lines = []
    for lines in netlist_routes:
        for line in lines.route:
            x_lines.append(line[0])
            y_lines.append(line[1])

    # plot
    plt.scatter(x_list, y_list, zorder=2, s=300)
    plt.step(x_lines, y_lines, linewidth=2.5)
    for i, txt in enumerate(id_list):
        plt.annotate(txt, (x_list[i], y_list[i]), ha="center", va="center")

    plt.xlim([min(x_list) - 1, max(x_list) + 1])
    plt.ylim([min(y_list) - 1, max(y_list) + 1])
    plt.grid(visible=True, zorder=0)
    plt.title("Circuit Board Grid")
    plt.tight_layout()
    plt.savefig("plots/plot1.png")


def costs(netlist):
    '''
    computes costs
    '''
    n = 0
    route_coords = []
    for line in netlist:
        if len(line.route) > 0:
            n += len(line.route) - 1
            route_coords.append(line.route[1:-1])

    counts = dict()
    for route in route_coords:
        for coordinate in route:
            if coordinate in counts:
                counts[coordinate] += 1
            else:
                counts[coordinate] = 1

    k = sum(value - 1 for value in counts.values())

    return n + 300 * k


def create_output(netlist_routes, chip, net):
    '''
    writes output to CSV file
    '''
    with open(f"gates&netlists/chip_{chip}/output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["net", "wires"])

        for line in netlist_routes:
            newrow = (int(line.start), int(line.end))
            writer.writerow([tuple(newrow), line.route])

        cost = costs(netlist_routes)
        writer.writerow([f"chip_{chip}_net_{net}", int(cost)])


# chip class that has a function that
class Chip:
    def __init__(self, id, x, y):
        self.id = id
        self.x = int(x)
        self.y = int(y)


class Line:
    def __init__(self, id, chip_start, chip_end, route):
        self.id = id
        self.start = chip_start
        self.end = chip_end
        self.route = route


class Board:
    def __init__(self):
        # {(1,1): (chip_id, [line_id1, line_id2]}
        self.board = {}
    
    # add chip to dictionary with coordinates as key
    def add_chip(self, chip_x, chip_y):
        #TODO: add chip to dictonary
        #if coordinate not in dict, add to dict and add chip
        #else update entry
        pass

    # add line to dictionary with coordinates as key
    def add_line(self, line):
        #TODO: add line to dictionary
        #if coordinate not in dict, add to dict and add line
        #else update entry
        pass


def main(chip, net):
    # create a board 
    board = Board()
    chips_dict = read_csv_chips(f"gates&netlists/chip_{chip}/print_{chip}.csv", board)
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    netlist_routes = find_routes(chips_dict, netlist)
    create_grid(chips_dict, netlist_routes)

    create_output(netlist_routes, chip, net)

# arg1 = chip , arg2 = net 
main(sys.argv[1], sys.argv[2])
