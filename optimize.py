
from algorithm import *
from helper import *

# board wordt niet geupdate dus probeerd ook omzichzelf heen te leggen

def optimize(line, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, board, overlap):
 # optimized_routes = 0
    wind = 0
    up = 0
    down = 0

    current_route = line.route

    # # maak bord leger
    for coordinate in line.route[1:-1]:
        board.lines.remove(coordinate)    

    better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)
    
    while len(better) < len(current_route):
        current_route = better
        better = optimize_route(current_route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)

    # voeg weer toe aan bord
    board.lines.extend(current_route[1:-1])
    line.route = current_route

    # return line.route

def optimize_route(route, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap):
    
    for i, point_one in enumerate(route):
        for j, point_two in reversed(list(enumerate(route[i:]))):
            distance = manhattan_distance(point_one, point_two)
            route_distance = j - i

            if distance > 1 and route_distance > distance:
                pos_new_route = find_random_route(point_one, point_two, chips_dict, min_x, max_x, min_y, max_y, min_z, max_z, wind, up, down, board, overlap)

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
