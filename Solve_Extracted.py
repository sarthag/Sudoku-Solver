import numpy as np
from  Extract_Digits import *
from Solver.solver import *


def solve_sudoku(sudoku_image_path):
    
    model1 = "model_dumps/model1.joblib"
    model2 = "model_dumps/model2.joblib"
    model3 = "model_dumps/model3.joblib"
    
    unsolved1 = extract_digit_values(sudoku_image_path, model1)
    solved, solved_sudoku = solve(unsolved1.copy())
    if solved: return solved_sudoku
    
    unsolved2 = extract_digit_values(sudoku_image_path, model2)
    solved, solved_sudoku = solve(unsolved2.copy())
    if solved: return solved_sudoku
    
    unsolved3 = extract_digit_values(sudoku_image_path, model3)
    solved, solved_sudoku = solve(unsolved3.copy())
    if solved: return solved_sudoku

    faults = list(np.where(unsolved1 != unsolved2)) + list(np.where(unsolved2 != unsolved3)) + list(np.where(unsolved3 != unsolved1))
    unsolved = unsolved1.copy()
    for idx in faults:
        entry = ""
        possible = set([unsolved1[idx[0], idx[1]], unsolved2[idx[0], idx[1]], unsolved3[idx[0], idx[1]]] )
        for i in possible: entry = entry + i 
        unsolved[idx[0], idx[1]] = entry

    solved, solved_sudoku = solve(unsolved.copy())
    if solved: return solved_sudoku
    
    for idx in faults: unsolved[idx[0], idx[1]] = "0"
    solved, solved_sudoku = solve(unsolved.copy())
    if solved: return solved_sudoku
    
    return None