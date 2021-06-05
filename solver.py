import numpy as np
import pandas as pd 


def box_info(row, col):
  
  #Takes in the row and column of the entry and 
  #Returns the box number and position in the box array
  
  box_no = int((row/3))*3 + int(col/3)
  index_in_box = (row%3)*3 + col%3
  
  return box_no , index_in_box 


def get_parts(puzzle):
  
  #Takes in puzzle with rows as arrays and 
  #Returns puzzle with rows, columns and bozes as subarrays
  
  rows = puzzle
  cols = puzzle.T
  boxes = np.zeros((9,9)).astype(str)

  for i in range(9):
    for j in range(9):
      box_no, pos = box_info(i, j)
      boxes[box_no][pos] = puzzle[i][j]


  return rows, cols, boxes


def update_puzzle(row, col, digit):
  pass


def get_dummies(puzzle):

  #returns an array with the possible entries in each box
  puzzle, puzzle_cols, puzzle_box = get_parts(puzzle)  
  dummy_puzzle = puzzle.copy()  
  
  for i in range(9):
    for j in range(9):
      if dummy_puzzle[i][j] != "0":
        continue
      
      box_no, box_ind = box_info(i, j)
      possible = "123456789"
      
      for k in range(9):
        possible = possible.replace(puzzle[i][k], "")
        possible = possible.replace(puzzle_cols[j][k], "")
        possible = possible.replace(puzzle_box[box_no][k], "")
        if len(possible) == 1: break
    
      dummy_puzzle[i][j] = possible
      if len(possible) == 1: update_puzzle(i, j, possible)
      
  return dummy_puzzle
       
  