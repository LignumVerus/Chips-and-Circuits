# main.py
# Draws circuits on grid based on CSV file

import csv
import matplotlib.pyplot as plt
import numpy as np

# read csv  print_0 and create chips
def read_csv(filename):
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        chip_list = []

        for row in csvreader:
            # creates chip with id, x coordinate and y coordinate
            chip = Chip(row[0], row[1], row[2])

            chip_list.append(chip)
        
        create_grid(chip_list)


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

    plt.xlim([min(x_list) - 1, max(x_list) + 1])
    plt.ylim([min(y_list) - 1, max(y_list) + 1])
    plt.grid(visible=True, zorder=0)
    plt.title('Circuit Board Grid')
    plt.tight_layout()
    plt.savefig("plots/plot1.png")

# chip class that has a function that
class Chip:
    def __init__(self, id, x, y):
        self.id = id
        self.x = int(x)
        self.y = int(y)

read_csv("gates&netlists/chip_0/print_0.csv")