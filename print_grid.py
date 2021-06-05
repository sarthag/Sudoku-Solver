import numpy as np


def align(text):
    length = len(text)
    if length%2 == 0: 
        text = text + " "
        length += 1
        
    gap = int((9-length)/2)
    text = " "*gap + text + " "*gap
    return text
    
    
def print_grid(array):
    arr = array.reshape((9,9))
    print("-"*84)
    for i in range(9):
        print("|", end = "") 
        for j in range(9):
            print(align(arr[i][j]), end = "")
            if j%3 == 2: print("|", end = "") 
        print()    
        if i%3 == 2: print("-"*84)