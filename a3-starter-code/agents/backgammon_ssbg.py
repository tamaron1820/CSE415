'''
Name(s):Tatsuhiko Araki and Ching Zheng Ing
UW netid(s): taraki and zi2b
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxPly = 1
        self.special_static_eval = None
        # feel free to create more instance variables as needed.

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "taraki(ssbg)"

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. Count the chance nodes
    # as a ply too!
    def setMaxPly(self, maxply=2):
        self.maxPly = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        self.special_static_eval = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1, die2):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        return self.expectiminimax(state, self.maxPly, die1, die2)[1]

    def expectiminimax(self, state, plyLeft, die1, die2):
        whoseMove = state.whose_move
        if plyLeft == 0:
            if self.special_static_eval != None:
                return (self.special_static_eval(state),"")
            else:
                return (self.staticEval(state),"")
        provisional = (0,"")
        if whoseMove == 0: #Max player, white
            provisional = (-100000,"")
        else:
            provisional = (100000,"")
        
        for next_move, next_state in self.get_all_moves_state_pair(state, die1, die2):
            value = 0
            for die_1 in range(6):
                for die_2 in range(6):
                    newVal = self.expectiminimax(next_state, plyLeft-1, die_1, die_2)
                    value += newVal[0] / 36
            
            if (whoseMove == 0) and value > provisional[0]:
                provisional = (value, next_move)
            elif (whoseMove ==1) and value < provisional[0]:
                provisional = (value, next_move)
        return provisional

    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        count_list_White=[]
        count_list_Red=[]
        for i in range(len(state.pointLists)):
            White_count = 0
            Red_count = 0
            White_home_count=0
            Red_home_count=0
            for j in range(len(state.pointLists[i])):    
                if state.pointLists[i][j]==0:
                    White_count+=1
                    if i<=5 and i>=0:
                        White_home_count+=1
                elif state.pointLists[i][j]==1:
                    Red_count+=1
                    if i>=18 and i<=23:
                        Red_home_count+=1
            count_list_White.append(White_count)
            count_list_Red.append(Red_count)
        #Initialize counts
        count_pip_Red = 0
        count_pip_White = 0
        for i in range(len(count_list_White)):
            count_pip_White+=count_list_White[i]*(len(count_list_White) -i)
        for i in range(len(count_list_Red)):
            count_pip_Red+=count_list_Red[i]*(i+1) 
        #pip_count 
        pip_differnce = count_pip_Red - count_pip_White
        R_bar=state.bar.count(1)
        W_bar=state.bar.count(0)
        #hit
        bar_difference=R_bar-W_bar
        #home count
        home_count_difference=White_home_count-Red_home_count
        White_out_board=state.white_off
        Red_out_board=state.red_off
        #bear off
        out_board_difference=len(White_out_board)-len(Red_out_board)
        Evaluation_count=pip_differnce+80*bar_difference+20*home_count_difference+90*out_board_difference
        return Evaluation_count

            

    def get_all_moves_state_pair(self, curr_state, die1, die2):
        """Uses the mover to generate all legal (moves,state) pairs."""
        #generate move for curr_state
        move_generator = self.GenMoveInstance.gen_moves(curr_state, curr_state.whose_move, die1, die2)
        move_state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(move_generator)    # Gets a (move, state) pair.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_state_list.append(m)    # Add the (move, state) to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:#if only can p
            move_state_list.append(('p', curr_state))
        return move_state_list