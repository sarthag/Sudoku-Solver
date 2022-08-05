# Sudoku-Solver
The core idea behid this project is to solve sudokus from images of puzzles. 

There are 3 components to the project 
1. Extracting 81 images of Sudoku digits/blank squares form an image of a sudoku.
2. Builing an unsolved sudoku from the images of digits. 
3. Building a 100% accurate solver using a modifies backtracking algorithm to release a solution from a 2D-array of valid sudoku digits 

Frameworks used: Python, NumPy, ScikitLearn, OpenCV


EXTRACTION OF DIGITS FROM SUDOKU IMAGE (OpenCV):

This is done using ExtractDigits.py

![image](https://user-images.githubusercontent.com/74304695/183119051-a4f628aa-5536-491e-bdfd-4be5e15e3f4e.png)

The order corners function returns the corners of the puzzle in an ordered fashion.


![image](https://user-images.githubusercontent.com/74304695/183119133-8a8fc0b1-94a0-4bdd-b624-5535d076aec5.png)

Extract SUdoku crops the image and applies a gaussian blur to cleare clearer distinctions between numbers and the background. This is done by finding the largest polygon in the image and warping it through the corners, plotting it on a mask to get the coordinates of the puzzle so that it can be extracted. 


![image](https://user-images.githubusercontent.com/74304695/183120671-136e92f6-cc45-4f88-932b-bb9ccdc9316a.png)

Crop Digits cuts the sudoku into it's 81 squares to get the inividual digits.

![image](https://user-images.githubusercontent.com/74304695/183120721-29f0ed5f-7f33-4104-9f72-c25afd222c70.png)

Darken background tries to identify the non digit pixels and completely blacken them

![image](https://user-images.githubusercontent.com/74304695/183120811-5861fb38-6d88-47f0-b593-260bae33675f.png)

Get Digits sotred all the extracted digits in a numpy array. 



OBTAING DIGIT VALUES (ScikitLearn):

The digits values were obtined using an ensemble of 3 MLP classifiers using different ratios of MNIST digits and Ppinted image digits.
(Printed Image Dataset: https://www.kaggle.com/kshitijdhama/printed-digits-dataset)

This was done as specic models judged different digits to different accuracies and using the ensemble ensures that the correst digit is one of the guessed digit. The incorrect digits can be later elimineted through the backtracking solver model.

Model 1: 

![image](https://user-images.githubusercontent.com/74304695/183122412-1b4b16cf-a759-49e5-8015-695479ccaadb.png)

Model 2:

![image](https://user-images.githubusercontent.com/74304695/183122524-4d54d8e1-16c1-4c7e-ae6a-6d35f279bccf.png)

Model 3:

![image](https://user-images.githubusercontent.com/74304695/183122586-b0a9ef57-2b2c-4c1b-89eb-789c1fad5a3a.png)


The digits are then extracted through the extract digit values function in the Extract_Digits.py model

![image](https://user-images.githubusercontent.com/74304695/183122788-3261e650-79e5-4fb8-bf38-e510b85a06f1.png)



BUILING THE SUDOKU SOLVER: 

THe solver was built using a modifed backtracking algorithm that finds the optimal digit to test and then subsequently attemps to solve the puzzle based on the assumption, this drastically increases the accuracy of the same.
(Peter Norwig's insightful Article where he created an algorithm to solve every possible sudoku: http://www.norvig.com/sudoku.html)
(Dataset of 1Mil sudokus, which is useful for testing: https://www.kaggle.com/bryanpark/sudoku)

![image](https://user-images.githubusercontent.com/74304695/183124362-a98e3e7a-98ed-48ae-ab28-43046adc4d86.png)

I was able to solve all tested sudokus form the dataset and 12/12 of Peter Norwig's hardest computer generated sudokus. 11/12 were solved within 2 seconds and the last (the objectively hardest sudoku) was solved in 30 minutes.


The following was the process of the solver: 

![image](https://user-images.githubusercontent.com/74304695/183124492-4196dd6b-2200-45aa-9a40-f96ad93883de.png)

Get dummies goes through the puzzle and finds the digits that can be placed in each box. 


![image](https://user-images.githubusercontent.com/74304695/183124698-6db91b2c-5eab-48bd-8000-5f79e3e2707d.png)

Update puzzle reduces the puzzle to it's minimum based on confirmed values in the box, row and column. 


![image](https://user-images.githubusercontent.com/74304695/183124875-6738cc30-692a-4a8c-8c21-e7709143c8ba.png)

![image](https://user-images.githubusercontent.com/74304695/183125019-d251247b-b714-4081-9ba6-1479dfda4a8f.png)


Is valid checks the validity of the puzzle to decide the subsequent move to sove the puzzle ans is complete checks wheter the puzzle has been completed


![image](https://user-images.githubusercontent.com/74304695/183125123-635d72ea-108e-4f6a-b625-3c304e4f4994.png)

Search value finds the box with minimum number of probables to make a guess on. The logic behind this is 
if a box with 2 probalbles is chosen and reduced 1/2 of the possible puzzles are eliminated , but is a box with 4 probables is chosen only 1/4th of the possible puzzles are eliminated on the worst case scenario.


![image](https://user-images.githubusercontent.com/74304695/183125529-c4ea2946-1396-42f6-8033-226cec808069.png)

Test guess implements the solver and attempts to find the completely reduced puzzle after each guess, while keeping a track of changes so that they can be backtracked if an error is made. 



FINAL COMPILATION AND RESULS: 

All the steps are put together in Solve Extracted function in the Solve Extracted model. 

![image](https://user-images.githubusercontent.com/74304695/183126049-97e7f810-4e4e-424d-880b-b9c91abf175c.png)

Once the digits are extracted, the digits are extracted using individual modes and are solved using the solver, if any of them return a complete a complete and valid puzzle, the same is returned as the solution, if none is able to return the same, the digits that are different in the unsolved sudokus are all added as probables and the puzzle is run through the solver, if still are errors, the sqares are made bank and the puzzle is solved. 
THe powerful solver is levereged to overcome any shortcomings in the digit exractor. 


Results form test images: 

![image](https://user-images.githubusercontent.com/74304695/183127069-bd6cf444-3a33-4fc8-8531-d997b55f4e5e.png) ![image](https://user-images.githubusercontent.com/74304695/183127118-39d12d13-44c6-492a-9d82-278c0ef53d9c.png) ![image](https://user-images.githubusercontent.com/74304695/183127161-b55ee837-9fe2-4a1f-bdea-3087f5697397.png)


LIMITATIONS: 
1. Discoloured and distorted images can result in failure or incorrect results
2. Images need to be stored locally


IMPROVEMETS:
1. An app can be built to obtain images from a phone camera.
2. A provision to enter digits via keyboard if the image is distorted
