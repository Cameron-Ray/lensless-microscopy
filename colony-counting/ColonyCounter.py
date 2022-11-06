# Code adapted from: http://www.sixthresearcher.com/counting-blue-and-white-bacteria-colonies-with-python-and-opencv/
# Author: Alvaro Sebastian
# Adapted by: Cameron Ray - University of Cape Town

import cv2
import numpy as np

# Load the bacterial colony image
image_orig = cv2.imread("colonies.png")
height_orig, width_orig = image_orig.shape[:2]

lower = np.array([100,100,100])
upper = np.array([130,130,130])

# Create a mask highlighting the bacteria
image_mask = cv2.inRange(image_orig, lower, upper)

# Use the mask to make colonies more pronounced
image_res = cv2.bitwise_and(image_orig, image_orig, mask = image_mask)

# load the image, convert it to grayscale, and blur it slightly
image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

# perform edge detection, then perform a dilation + erosion to close gaps in between object edges
image_edged = cv2.Canny(image_gray, 65, 100)
image_edged = cv2.dilate(image_edged, None, iterations=1)
image_edged = cv2.erode(image_edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0]

count = 0
maxsize = 0

# loop over the contours individually
for c in cnts:
# Check the area of the contour
    maxsize = cv2.contourArea(c) if maxsize < cv2.contourArea(c) else maxsize

    if cv2.contourArea(c) < 100:
        continue
        
    # Find the Convex Hull of the contour
    hull = cv2.convexHull(c)
    cv2.drawContours(image_res,[hull],0,(255,0,0),2)
    count += 1

    
cv2.putText(image_res, "Count: " + str(count), (10, height_orig - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
 
print(maxsize)
# Writes the output image
cv2.imwrite("output.jpg", image_res)
