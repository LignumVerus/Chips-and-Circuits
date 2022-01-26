
from algorithm import *
from helper import *

def optimize(netlist, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board):
 # optimized_routes = 0
    wind = 0
    up = 0
    down = 0

    # idee: doe dit while er nog een netlist verbeterd is 
    for line in netlist: 

        current_route = line.route

        better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)
        
        while len(better) < len(current_route):
            current_route = better
            better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)

        line.route = current_route
    
    return netlist

def optimize_route(route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board):
    for i, point_one in enumerate(route):
        # idee: laat punt 2 bij de laatste beginnen
        for j, point_two in enumerate(route[i:]):
            distance = manhattan_distance(point_one, point_two)
            route_distance = j - i

            if distance > 1 and route_distance > distance:
                pos_new_route = find_random_route(point_one, point_two, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board)

                new_route = pos_new_route[0]

                if len(new_route) < route_distance and len(new_route) > 0 and pos_new_route[1]:

                    if len(route[:i]) > 0 and len(route[j:]) > 0: 
                        temp = route[:i]

                        temp.extend(new_route)
                        temp.extend(route[j + 1:])

                        route = temp
                    
                    elif len(route[:i]) > 0:
                        temp = route[:i]

                        temp.extend(new_route)

                        route = temp
                    
                    elif len(route[j:]) > 0:
                        temp = route[j + 1:]
                        
                        new_route.extend(temp)

                        route = new_route
                    
                    else:
                        route = new_route
                    
                    return route
    
    return route
