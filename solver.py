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
  
  
  checkpoint, checkpoint_dummy = puzzle.copy(), dummy_puzzle.copy()

  #updating dummies
  for i in range(9):
    for j in range(9):
      if len(dummy_puzzle[i][j]) != 1:
        continue
      
      puzzle[i][j] = dummy_puzzle[i][j]
      box_no , index_in_box = box_info(i, j)
      
      for k in range(9):
        if k != j:
          dummy_puzzle[i][k] = dummy_puzzle[i][k].replace(dummy_puzzle[i][j], "")
          
        if k != i:
          dummy_puzzle[k][j] = dummy_puzzle[k][j].replace(dummy_puzzle[i][j], "")

      for idx, (r, c) in enumerate(box_indexes[box_no]):
        if idx != index_in_box: 
          dummy_puzzle[r][c] = dummy_puzzle[r][c].replace(dummy_puzzle[i][j], "")
        

  if False in (dummy_puzzle == checkpoint_dummy):
    puzzle, dummy_puzzle = update_puzzle(puzzle, dummy_puzzle)
    
  return puzzle, dummy_puzzle


def find_individuals(puzzle, dummy_puzzle):
  
  checkpoint = dummy_puzzle.copy()
  for i in range(9):
    row = {"1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[]}
    col = {"1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[]}
    box = {"1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[]}
    
    for j in range(9):
      
      if puzzle[i][j] == "0":
        for k in dummy_puzzle[i][j]:
          row[k].append(j)
          
      if puzzle[j][i] == "0":
        for k in dummy_puzzle[j][i]:
          col[k].append(j)
  
    
    for idx, (r, c) in enumerate(box_indexes[i]):
      if puzzle[r][c] == "0":
        for k in dummy_puzzle[r][c]:
          box[k].append((r,c))
      
    for val in "123456789":
      if len(row[val]) == 1:
        dummy_puzzle[i][row[val][0]] = dummy_puzzle[i][row[val][0]].replace(dummy_puzzle[i][row[val][0]], val)
        

      if len(col[val]) == 1:
        dummy_puzzle[col[val][0]][i] = dummy_puzzle[col[val][0]][i].replace(dummy_puzzle[col[val][0]][i], val)
        
      if len(box[val]) == 1:
        dummy_puzzle[box[val][0][0]][box[val][0][1]] = dummy_puzzle[box[val][0][0]][box[val][0][1]].replace(dummy_puzzle[box[val][0][0]][box[val][0][1]], val)
  
  if False in (dummy_puzzle == checkpoint):
    puzzle, dummy_puzzle = update_puzzle(puzzle, dummy_puzzle)
  
  return puzzle, dummy_puzzle
       

def is_valid(puzzle, dummy_puzzle):

  for i in range(9):
    for j in range(9):
      if dummy_puzzle[i][j] is None or len(dummy_puzzle[i][j]) == 0:
        return False

      
  puzzle_cols = puzzle.T
  for i in range(9):
    row_count = np.unique(puzzle[i], return_counts = True)
    if row_count[0][0] == "0":
      if True in (row_count[1][1:] > 1):
        return False
      
    else:
      if True in (row_count[1] > 1):
        return False
    
    col_count = np.unique(puzzle_cols[i], return_counts = True)
    if col_count[0][0] == "0":
      if True in (row_count[1][1:] > 1):
        return False
    else:
      if True in (row_count[1] > 1):
        return False
      
    box = box_indexes[i]
    entries = np.array([puzzle[r][c] for (r,c) in box])
    box_count = np.unique(entries, return_counts=True) 
    if box_count[0][0] == "0":
      if True in (box_count[1][1:] > 1):
        return False
    else:
      if True in (box_count[1] > 1):
        return False
      
  return True 
    
  
def is_complete(puzzle):
  if "0" not in puzzle:
    return True
  return False


def search_value(puzzle, dummy_puzzle):
  
  for len_curr in range(2,10):
    for i in range(9):
      for j in range(9):
        if len(dummy_puzzle[i][j]) != len_curr:
          continue
        
        return i, j, len_curr


def test_guess(puzzle, dummy_puzzle, layer = 1):
  #print("entering layer", layer)
  row, col, len_curr = search_value(puzzle, dummy_puzzle) 
  if len_curr == None:
    return puzzle
  
  checkpoint, checkpoint_dummy = puzzle.copy(), dummy_puzzle.copy()
  
  for pos in range(len_curr):
    if layer == 1:
      print(row, col)
    if pos >= len(dummy_puzzle[row][col]):
      continue
    #print("pos:", pos)
    #print("len:", len_curr)
    #print("rc:", row, col)
    #print("val:", dummy_puzzle[row][col])
    dummy_puzzle[row][col] = dummy_puzzle[row][col].replace(dummy_puzzle[row][col], dummy_puzzle[row][col][pos])
    puzzle, dummy_puzzle = update_puzzle(puzzle,dummy_puzzle)
    if is_valid(puzzle, dummy_puzzle):
      
      if is_complete(puzzle):
        return puzzle

      puzzle, dummy_puzzle = find_individuals(puzzle, dummy_puzzle)
      if is_valid(puzzle, dummy_puzzle):
        if is_complete(puzzle):
          return puzzle

        puzzle = test_guess(puzzle, dummy_puzzle, layer + 1)
        if puzzle is not None:
          return puzzle
            
    puzzle, dummy_puzzle = checkpoint, checkpoint_dummy
    #print_grid(checkpoint_dummy)
    #print("exiting layer", layer)
    
    continue

  

 
def solve(unsolved):
  dummy_puzzle = get_dummies(unsolved)
  print_grid(dummy_puzzle)
  checkpoint, checkpoint_dummy = update_puzzle(unsolved, dummy_puzzle)
  if is_complete(checkpoint):
    print("complete")
    return checkpoint
  
  checkpoint, checkpoint_dummy = find_individuals(checkpoint, checkpoint_dummy)
  if is_complete(checkpoint):
    print("complete")
    return checkpoint
  
  print(is_valid(checkpoint, checkpoint))
  
  solved = test_guess(checkpoint, checkpoint_dummy)
  print_grid(solved)
  print(is_valid(solved, solved), is_complete(solved)) 