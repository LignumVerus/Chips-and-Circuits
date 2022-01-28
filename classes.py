"""
* classes.py
* Creates classes used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""

# chip class that has a function that
class Chip:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)


class Line:
    def __init__(self, id, chip_start, chip_end, route):
        self.id = id
        self.start = chip_start
        self.end = chip_end
        self.route = route

    def __str__(self):
        pass
        # eerst lijst van alle tuples als string, loopen over route en toevoegen aan lijst met str ervoor
        list_tuples = []
        for tuple in self.route:
            list_tuples.append(str(tuple))
        # lijst returnen als string
        list_tuples = str(list_tuples)
        # list_tuples = [x.strip("") for x in list_tuples]
        # strippen van spaties
        print(list_tuples.strip(""))
        return list_tuples.strip("")
        # return list.strip , zodat die alle spaties eruit haalt
        


class Board:
    def __init__(self, lines):
        self.lines = lines
    
