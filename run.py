"""
* run.py
* Runs the code with the terminal entered user's input 
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import sys

from main import main

# TODO: COMMENTS
def input_wind():
    try:
        wind = int(input("Enter heuristic for directions North, East, South, West (2 recommended): ").strip())
        return wind
    except ValueError:
        input_wind()


def input_up():
    try:
        up = int(input("Enter heuristic for direction Up (0 recommended): ").strip())
        return up
    except ValueError:
        input_up()


def input_down():
    try:
        down = int(input("Enter heuristic for direction Down (1 recommended): ").strip())
        return down
    except ValueError:
        input_down()


def input_draw():
    try:
        draw = input("Do you want to create a visualization? (Y/N) (Y recommended): ").strip().lower()

        if draw == "y" :
            draw = True
        else:
            draw = False

        return draw
    except ValueError:
        input_draw()


def input_options():
    try:
        options = int(input("What do you want the random range of heuristics for the hill climber to be? (3-15 recommended) From 0 to: ").strip())
        return draw
    except ValueError:
        input_options()


def input_len_choices():
    try:
        len_choices = int(input("What is the maximum number of combinations of these options you want to try? (10-50 recommended) ").strip())
        return len_choices
    except ValueError:
        input_len_choices()


def input_shuffles():
    try:
        shuffles = int(input("How many different shuffles of the netlist do you want to try for the hill climber? (1-5 recommended) ").strip())
        return shuffles
    except ValueError:
        input_shuffles()


# get user input
wind = input_wind()
up = input_up()
down = input_down()
draw = input_draw()
options = input_options()
len_choices = input_len_choices()
shuffles = input_shuffles()

# run main
print("Not found, cost: ", main(sys.argv[1], sys.argv[2], wind, up, down, True, options, len_choices, shuffles))
