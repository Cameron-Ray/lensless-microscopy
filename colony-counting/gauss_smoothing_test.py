# importing cv2 
import cv2

# print(cv2.haveImageReader("micro.webp"))


img1 = cv2.imread("micro.webp", 0) 
denoise = cv2.fastNlMeansDenoising(img1, None, 20, 3, 12)
gblurimg = cv2.GaussianBlur(denoise, (5,5), 0)
cannyimg = cv2.Canny(denoise, 5, 40)

cv2.imshow("Denoise", denoise)
cv2.imshow("Blur", gblurimg)
cv2.imshow("Final", cannyimg)
cv2.moveWindow("Denoise", 100, 100)
cv2.moveWindow("Blur", 500, 100)
cv2.moveWindow("Final", 900, 100)
cv2.waitKey()
cv2.destroyAllWindows()