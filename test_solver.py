import numpy as np
import pandas as pd 
from solver import *
from print_grid import print_grid


unsolved = np.array([[0, 0, 4, 3, 0, 0, 2, 0, 9],
                     [0, 0, 5, 0, 0, 9, 0, 0, 1],
                     [0, 7, 0, 0, 6, 0, 0, 4, 3],
                     [0, 0, 6, 0, 0, 2, 0, 8, 7],
                     [1, 9, 0, 0, 0, 7, 4, 0, 0],
                     [0, 5, 0, 0, 8, 3, 0, 0, 0],
                     [6, 0, 0, 0, 0, 0, 1, 0, 5],
                     [0, 0, 3, 5, 0, 8, 6, 9, 0],
                     [0, 4, 2, 9, 1, 0, 3, 0, 0]])

unsolved = unsolved.astype(str)
#solve(unsolved)

grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
unsolved2 = [i for i in grid2]
for i in range(81):
    if unsolved2[i] == ".":
        unsolved2[i] ="0"


unsolved2 = np.int_(unsolved2).reshape((9,9))  
unsolved2 = unsolved2.astype(str)

#solve(unsolved)