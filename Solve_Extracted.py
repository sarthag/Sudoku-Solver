import numpy as np
import cv2
from  Extract_Digits import *
from Solver.solver import *
from Solver.print_grid import *


def modified_where(array):
    
    arr = np.where(array)
    indexes = np.column_stack((arr[0], arr[1]))
    return indexes
    
    
def place_digits(solved):
    
    final_image = np.ones((360, 360, 3), dtype = "uint8")*255
    curr = 0 
    for i in range(1, 9):
        curr += 40
        
        if i%3 == 0: thickness = 4
        else: thickness = 2
        
        cv2.line(final_image, (0, curr), (379, curr), (0, 0, 0), thickness)
        cv2.line(final_image, (curr, 0), (curr, 379), (0, 0, 0), thickness)
        
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(9):
        for j in range(9):
            cv2.putText(final_image, solved[i][j] ,(i*40 + 10, (j+1)*40 - 10), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    
    return final_image



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

    faults = list(modified_where(unsolved1 != unsolved2)) + list(modified_where(unsolved2 != unsolved3)) + list(modified_where(unsolved3 != unsolved1))
    unsolved = unsolved1.copy()
    
    for idx in faults:
        entry = ""
        possible = unsolved1[idx[0], idx[1]] + unsolved2[idx[0], idx[1]] + unsolved3[idx[0], idx[1]]
        for i in possible: 
            if i == "0":
                entry = "0"
                break
            if i not in entry:
                entry = entry + i 
        
        unsolved[idx[0], idx[1]] = entry

    solved, solved_sudoku = solve(unsolved.copy())
    if solved: return solved_sudoku
    
    for idx in faults: unsolved[idx[0], idx[1]] = "0"
    solved, solved_sudoku = solve(unsolved.copy())
    if solved: return solved_sudoku
    
    return None