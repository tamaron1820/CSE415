'''Farmer_Fox.py
by Tatsuhiko Araki
UWNetID: taraki
Student number: 2276178

Assignment 2, in CSE 415, Autumn 2022.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

# replace this.
'''HumansRobotsFerry.py
("Humans, Robots and Ferry" problem)
'''
#<METADATA>
from re import T


SOLUTION_VERSION = "2.0"
PROBLEM_NAME = "Farmer-fox problem"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Tatsuhiko Araki']
PROBLEM_CREATION_DATE = "11-Oct-2022"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC=\
 '''The <b>"Humans, Robots and Ferry"</b> problem is a variation of
the classic puzzle "Missionaries and Cannibals." In the Humans, Robots
and Ferry problem, the player starts off with three humans and three
robots on the left bank of a creek.  The object is to execute a
sequence of legal moves that transfers them all to the right bank of
the creek.  In this puzzle, there is a ferry that can carry at most
three agents (humans, robots), and one of them must be a human to steer
the ferry.  It is forbidden to ever have one or two humans outnumbered
by robots, either on the left bank, right bank, or on the ferry.
In the formulation presented here, the computer will not let you make a
move to such a forbidden situation, and it will only show you moves
that could be executed "safely."
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
F=0  # array index to access human counts
f=1  # same idea for robots
c=2
g=3
LEFT=0 # same idea for left side of creek
RIGHT=1 # etc.

class State():

  def __init__(self, d=None):
    if d==None: 
      d = {'agents':[[0,0,0,0],[0,0,0,0]],
      'ferry':LEFT}
    self.d = d

  def __eq__(self,s2):
    for prop in ['agents','ferry']:
      if self.d[prop] != s2.d[prop]: return False
    return True

  def __str__(self):
    # Produces a textual description of a state.
    p = self.d['agents']
    txt = "\n F on left:"+str(p[LEFT][F])+"\n"
    txt += " f on left:"+str(p[LEFT][f])+"\n"
    txt += " c on left:"+str(p[LEFT][c])+"\n"
    txt += " g on left:"+str(p[LEFT][g])+"\n"
    txt += "   F on right:"+str(p[RIGHT][F])+"\n"
    txt += "   f on right:"+str(p[RIGHT][f])+"\n"
    txt += "   c on right:"+str(p[RIGHT][c])+"\n"
    txt += "   g on right:"+str(p[RIGHT][g])+"\n"
    side='left'
    if self.d['ferry']==1: side='right'
    txt += " ferry is on the "+side+".\n"
    return txt

  def __hash__(self):
    return (self.__str__()).__hash__()

  def copy(self):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = State({})
    news.d['agents']=[self.d['agents'][left_or_right][:] for left_or_right in [LEFT,RIGHT]]
    news.d['ferry'] = self.d['ferry']
    return news

  def can_move(self,Fa,fo,ch,gr):
    '''Tests whether it's legal to move the ferry and take
     h humans and r robots.'''
    side = self.d['ferry'] # Where the ferry is.
    p = self.d['agents']
    if Fa<1: return False # Need an H to steer boat.
    F_available = p[side][F]
    if F_available < Fa: return False
    f_available = p[side][f]
    if f_available < fo: return False # Can't take more h's than available
    c_available = p[side][c]
    if c_available < ch: return False
    g_available = p[side][g]
    if g_available < gr: return False
    f_remaining = f_available - fo
    c_remaining = c_available - ch
    g_remaining = g_available - gr
    if f_remaining==1 and c_remaining==1:
      return False
    if c_remaining==1 and g_remaining==1:
      return False
    return True
    
  def move(self,Fa,fo,ch,gr):
    '''Assuming it's legal to make the move, this computes
     the new state resulting from moving the ferry carrying
     h humans and r robots.'''
    news = self.copy()      # start with a deep copy.
    side = self.d['ferry']        # where is the ferry?
    p = news.d['agents']          # get the array of arrays of agents.
    p[side][F] = p[side][F]-Fa     # Remove agents from the current side.
    p[side][f] = p[side][f]-fo
    p[side][c] = p[side][c]-ch     # Remove agents from the current side.
    p[side][g] = p[side][g]-gr

    p[1-side][F] = p[1-side][F]+Fa # Add them at the other side.
    p[1-side][f] = p[1-side][f]+fo
    p[1-side][c] = p[1-side][c]+ch
    p[1-side][g] = p[1-side][g]+gr
    news.d['ferry'] = 1-side      # Move the ferry itself.
    return news

def goal_test(s):
  '''If all Ms and Cs are on the right, then s is a goal state.'''
  p = s.d['agents']
  return (p[RIGHT][F]==1 and p[RIGHT][f]==1 and p[RIGHT][c]==1 and p[RIGHT][g]==1)

def goal_message(s):
  return "Congratulations on successfully guiding the humans and robots across the creek!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda : State(d={'agents':[[1,1,1,1],[0,0,0,0]] ,'ferry':LEFT })
#</INITIAL_STATE>

#<OPERATORS>
Ffcg_combinations = [(1,0,0,0),(1,0,1,0),(1,1,0,0),(1,0,0,1)]

OPERATORS = [Operator(
  "Cross the creek with "+str(F)+" Farmer and "+str(f)+"fox"+str(c)+"chicken"+str(g)+"grain",
  lambda s, Farmer=F, fox=f,chicken=c,grain=g: s.can_move(Farmer,fox,chicken,grain),
  lambda s, Farmer=F, fox=f,chicken=c,grain=g: s.move(Farmer,fox,chicken,grain) ) 
  for (F,f,c,g) in Ffcg_combinations]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
