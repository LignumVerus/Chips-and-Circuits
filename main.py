# main.py
# Draws circuits on grid based on CSV file

import csv
import matplotlib.pyplot as plt
import numpy as np

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
            line = Line(number, row[0], row[1],[])

            netlist.append(line)

    return netlist



# def find_routes(chip_list):
#     find_route(x_start, y_start x_end, y_end)
#     pass

# def find_route(x_start, y_start x_end, y_end):
#     pass

# visualize grid
def create_grid(chip_list):
    id_list = []
    x_list = []
    y_list = []
    
    for chip in chip_list:
        id_list.append(chip.id)
        x_list.append(chip.x)
        y_list.append(chip.y)

    # plot
    plt.scatter(x_list, y_list, zorder=2, s=300)
    for i, txt in enumerate(id_list):
        plt.annotate(txt, (x_list[i], y_list[i]), ha='center', va='center')

    plt.xlim([min(x_list) - 1, max(x_list) + 2])
    plt.ylim([min(y_list) - 1, max(y_list) + 2])
    plt.grid(visible=True, zorder=0)
    plt.title('Circuit Board Grid')
    plt.tight_layout()
    plt.savefig("gates&netlists/plots/plot1.png")

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

def main():
    chip_list = read_csv_chips("gates&netlists/chip_0/print_0.csv")
    netlist = read_csv_netlist("gates&netlists/chip_0/netlist_1.csv")
    # routes = find_routes()
    create_grid(chip_list)

main()
