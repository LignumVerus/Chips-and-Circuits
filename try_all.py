"""
* try_all.py
* Runs all the netlists, and tests all the combi's for wind up and down and creates an output file with the costs
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import csv

from main import main

def try_all():
    """
    Runs all netlists for each combination of experimental values.
    """

    # try different variable values
    wind = [0,1,2,3,4]
    up = [0,1,2,3,4]
    down = [0,1,2,3,4]
    options = [3, 5, 10, 15]
    len_choices = [10, 50, 100]
    shuffles = [1, 5, 10]

    # define the netlists that should be run
    netlists = [1,2,3,4,5,6,7,8,9]

    # define if the grid should be drawn
    draw = False

    # create headers
    headers = [0,1,2,3,4,5,6,7,8,9]

    # open output file to overwrite
    with open(f"gates&netlists/optimize/output.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(headers)

        # try all combinations of variable values
        for w in wind:
            for u in up:
                for d in down:
                    for o in options:
                        for ln in len_choices:
                            for s in shuffles:
                                row = []
                                row.append(f"{w}, {u}, {d}, {o}, {ln}, {s}")

                                # go over each netlist
                                for x in netlists:
                                    # append the results
                                    if x < 4:
                                        row.append(main(0, x, w, u, d, draw, o, ln, s))

                                    elif x < 7:
                                        row.append(main(1, x, w, u, d, draw, o, ln, s))

                                    else:
                                        row.append(main(2, x, w, u, d, draw, o, ln, s))

                                writer.writerow(row)    

# run
try_all()
