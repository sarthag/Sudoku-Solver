import numpy as np

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
      if len(puzzle[i][j]) != 1:
        puzzle[i][j] = '0' 
  
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
  
  #Function to recursively update dummy values in the puzzle based on neighbours
  #Returns a puzzle with minimum number of possible probales

  checkpoint, checkpoint_dummy = puzzle.copy(), dummy_puzzle.copy()

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
  
  #Finds any location which is the only possible loction for a number in a row, column or box
  #And assigns said value to the box 
  
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

  #Checks validity of the puzzle by checking whether there are duplicates in rows, clouns and boxes
  
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
      if True in (col_count[1][1:] > 1):
        return False
    else:
      if True in (col_count[1] > 1):
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
  
  #Checks whether all values in the puzzle are filled 
  
  if "0" not in puzzle:
    return True
  return False


def search_value(puzzle, dummy_puzzle):
  
  #Finds the box with least number of probables to make a guess
  
  for len_curr in range(2,10):
    for i in range(9):
      for j in range(9):
        if len(dummy_puzzle[i][j]) != len_curr:
          continue
      
        return i, j, len_curr
  
  return None, None, None


def test_guess(puzzle, dummy_puzzle, checkpoints = {}, layer = 1):
  
  #Substitues probable values in a chosen box and tests implications
  #Follows Backtracking to make guesses and attempts to minimize 
  #Guesses needed by attempting to completely sove the puzzle after each guess
  
  row, col, len_curr = search_value(puzzle, dummy_puzzle) 
  if len_curr == None:
    return puzzle
  
  checkpoints[layer] = puzzle.copy(), dummy_puzzle.copy()
  
  for value in dummy_puzzle[row][col]:
    dummy_puzzle[row][col] = value

    puzzle, dummy_puzzle = update_puzzle(puzzle,dummy_puzzle)
    if is_valid(puzzle, dummy_puzzle):
      
      if is_complete(puzzle):
        return puzzle

      puzzle, dummy_puzzle = find_individuals(puzzle, dummy_puzzle)
      if is_valid(puzzle, dummy_puzzle):
        if is_complete(puzzle):
          return puzzle

        puzzle = test_guess(puzzle, dummy_puzzle, checkpoints=checkpoints, layer = layer+1)

        if puzzle is not None:
          return puzzle
         
    puzzle, dummy_puzzle = checkpoints[layer]
    continue


def solve(unsolved):
  
  #Final implementation of algorthim
  
  dummy_puzzle = get_dummies(unsolved)
  checkpoint, checkpoint_dummy = update_puzzle(unsolved, dummy_puzzle)
  if is_valid(checkpoint, checkpoint_dummy) and is_complete(checkpoint):
    return True, checkpoint
  
  checkpoint, checkpoint_dummy = find_individuals(checkpoint, checkpoint_dummy)
  if is_valid(checkpoint, checkpoint_dummy) and is_complete(checkpoint):
    return True, checkpoint

  solved = test_guess(checkpoint, checkpoint_dummy)
  if solved is None:
    return False, None
  
  if is_complete(solved) and is_valid(solved, solved):
    return True, solved
  
  else: 
    return False, None