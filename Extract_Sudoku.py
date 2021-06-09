import numpy as np
import cv2 


def order_corners(corner_values):
    
    #Function to take in the pixel values of the corver points and 
    #returns then in the order ->
    #top-left, top-right, bottom-left, bottom-roght
    
    ordered = corner_values.copy()
    corner_values = corner_values
    min_sum = np.sum(np.max(corner_values, axis = 0))
    max_sum = 0
    for i in range(4):
        if sum(corner_values[i]) <= min_sum: 
            ordered[0] = corner_values[i]
            min_sum = sum(corner_values[i])

        if sum(corner_values[i]) >= max_sum: 
            ordered[3] = corner_values[i]
            max_sum = sum(corner_values[i])
 
    for i in range(4):
        if False not in (corner_values[i] == ordered[0]) or False not in (corner_values[i] == ordered[3]): 
            continue

        k = corner_values[i] - ordered[0]
        if k[0] > k[1]:
            ordered[1] = corner_values[i]
    
        else:
            ordered[2] = corner_values[i]
      
    return ordered 



def extract_sudoku(image_file_path):
    
    #takes in an image file and returns the cropped square image of the sudoku inside it and the size of the image 
    
    #load the image and turn it into greyscale and apply gaussian blur
    img = cv2.imread(image_file_path)     
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3,3), cv2.BORDER_DEFAULT)


    #find the largest polygon in the image
    canny = cv2.Canny(grey, 50, 200)
    contours, hierarchies = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    polygon = contours[0]


    #plot the largest polygon on a mask and find to corrdinates of the corners
    mask = np.zeros(img.shape[:2], dtype = "uint8")
    cv2.drawContours(mask, polygon, -1, (255,0,0), 10)
    corners = cv2.goodFeaturesToTrack(mask, 4, 0.1, 200)
    corners = np.int0(corners)
    corner_values = []
    if corners is not None:
        for i in corners:
            x,y = i.ravel()
            corner_values.append((x,y))


    #warp and crop the image based on the corner coordinates
    corner_values = order_corners(np.array(corner_values, np.float32))
    dim = int(np.mean(np.max(corner_values, axis = 0) - np.min(corner_values, axis = 0))) + 1
    dim = (int(dim/9))*9
    dim_final = np.array([[0,0], [dim, 0], [0, dim], [dim, dim]], np.float32)
    matrix = cv2.getPerspectiveTransform(corner_values, dim_final)
    sudoku = cv2.warpPerspective(img, matrix, grey.shape)[:int(dim), :int(dim)]
    
    return sudoku



def translate(image, x, y):
    
    #-x --> left
    #+x --> Right
    #-y --> Up
    #+y --> Down
    
    trans_mat = np.float32([[1, 0, x], [0, 1, y]])
    dimentions = (image.shape[1], image.shape[0])
    
    return cv2.warpAffine(image, trans_mat, dimentions)



def crop_digit(image, row, col):
    
    #inputs 28 x 28 image and removes the box lines to best possible extent
    
    if col == 0:
        image = translate(image, 4, 0)
        image = translate(image, -2, 0)
    
    elif col == 1:
        image = translate(image, 3, 0)
        image = translate(image, -1, 0)
    
    elif col == 2:
        image = translate(image, 4, 0)
        image = translate(image, -3, 0)
        
    elif col == 3:
        image = translate(image, -3, 0)
        image = translate(image, 3, 0)
        
    elif col == 4:
        image = translate(image, -3, 0)
        image = translate(image, 4, 0)
        
    elif col == 5:
        image = translate(image, -2, 0)
        image = translate(image, 3, 0)
        
    elif col == 6:
        image = translate(image, -4, 0)
        image = translate(image, 4, 0)
        
    elif col == 7:
        image = translate(image, -3, 0)
        image = translate(image, 1, 0)
        
    elif col == 8:
        image = translate(image, -4, 0)
        image = translate(image, 2, 0)
        
        
    
    if row == 0:
        image = translate(image, 0, -1)
        image = translate(image, 0, 4)
       
    if row == 1:
        image = translate(image, 0, 3)
        image = translate(image, 0, -3)
    
    if row == 2:
        image = translate(image, 0, 3)
        image = translate(image, 0, -3)
    
    if row == 3:
        image = translate(image, 0, -2)
    
    if row == 4:
        image = translate(image, 0, 1)
        image = translate(image, 0, -3)
    
    if row == 5:
        image = translate(image, 0, 1)
        image = translate(image, 0, -3)
    
    if row == 6:
        image = translate(image, 0, -4)
        image = translate(image, 0, 1)
       
    if row == 7:
        image = translate(image, 0, -3)
        
    if row == 8:
        image = translate(image, 0, -4)
    
    
    return image



def darken_background(image):
    
    #Takes in 28 x 28 image and darkens the background to 0
    
    dim = image.shape[0]
    pixel_max = np.max(np.max(image))
    pixel_mean = np.mean(np.mean(image))
    
    if (pixel_max <= 125) or (pixel_max - pixel_mean) <= 45:
        image = np.float32(np.zeros_like(image))
        return image
    
    elif (pixel_mean > 90) and (pixel_max - pixel_mean) <= 85:
        image = np.float32(np.zeros_like(image))
        return image
        
    
    for i in range(dim):
        for j in range(dim):
            
            if image[i][j] <= (pixel_mean + 25):
                image[i][j] = np.float32(0)
    
    image = translate(image, -4, -3)   
    image = translate(image, 7, 6)
    image = translate(image, -3, -3)
    return image



def get_digits(sudoku):
    
    #returns an array with all the digit values of the sudoku
    sudoku = cv2.cvtColor(sudoku, cv2.COLOR_BGR2GRAY)
    digits = []
    dim_digit = int(sudoku.shape[0]/9)
    
    for row in range(9):
        for col in range(9):
            
            #Loading digit
            digit = sudoku[dim_digit*row : dim_digit*(row+1), dim_digit*col : dim_digit*(col+1)]
            digit = cv2.resize(digit, (28,28), interpolation = cv2.INTER_CUBIC)
            digit = 255-digit
            
            #Applying transformations to the digit
            digit = crop_digit(digit, row, col)
            digit = darken_background(digit)
            digits.append(digit) 
    
    digits = np.array(digits).reshape(9, 9, 28, 28)
            
    return digits