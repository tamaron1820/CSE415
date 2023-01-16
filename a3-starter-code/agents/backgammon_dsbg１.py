'''
Name(s):
UW netid(s):
'''

from sre_parse import State
from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.AlphaBeta = False
        self.maxPly = 1
        self.cutoff=0
        # feel free to create more instance variables as needed.

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "taraki and zheng ing"

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        if prune==True:
            

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containig states and cutoff
        return (, self.cutoff)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        pass

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        pass
    
    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        
        return self.move_minimax(state)

    def move_minimax(self, state):
        move_state_pairs = self.get_all_moves_state_pair(state)
        if len(move_state_pairs) ==0:
            return "NO MOVES COULD BE FOUND"
        else:
            return self.minimax(state,plyLeft=1)[1]
        
    def minimax(self, state, plyLeft):
        whoseMove = state.whose_move
        if plyLeft == 0:
            return (self.staticEval(state),"")
        provisional = (0,"")
        if whoseMove == 0: #Max player, white
            provisional = (-100000,"")
        else:
            provisional = (100000,"")
        for next_move, next_state in self.get_all_moves_state_pair(state):
            newVal = self.minimax(next_state, next_state.whose_move, plyLeft=-1)
            if (whoseMove == 0) and newVal[0] > provisional[0]:
                provisional = (newVal[0], next_move)
            elif (whoseMove ==1) and newVal[0] < provisional[0]:
                provisional = (newVal[0], next_move)
        return provisional
        
    def alphaBeta(self, state, alpha,beta,plyLeft):
        whoseMove = state.whose_move
        if plyLeft == 0:
            return (self.staticEval(state),"")
        provisional = (0,"")
        if whoseMove == 0: #Max player, white
            provisional = (-100000,"")
        else:
            provisional = (100000,"")
        for next_move, next_state in self.get_all_moves_state_pair(state):
            newVal = self.alphaBeta(next_state, next_state.whose_move, alpha,beta,plyLeft=-1)
            if (whoseMove == 0) :
                provisional=(max(newVal[0],provisional[0]),next_move)
                alpha=max(alpha,provisional[0])
                if beta<=alpha:
                    self.cutoff+=1
                    break
            elif (whoseMove ==1): 
                provisional=(min(newVal[0],provisional[0]),next_move)
                beta=min(beta,provisional[0])
                if beta<=alpha:
                    self.cutoff+=1
                    break
        return provisional

    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        count_list_White=[]
        count_list_Red=[]
        for i in range(len(state.pointLists)):
            White_count = 0
            Red_count = 0
            for j in range(len(i)):    
                if state.pointLists[i][j]=="W":
                    White_count+=1
                elif state.pointLists[i][j]=="R":
                    Red_count+=1
            count_list_White[i] = White_count
            count_list_Red[i] = Red_count
        #Initialize counts
        count_pip_Red = 0
        count_pip_White = 0
        for i in range(len(count_list_White)):
            count_pip_White+=count_list_White[i]*(len(count_list_White) -i)

        for i in range(len(count_list_Red)):
            count_pip_Red+=count_list_Red[i]*(i+1)
        pip_differnce = count_pip_Red - count_pip_White
        return pip_differnce 

    def get_all_moves_state_pair(self, curr_state):
        """Uses the mover to generate all legal (moves,state) pairs."""
        move_state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_state_list.append(m)    # Add the (move, state) to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:#if only can p
            move_state_list.append(('p', curr_state))
        return move_state_list