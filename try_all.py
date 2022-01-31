import csv

from main import main

def try_all():

    wind = [0,1,2,3,4]
    up = [0,1,2,3,4]
    down = [0,1,2,3,4]
    options = [3, 5, 10, 15]
    len_choices = [10, 50, 100]
    shuffels = [1, 5, 10]

    netlist = [1,2,3,4,5,6,7,8,9]
    draw = False

    headers = [0,1,2,3,4,5,6,7,8,9]

    with open(f"gates&netlists/optimize/output.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(headers)


        for w in wind:
            for u in up:
                for d in down:
                    for o in options:
                        for ln in len_choices:
                            for s in shuffels:
                                row = []
                                row.append(f"{w}, {u}, {d}, {o}, {ln}, {s}")

                                for x in netlist:

                                    if x < 4:
                                        row.append(main(0, x, w, u, d, o, ln, s, draw))
                                    
                                    elif x < 7:
                                        row.append(main(1, x, w, u, d, o, ln, s, draw))
                                    
                                    else:
                                        row.append(main(2, x, w, u, d, o, ln, s, draw))
                                
                                
                                writer.writerow(row)
                            

        print(x)
    
            

try_all() 
