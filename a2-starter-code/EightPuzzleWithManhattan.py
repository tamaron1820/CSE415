"""Student Name 1: Tatsuhiko Araki
Student Name 2: Chenliang Huang :student number: 2276084
UW NetID: taraki
My student number: 2276178
"""
from EightPuzzle import *


g=[[0,1,2],[3,4,5],[6,7,8]]

def h(s):
    """We return an estimate of the horizontal distance
  between s and the goal city."""
    count =0
    for m in range(0, 3):
      for n in range(0, 3):
        if s.b[m][n]!=0:
            for i in range(0,3):
                for j in range(0,3):
                    if s.b[m][n]==g[i][j]:
                        count += abs(m-i) +abs (n-j)
                        break
                    else:
                        continue
    return count
    