"""
* options.py
* Returns the valid directions (choices) from a current point 
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
from code.helper import is_not_collision


def valid_directions(
    current_coordinate,
    invalid_chip_coords,
    route,
    board_size,
    wind,
    up,
    down,
    board,
    overlap,
):
    """
    Finds all possible directions from point in grid.
    Returns list with tuples. First item is possible next coordinate, second is extra cost for that direction.
    """
    choices = []

    min_x = board_size[0]
    max_x = board_size[1]
    min_y = board_size[2]
    max_y = board_size[3]
    min_z = board_size[4]
    max_z = board_size[5]

    # west
    if (
        # cannot go out of board
        current_coordinate[0] - 1 >= min_x
        # cannot go over another chip
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        # cannot collide with another line
        and (
            is_not_collision(
                (
                    current_coordinate[0] - 1,
                    current_coordinate[1],
                    current_coordinate[2],
                ),
                board,
            )
            or overlap
        )
        # cannot collide with own route
        and (current_coordinate[0] - 1, current_coordinate[1], current_coordinate[2])
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0] - 1,
                    current_coordinate[1],
                    current_coordinate[2],
                ),
                wind,
            )
        )

    # east
    if (
        current_coordinate[0] + 1 <= max_x
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in invalid_chip_coords
        and (
            is_not_collision(
                (
                    current_coordinate[0] + 1,
                    current_coordinate[1],
                    current_coordinate[2],
                ),
                board,
            )
            or overlap
        )
        and (current_coordinate[0] + 1, current_coordinate[1], current_coordinate[2])
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0] + 1,
                    current_coordinate[1],
                    current_coordinate[2],
                ),
                wind,
            )
        )

    # north
    if (
        current_coordinate[1] - 1 >= min_y
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in invalid_chip_coords
        and (
            is_not_collision(
                (
                    current_coordinate[0],
                    current_coordinate[1] - 1,
                    current_coordinate[2],
                ),
                board,
            )
            or overlap
        )
        and (current_coordinate[0], current_coordinate[1] - 1, current_coordinate[2])
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0],
                    current_coordinate[1] - 1,
                    current_coordinate[2],
                ),
                wind,
            )
        )

    # south
    if (
        current_coordinate[1] + 1 <= max_y
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in invalid_chip_coords
        and (
            is_not_collision(
                (
                    current_coordinate[0],
                    current_coordinate[1] + 1,
                    current_coordinate[2],
                ),
                board,
            )
            or overlap
        )
        and (current_coordinate[0], current_coordinate[1] + 1, current_coordinate[2])
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0],
                    current_coordinate[1] + 1,
                    current_coordinate[2],
                ),
                wind,
            )
        )

    # down
    if (
        current_coordinate[2] - 1 >= min_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in invalid_chip_coords
        and (
            is_not_collision(
                (
                    current_coordinate[0],
                    current_coordinate[1],
                    current_coordinate[2] - 1,
                ),
                board,
            )
            or overlap
        )
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] - 1)
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0],
                    current_coordinate[1],
                    current_coordinate[2] - 1,
                ),
                down,
            )
        )

    # up
    if (
        current_coordinate[2] + 1 <= max_z
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in invalid_chip_coords
        and (
            is_not_collision(
                (
                    current_coordinate[0],
                    current_coordinate[1],
                    current_coordinate[2] + 1,
                ),
                board,
            )
            or overlap
        )
        and (current_coordinate[0], current_coordinate[1], current_coordinate[2] + 1)
        not in route
    ):
        choices.append(
            (
                (
                    current_coordinate[0],
                    current_coordinate[1],
                    current_coordinate[2] + 1,
                ),
                up,
            )
        )

    return choices
