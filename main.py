# main.py
# Draws circuits on grid based on CSV file

import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import sys

# read csv  print_0 and create chips
def read_csv_chips(filename):
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        chip_list = []
        
        # creates chips with id, x coordinate and y coordinate
        for row in csvreader:
            chip = Chip(row[0], row[1], row[2])

            chip_list.append(chip)
    return chip_list

def read_csv_netlist(filename):
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        netlist = []

        for number, row in enumerate(csvreader):
            try:
                line = Line(number, row[0], row[1],[])

                netlist.append(line)
            except IndexError:
                pass

    return netlist


# Needs to return list of Line
def find_routes(chip_list, netlist):
    route1 = [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5)]
    route2 = [(1,5),(1,4),(2,4),(3,4), (4,4)]

    netlist[0].route = route1
    netlist[1].route = route2
    return netlist

    # find_route(x_start, y_start x_end, y_end)
    # pass

# def find_route(x_start, y_start x_end, y_end):
#     pass

# visualize grid
def create_grid(chip_list, netlist_routes):
    id_list = []
    x_list = []
    y_list = []
    
    for chip in chip_list:
        id_list.append(chip.id)
        x_list.append(chip.x)
        y_list.append(chip.y)

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
        plt.annotate(txt, (x_list[i], y_list[i]), ha='center', va='center')

    plt.xlim([min(x_list) - 1, max(x_list) + 2])
    plt.ylim([min(y_list) - 1, max(y_list) + 2])
    plt.grid(visible=True, zorder=0)
    plt.title('Circuit Board Grid')
    plt.tight_layout()
    plt.savefig("plots/plot1.png")

# compute costs
def costs(netlist):
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

    # counts = Counter(route_coords)
    k = sum(value - 1 for value in counts.values())
    
    return n + 300 * k

def create_output(netlist_routes,chip, net):
    with open('gates&netlists/chip_0/output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["net","wires"])

        for line in netlist_routes:
            newrow= (int(line.start), int(line.end))
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

def main(chip, net):
    chip_list = read_csv_chips(f"gates&netlists/chip_{chip}/print_0.csv")
    netlist = read_csv_netlist(f"gates&netlists/chip_{chip}/netlist_{net}.csv")
    netlist_routes = find_routes(chip_list, netlist)
    create_grid(chip_list, netlist_routes)
    
    create_output(netlist_routes, chip, net)

main(sys.argv[1], sys.argv[2])
