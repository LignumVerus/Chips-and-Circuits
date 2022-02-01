"""
* output.py
* Creates output functions used in main.py
* 
* Viola Koers 12213101
* Finn Peranovic 12740454
* Rachel de Haan 12423254
"""
import matplotlib.pyplot as plt
import csv

from code.helper import costs


def create_grid(chips_dict, netlist_routes, chip, net):
    """
    Visualizes a 3D grid with the chips and the netlist routes.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    # Prepare chips for drawing
    id_list = chips_dict.keys()
    x_list = []
    y_list = []
    z_list = []

    for coordinate in chips_dict.values():
        x_list.append(coordinate[0])
        y_list.append(coordinate[1])
        z_list.append(coordinate[2])

    # Prepare routes for drawing
    for lines in netlist_routes:
        x_lines = []
        y_lines = []
        z_lines = []

        for line in lines.route:
            x_lines.append(line[0])
            y_lines.append(line[1])
            z_lines.append(line[2])

        # Draw the routes
        ax.plot(x_lines, y_lines, z_lines, linewidth=2.5)

    # Draw the chips
    ax.scatter(x_list, y_list, z_list, zorder=2, s=300)

    for i, txt in enumerate(id_list):
        ax.annotate(txt, (x_list[i], y_list[i]), ha="center", va="center")

    plt.xlim([min(x_list) - 1, max(x_list) + 1])
    plt.ylim([min(y_list) - 1, max(y_list) + 1])
    ax.set_zticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax.grid(visible=True, zorder=0)
    plt.title("Circuit Board Grid")
    plt.tight_layout()
    plt.savefig(f"output/plots/chip_{chip}_net{net}.png")


def create_output(netlist_routes, chip, net, board):
    """
    Writes output to CSV file.
    """
    with open(f"output/chip_{chip}/net_{net}/output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["net", "wires"])

        for line in netlist_routes:
            newrow = (int(line.start), int(line.end))
            writer.writerow([str(newrow).replace(" ",""), line])

        cost = costs(board, netlist_routes)
        writer.writerow([f"chip_{chip}_net_{net}", int(cost)])

    # TODO remove return
    return cost
