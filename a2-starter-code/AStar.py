""" AStar.py

A* Search of a problem space.
Partnership? (YES or NO):YES
Student Name 1: Tatsuhiko Araki
Student Name 2: Chenliang Huang :student number: 2276084

UW NetID: taraki
My student number: 2276178
CSE 415, Autumn 2022, University of Washington

This code contains my implementation of the A* Search algorithm.

Usage:
python3 AStar.py FranceWithDXHeuristic
"""

import sys
import importlib
from PriorityQueue import My_Priority_Queue


class AStar:
    """
    Class that implements A* Search for any problem space (provided in the required format)
    """
    def __init__(self, problem):
        """ Initializing the AStar class.
        Please DO NOT modify this method. You may populate the required instance variables
        in the other methods you implement.
        """
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded.
        self.MAX_OPEN_LENGTH = None  # How long OPEN ever gets.
        self.PATH = None  # List of states from initial to goal, along lowest-cost path.
        self.PATH_LENGTH = None  # Number of states from initial to goal, along lowest-cost path.
        self.TOTAL_COST = None  # Sum of edge costs along the lowest-cost path.
        self.BACKLINKS = {}  # Predecessor links, used to recover the path.
        self.OPEN = None  # OPEN list
        self.CLOSED = None  # CLOSED list
        self.VERBOSE = True  # Set to True to see progress; but it slows the search.

        # The value g(s) represents the cost along the best path found so far
        # from the initial state to state s.
        self.g = {}  # We will use a hash table to associate g values with states.
        self.h = self.Problem.h# Heuristic function

        print("\nWelcome to A*.")

    def runAStar(self):
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.Astar(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def Astar(self,initial_state):
        self.CLOSED = []
        self.BACKLINKS[initial_state] = None
        # The "Step" comments below help relate UCS's implementation to
        # those of Depth-First Search and Breadth-First Search.

        # STEP 1a. Put the start state on a priority queue called OPEN
        self.OPEN = My_Priority_Queue()
        self.CLOSED = My_Priority_Queue()
        self.OPEN.insert(initial_state, 0)
        # STEP 1b. Assign g=0 to the start state.
        self.g[initial_state] = 0.0
        # STEP 2. If OPEN is empty, output “DONE” and stop.
        while len(self.OPEN) > 0:
            if self.VERBOSE:
                report(self.OPEN, self.CLOSED, self.COUNT)
            if len(self.OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(self.OPEN)
            (S, P) = self.OPEN.delete_min()
            # print("In Step 3, returned from OPEN.delete_min with results (S,P)= ", (str(S), P))
            self.CLOSED.insert(S,P)
            if self.Problem.GOAL_TEST(S):
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f'Length of solution path found: {self.PATH_LENGTH} edges')
                self.TOTAL_COST = self.g[S]
                print(f'Total cost of solution path found: {self.TOTAL_COST}')
                return
            self.COUNT += 1
            gs = self.g[S]
 
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    edge_cost = S.edge_distance(new_state)
                    new_g = gs + edge_cost
                    fs=new_g+self.h(new_state)
        

                    if new_state in self.CLOSED:
                        if fs >= self.CLOSED[new_state]:
                            del new_state
                            continue
                        elif fs < self.CLOSED[new_state]:
                            del self.CLOSED[new_state]
                            self.OPEN.insert(new_state,fs)
                        

                    elif new_state in self.OPEN:
                        if fs >= self.OPEN[new_state]:
                            del new_state
                            continue
                        elif fs < self.OPEN[new_state]:
                            del self.OPEN[new_state]
                            self.OPEN.insert(new_state,fs)
                    else:
                        self.OPEN.insert(new_state, fs)
                    self.BACKLINKS[new_state] = S
                    self.g[new_state] = new_g
        # print_state_queue("OPEN", OPEN)
        # STEP 6. Go to Step 2.
        return None

    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path


def print_state_queue(name, q):
    """
    Prints the states in queue q
    """
    print(f"{name} is now: ", end='')
    print(str(q))


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")    


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "FranceWithDXHeuristic"
    else:
        Problem = sys.argv[1]
    aStar = AStar(Problem)
    aStar.runAStar()
