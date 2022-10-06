import cv2
import numpy as np

# load the image
image_orig = cv2.imread("RedBloodCells.jpg")
height_orig, width_orig = image_orig.shape[:2]
 
print(height_orig, width_orig)

# copy of original image
image_to_process = image_orig.copy()

lower = np.array([26,26,26])
upper = np.array([115,115,115])

# find the colors within the specified boundaries
image_mask = cv2.inRange(image_to_process, lower, upper)

# apply the mask
image_res = cv2.bitwise_and(image_to_process, image_to_process, mask = image_mask)

cv2.imwrite("output.jpg",image_res)
# ## load the image, convert it to grayscale, and blur it slightly
# image_gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
# image_gray = cv2.GaussianBlur(image_gray, (5, 5), 0)

# # perform edge detection, then perform a dilation + erosion to close gaps in between object edges
# image_edged = cv2.Canny(image_gray, 50, 100)
# image_edged = cv2.dilate(image_edged, None, iterations=1)
# image_edged = cv2.erode(image_edged, None, iterations=1)

# # find contours in the edge map
# cnts = cv2.findContours(image_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# # loop over the contours individually
# for c in cnts:
        
#     # if the contour is not sufficiently large, ignore it
#     if cv2.contourArea(c) < 5:
#         continue
        
#     # compute the Convex Hull of the contour
#     hull = cv2.convexHull(c)
#     if color == 'blue':
#         # prints contours in red color
#         cv2.drawContours(image_contours,[hull],0,(0,0,255),1)
#     elif color == 'white':
#         # prints contours in green color
#         cv2.drawContours(image_contours,[hull],0,(0,255,0),1)

#     counter[color] += 1
#     #cv2.putText(image_contours, "{:.0f}".format(cv2.contourArea(c)), (int(hull[0][0][0]), int(hull[0][0][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

# # Print the number of colonies of each color
# print("{} {} colonies".format(counter[color],color))
 
# Writes the output image
# cv2.imwrite("output.jpg",image_mask)
