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
    
    #takes in an image file and returns the cropped square image of the sudoku inside it 
    
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
    corners = cv2.goodFeaturesToTrack(mask, 4, 0.1, 250)
    corners = np.int0(corners)
    corner_values = []
    if corners is not None:
        for i in corners:
            x,y = i.ravel()
            corner_values.append((x,y))


    #warp and crop the image based on the corner coordinates
    corner_values = order_corners(np.array(corner_values, np.float32))
    dim = int(np.mean(np.max(corner_values, axis = 0) - np.min(corner_values, axis = 0))) + 1

    dim_final = np.array([[0,0], [dim, 0], [0, dim], [dim, dim]], np.float32)
    matrix = cv2.getPerspectiveTransform(corner_values, dim_final)
    sudoku = cv2.warpPerspective(img, matrix, grey.shape)[:int(dim), :int(dim)]
    
    return sudoku