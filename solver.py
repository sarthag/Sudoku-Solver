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
  boxes = np.zeros((9,9))

  for i in range(9):
    for j in range(9):
      box_no, pos = box_info(i, j)
      boxes[box_no][pos] = puzzle[i][j]
  boxes = np.int_(boxes)

  return rows, cols, boxes

