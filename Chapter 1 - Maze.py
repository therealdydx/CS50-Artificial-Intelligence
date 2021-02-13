# this script is for analyzing purposes, not personally written 

# the sys module provides information about constants, functions and methods
import sys

# define a class called Node, this class has three variables
class Node():
    
    def __init__(self, state, parent, action):
       
       self.state = state
       self.parent = parent
       self.action = action
    
# define a class called StackFrontier, representing the frontier in a depth first approach
class StackFrontier():
    
    # create a frontier that is empty, create empty list
    def __init__(self):
        self.frontier = []
    
    # stack the node onto the stack
    def add(self, node):
        self.frontier.append(node)
        
    # check if the frontier contains a particular state
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    # check if the frontier is empty, 0 length means no solutions
    def empty(self):
        return len(self.frontier) == 0
        
    # if frontier isn't empty, then we should remove the last node in the frontier for checking, and return node
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
            
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# define a class called QueueFrontier, representing the frontier in a breadth first approach
class QueueFrontier(StackFrontier):

    # if frontier isn't empty, then we should remove the first node in the frontier for checking, and return node
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
            
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):

        # read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # validate start and goal, there must be only 1 start point
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")

        # in the case of this maze, there should be 1 end goal, or B
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # determine height and width of the maze, splitlines splits strings into a list, where the line breaks are
        contents = contents.splitlines()
        self.height = len(contents) # number of lines
        self.width = max(len(line) for line in contents) # maximum length of a line

        # keep track of walls
        self.walls = []

        # start iterating through heights
        for i in range(self.height):
            row = []
            
            # start iterating through width
            for j in range(self.width):

                try:
                    # if you have found the start point
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)

                    # if you have found the end point
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)

                    elif contents[i][j] == " ":
                        row.append(False)

                    else:
                        row.append(True)

                except IndexError:
                    row.append(False)
            
            self.walls.append(row)

        self.solution = None
        

# ..................................... more code in the middle ..................................

    def solve(self):

        # Finds a solution to maze, if one exists

        # keep track of number of states explored
        self.num_explored = 0

        # initialize frontier to the starting position
        start = Node(state = self.start, parents = None, action = None)
        frontier = StackFrontier() # start with stack frontier, depth first search
        frontier.add(start) # this frontier just contains the start set

        # initialize an empty explored set
        self.explored = set()

        # keep looping until solution found
        while True:

            # if nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution") # no solution to this problem

            # choose a node from the frontier
            node = frontier.remove() # remove a node from the frontier
            self.num_explored += 1 # update number of states that we have explored

            # if node is the goal, then we have a solution
            if node.state == self.goal: 
                actions = []
                cells = []

                # want to backtrack way to find solution. every node contains the parent and the action.

                # thus, create a loop, constantly looking at parents of each node, and the action to get to the parent
                while node.parent is not None: # none signifies initial node

                    actions.append(node.action) # include the action taken to get there
                    cells.append(node.state) # include the current state of the node
                    node = node.parents # now traverse up one stage to the parent so that we can check the parents' parents
                
                actions.reverse() # to find the initial state downwards
                cells.reverse() # to find the states down
                self.solution = (actions, cells)
                return

            # if it is not the goal, then mark it into the explored, so that we don't have to explore it anymore
            self.explored.add(node.state)

            # add neighbours to the frontier
            for action, state in self.neighbors(node.state):
                
                # checking, is the state already in the frontier, and is the state in the explored set
                if not frontier.contains_state(state) and state not in self.explored:
                    
                    # if not in either set, then add neighbour node into the frontier
                    child = Node(state = state, parent = node, action = action)
                    frontier.add(child)



# ....................more code in the middle......................

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze: ")
m.print()
print("Solving..."
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored = True)