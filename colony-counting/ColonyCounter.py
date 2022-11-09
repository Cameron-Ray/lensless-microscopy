# Code adapted from: http://www.sixthresearcher.com/counting-blue-and-white-bacteria-colonies-with-python-and-opencv/
# Author: Alvaro Sebastian
# Adapted by: Cameron Ray - University of Cape Town

import cv2
import numpy as np

# Load the bacterial colony image
image_orig = cv2.imread("colony_count_test_2.jpg")
height_orig, width_orig = image_orig.shape[:2]

# image_orig = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)

lower = np.array([0,0,0])
upper = np.array([180,180,180])

# Create a mask highlighting the bacteria
image_mask = cv2.inRange(image_orig, lower, upper)

# Use the mask to make colonies more pronounced
image_res = cv2.bitwise_and(image_orig, image_orig, mask = image_mask)

# load the image, convert it to grayscale, and blur it slightly
image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_edged = cv2.Canny(image_gray, 95, 100)
image_edged = cv2.dilate(image_edged, None, iterations=3)
image_edged = cv2.erode(image_edged, None, iterations=3)

# find contours in the edge map
cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0]

count = 0
maxsize = 0

# loop over the contours individually
for c in cnts:
# Check the area of the contour

    maxsize = cv2.contourArea(c) if maxsize < cv2.contourArea(c) else maxsize

    if cv2.contourArea(c) < 10 or cv2.contourArea(c) > 30000:
        continue

    x,y,w,h = cv2.boundingRect(c)

    if w > 200 or h > 200:
        continue
        
    # Find the Convex Hull of the contour
    hull = cv2.convexHull(c)
    
    # cv2.rectangle(image_res,(x,y),(x+w,y+h),(0,255,0),2)
    
    cv2.drawContours(image_res,[hull],0,(0,255,0),2)
    count += 1

    
cv2.putText(image_res, str(count), (10, height_orig - 50), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10)
 
print(maxsize)
# Writes the output image
cv2.imwrite("output.jpg", image_res)
