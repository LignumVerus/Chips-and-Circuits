"""
* classes.py
* Creates classes used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""

class Line:
    """
    Creates line class.
    """
    def __init__(self, id, chip_start, chip_end, route):
        self.id = id
        self.start = chip_start
        self.end = chip_end
        self.route = route

    def __str__(self):
        # remove the spaces betweeen the elements from the output
        list_tuples = []
        for item in self.route:
            list_tuples.append(item)

        return str(list_tuples).replace(" ","")
        

class Board:
    """
    Creates board class that stores all non-chip route coordinates.
    """
    def __init__(self, lines):
        self.lines = lines
    
    def remove_route(self, line):
        """
        Removes a route from the board.
        """
        for coordinate in line.route[1:-1]:
            self.lines.remove(coordinate)
