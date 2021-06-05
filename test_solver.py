import numpy as np
import pandas as pd 
from solver import *
from print_grid import print_grid


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

"""
str1 = "abc"
str2 = str1 + "d"
str3 = "123456789"
print(str3.replace("5", ""))
print(str3.replace("a", ""))
print("5" in ["123", "45"])
"""

print_grid(get_dummies(unsolved))


