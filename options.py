
from helper import *

def valid_directions(
    current_coordinate, invalid_chip_coords, route, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board
):
    """
    finds all possible directions from point in grid

    returns list with tuples. first item is possible next coordinate, second is extra cost for that direction
    """
    choices = []

    # west
    if (
        # can't go out of board
        current_coordinate[0] - 1 >= min_x
        # can't go over another chip
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        # can't collide with another line
        and is_not_collision((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]), board)
        # can't collide with own route
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2]), wind))

    # east
    if (
        current_coordinate[0] + 1 <= max_x
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), board)
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2]), wind))

    # north
    if (
        current_coordinate[1] - 1 >= min_y
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2]), wind))

    # south
    if (
        current_coordinate[1] + 1 <= max_y
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), board)
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2]), wind))

    # down
    if (
        current_coordinate[2] - 1 >= min_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1), down))

    # up
    if (
        current_coordinate[2] + 1 <= max_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in invalid_chip_coords
        and is_not_collision((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), board)
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1) not in route
    ):
        choices.append(((current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1), up))
        
    return choices
