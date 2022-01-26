import csv

from main import main

def optimize():

    wind = [2]
    up = [0]
    down = [1]

    netlist = [1,2,3,4,5,6,7,8,9]
    draw = False

    data = []

    for x in netlist:

        row = []
        headers = []

        for w in wind:
            for u in up:
                for d in down:

                    headers.append(f"{w}, {u}, {d}")

                    if x < 4:
                        row.append(main(0, x, w, u, d, draw))
                    
                    elif x < 7:
                        row.append(main(1, x, w, u, d, draw))
                    
                    else:
                        row.append(main(2, x, w, u, d, draw))

        data.append(row)

        print(x)
    
    with open(f"gates&netlists/optimize/output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for line in data:
            writer.writerow(line)


optimize() 