import numpy as np
import pandas as pd 
from solver import *
from print_grid import print_grid
import time


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
#unsolved[0][0] = unsolved[0][0].replace(unsolved[0][0], "")
#print(is_valid(unsolved, unsolved))

#solve(unsolved)
def make_array(grid):
    sudoku = [i for i in grid]
    for i in range(81):
        if sudoku[i] == ".":
            sudoku[i] ="0"
    sudoku = np.int_(sudoku).reshape((9,9))  
    sudoku = sudoku.astype(str)
    return sudoku
    
    
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
unsolved2 = make_array(grid2)
print(unsolved2)

hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
hard01 = make_array(hard1)
print(hard01)

impossible = "85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4."
impossible1 = make_array(impossible)

start = time.process_time()
solve(impossible1)
end = time.process_time()
print("time: ", end - start)


