"""
* run.py
* Runs the code with the terminal entered user's input 
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import sys

from code.main import main


def input_wind():
    """
    Asks user for wind input heuristic. Returns wind heurisic.
    """
    try:
        wind = int(input("Enter heuristic for directions North, East, South, West (2 recommended): ").strip())

        if wind < 0:
            print("Has to be 0 or higher")
            input_wind()
        
        return wind
    except ValueError:
        print("Has to be an interger")
        return input_wind()
        
    
def input_up():
    """
    Asks user for up input heuristic. Returns up heurisic.
    """
    try:
        up = int(input("Enter heuristic for direction Up (0 recommended): ").strip())

        if up < 0:
            print("Has to be 0 or higher")
            input_up()

        return up
    except ValueError:
        print("Has to be an interger")
        return input_up()


def input_down():
    """
    Asks user for down input heuristic. Returns down heurisic.
    """
    try:
        down = int(input("Enter heuristic for direction Down (1 recommended): ").strip())

        if down < 0:
            print("Has to be 0 or higher")
            input_down()
            
        return down
    except ValueError:
        print("Has to be an interger")
        return input_down()


def input_draw():
    """
    Asks user for draw input. Returns boolean whether a visualization should be created.
    """
    try:
        draw = input("Do you want to create a visualization? (Y/N) (Y recommended): ").strip().lower()

        if draw == "y" :
            draw = True
        elif draw == "n":
            draw = False
        else:
            print("Y or N?")
            input_draw()
            
        return draw
    except ValueError:
        return input_draw()


def input_options():
    """
    Asks user for range of input for hill climber input. Returns the maximum value.
    """
    try:
        options = int(input("What do you want the random range of heuristics for the hill climber to be? (3-15 recommended) From 0 to: ").strip())

        if options < 1:
            print("Has to be 1 or higher")
            input_options()

        return options

    except ValueError:
        print("Has to be an interger")
        return input_options()


def input_len_choices():
    """
    Asks user for the number of combinations they want to try. Returns this value.
    """
    try:
        len_choices = int(input("What is the maximum number of combinations of these options you want to try? (10-50 recommended) ").strip())
        
        if len_choices < 1:
            print("Has to be 1 or higher")
            input_len_choices()

        return len_choices

    except ValueError:
        print("Has to be an interger")
        return input_len_choices()


def input_shuffles():
    """
    Asks user for number of times they want to shuffle the order of the lines. Returns this value.
    """
    try:
        shuffles = int(input("How many different shuffles of the netlist do you want to try for the hill climber? (1-5 recommended) ").strip())
        if shuffles < 1:
            print("Has to be 1 or higher")
            input_shuffles()

        return shuffles

    except ValueError:
        print("Has to be an interger")
        return input_shuffles()


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
