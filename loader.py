"""
* loader.py
* Loads CSV files used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import csv

from classes import Chip, Line, Board

def read_csv_chips(filename, board):
    """
    reads csv  print_0 and create chips
    """

    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)

        chips_dict = {}

        # creates chips with id, x coordinate and y coordinate
        for row in csvreader:
            chip = Chip(row[0], row[1], row[2], 0)

            # add x and y coordinate to board
            board.add_chip(chip.x, chip.y, 0)

            # Make a dictionary of all the chips, with the id as the key and tuple of coordinates as value
            chips_dict[row[0]] = (chip.x, chip.y, 0)

    return chips_dict


def read_csv_netlist(filename):
    """
    reads cvc file with netlist
    """
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)
        netlist = []

        for number, row in enumerate(csvreader):
            try:
                line = Line(number, row[0], row[1], [])
                netlist.append(line)
            except IndexError:
                pass

    return netlist
