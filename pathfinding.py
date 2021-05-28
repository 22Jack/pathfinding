from warnings import warn
import heapq
import json

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement=False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = (len(maze[0]) * len(maze) // 2)

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

            # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if
                    child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None

def maze_():
    file = open("maze.json", "r")
    data = json.load(file)
    maze = data["maze"]
    file.close()
    return maze

def start():
    file = open("maze.json", "r")
    data = json.load(file)
    start1 = data["start"]
    start=(start1[1], start1[0])
    file.close()
    return start

def end():
    file = open("maze.json", "r")
    data = json.load(file)
    end1 = data["end"]
    end=(end1[1], end1[0])
    file.close()
    return end

def facing():
    file = open("maze.json", "r")
    data = json.load(file)
    facing = data["facing"]
    file.close()
    return facing

def printPath(path):
    maze=maze_()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if [y, x] == path[0]:
                print("O", end="")
            elif [y, x] == path[-1]:
                print("X", end="")
            elif [y, x] in path:
                print(".", end="")
            elif maze[y][x]==0:
                print(" ", end="")
            elif maze[y][x]==1:
                print("#", end="")
        print()

def pathEncoder(path):
    e=""
    for i in range(len(path)-1):
        deltaY=path[i][0]-path[i+1][0]
        deltaX=path[i][1]-path[i+1][1]
        if deltaY==1: e+="U"
        elif deltaY==-1: e+="D"
        elif deltaX==1: e+="L"
        else: e+="R"
    encodedPath="F"

    for i in range(len(path)-2):
        if e[i]==e[i+1]: encodedPath+="F"
        elif (e[i], e[i+1]) in (("U", "R"), ("R", "D"), ("D", "L"), ("L", "U")):
            encodedPath+="RF"
        elif (e[i], e[i+1]) in (("U", "L"), ("L", "D"), ("D", "R"), ("R", "U")):
            encodedPath+="LF"
    return encodedPath


def mainPathfinding():
    path=astar(maze_(), start(), end())
    encodedPath = pathEncoder(path)
    file = open("maze.json", "r")
    data = json.load(file)
    file.close()

    data["encodedPath"]=encodedPath
    data["path"]=path
    file = open("maze.json", "w")
    json.dump(data, file)
    file.close()

    #print(path)
    #print(encodedPath)
    #printPath(path)
