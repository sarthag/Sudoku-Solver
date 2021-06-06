import pandas as pd
import numpy as np
from solver import *
import time

df = pd.read_csv("sudoku.csv")
puzzles = df["quizzes"].values[:1]
solns = df["solutions"].values[:1]

def make_array(grid):
    sudoku = [i for i in grid]
    sudoku = np.int_(sudoku).reshape((9,9))  
    sudoku = sudoku.astype(str)
    return sudoku
    
tot = 0
num_correct = 0
t1 = time.process_time()
for i in range(len(puzzles)):
    puzz = puzzles[i]
    soln = solns[i]
    unsolved = make_array(puzz)
    print_grid(unsolved)
    solution = make_array(soln)
    print("solution")
    print_grid(solution)
    start = time.process_time()
    sol, solved = solve(unsolved)
    print("solved")
    print_grid(solved)
    if False not in (solved == solution): num_correct += 1
    
    tot += sol
    end = time.process_time()
    print("time: ", end - start)

t2 = time.process_time()

print("solved:", tot, "/", len(puzzles))
print("correct:", num_correct, "/", len(puzzles))
print("total time:", t2 - t1)
    