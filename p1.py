from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """

    frontQueue = []
    heappush(frontQueue, (0, initial_position))
    came_from = dict()
    cost_so_far = dict()
    came_from[initial_position] = None
    cost_so_far[initial_position] = 0

    while len(frontQueue) > 0:
        p1, currentTile = heappop(frontQueue)

        if currentTile == destination:
            pathCells = []
            ct = currentTile
            while ct is not None:
                pathCells.append(ct)
                ct = came_from[ct]
            print('total cost =', cost_so_far[currentTile])
            print()
            return pathCells

        for neighbor in adj(graph, currentTile):
            new_cost = cost_so_far[currentTile] + neighbor[1]
            if neighbor[0] not in cost_so_far or new_cost < cost_so_far[neighbor[0]]:
                cost_so_far[neighbor[0]] = new_cost
                priority = new_cost
                heappush(frontQueue, (priority, neighbor[0]))
                came_from[neighbor[0]] = currentTile

    #in the case that it exits but no path is found
    return None




def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    #this code should be exactly the same is shortest path to one, with the exception that there is no destination.
    #because of so, we just keep going through the queue until no more remain, in which case the cost so far is found for every position.
    #we just then return cost so far.
    frontQueue = []
    heappush(frontQueue, (0, initial_position))
    came_from = dict()
    cost_so_far = dict()
    came_from[initial_position] = None
    cost_so_far[initial_position] = 0
    while len(frontQueue) > 0:
        p1, currentTile = heappop(frontQueue)

        for neighbor in adj(graph, currentTile):
            new_cost = cost_so_far[currentTile] + neighbor[1]
            if neighbor[0] not in cost_so_far or new_cost < cost_so_far[neighbor[0]]:
                cost_so_far[neighbor[0]] = new_cost
                priority = new_cost
                heappush(frontQueue, (priority, neighbor[0]))
                came_from[neighbor[0]] = currentTile

    #in the case that it exits but no path is found
    return cost_so_far


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    xSteps = [1, 0, -1]
    ySteps = [1, 0, -1]
    adjList = []
    for xStep in xSteps:
        for yStep in ySteps:
            neighbor = (cell[0] + xStep, cell[1] + yStep)
            distScalar = 0.5 if yStep == 0 or xStep == 0 else 0.5 * sqrt(2)
            if not (xStep == 0 and yStep == 0) and neighbor in level['spaces']:
                cellCost = level['spaces'][cell]
                neighborCost = level['spaces'][neighbor]

                adj = (neighbor, (cellCost + neighborCost) * distScalar)
                adjList.append(adj)

    # print(adjList)
    return adjList




def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!!!!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)
    # navigation_edges(level, (2, 10))

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a', 'e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
