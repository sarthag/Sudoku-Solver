import numpy as np
from print_grid import print_grid

grps = [(0,1,2), (3,4,5), (6,7,8)]
box_indexes = [[(i,j) for i in r for j in c] for r in grps for c in grps]
                      
def box_info(row, col):
  
  #Takes in the row and column of the entry and 
  #Returns the box number and position in the box array
  
  box_no = int((row/3))*3 + int(col/3)
  index_in_box = (row%3)*3 + col%3
  
  return box_no, index_in_box    


def get_dummies(puzzle):
  
  #returns an array with the possible entries in each box
  dummy_puzzle = puzzle.copy()  
  
  for i in range(9):
    for j in range(9):
      if dummy_puzzle[i][j] != "0":
        continue
  
      box_no, box_ind = box_info(i, j)
   
      possible = "123456789"
      
      for k in range(9):
        if len(possible) == 1: break
        possible = possible.replace(puzzle[i][k], "")
        possible = possible.replace(puzzle[k][j], "")
      
      for idx, (r, c) in enumerate(box_indexes[box_no]):
        if len(possible) == 1: break
        possible = possible.replace(puzzle[r][c], "")
   
      dummy_puzzle[i][j] = possible

  return dummy_puzzle
       
  
def update_puzzle(puzzle, dummy_puzzle):
  
  print_grid(puzzle)
  print_grid(dummy_puzzle)
  checkpoint = dummy_puzzle.copy()

  #updating dummies
  for i in range(9):
    for j in range(9):
      if len(dummy_puzzle[i][j]) != 1:
        continue
      
      puzzle[i][j] = dummy_puzzle[i][j]
      box_no , index_in_box = box_info(i, j)
      
      for k in range(9):
        if (i, k) == (i, j) or (k, j) == (i,j):
          continue
        
        dummy_puzzle[i, k] = dummy_puzzle[i, k].replace(dummy_puzzle[i][j], "")
        dummy_puzzle[k, j] = dummy_puzzle[k, j].replace(dummy_puzzle[i][j], "")

      for idx, (r, c) in enumerate(box_indexes[box_no]):
        if idx == index_in_box: 
          continue
        
        dummy_puzzle[r][c] = dummy_puzzle[r][c].replace(dummy_puzzle[i][j], "")

  if (sum(sum(dummy_puzzle == checkpoint))) != 81:
    update_puzzle(puzzle, dummy_puzzle)
    
  return puzzle, dummy_puzzle


def solve(unsolved):
  dummy_puzzle = get_dummies(unsolved)
  checkpoint, checkpoint_dummy = update_puzzle(unsolved, dummy_puzzle)
  
  