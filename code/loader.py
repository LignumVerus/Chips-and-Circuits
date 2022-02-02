"""
* loader.py
* Loads CSV files used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import csv

from code.classes import Line


def read_csv_chips(filename):
    """
    Reads CSV file print_0 and creates chips.
    """
    with open(filename) as file:
        csvreader = csv.reader(file)
        next(csvreader)

        chips_dict = {}

        # make a dictionary of all the chips, with the id as the key and tuple of coordinates as value
        for row in csvreader:
            chips_dict[row[0]] = (int(row[1]), int(row[2]), int(0))

    return chips_dict


def read_csv_netlist(filename):
    """
    Reads CSV file containing the netlist.
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
