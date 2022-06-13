import cv2
import numpy as np
import math
width = 640
half_width = 320
height = 240

img = cv2.imread('./asset/test_img.jpg')
img_resize = cv2.resize(img, (width, height))
gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(img_resize, 100, 255)

thres = 100
threshold = cv2.inRange(gray, 0, thres) # (이미지, 하한값, 상한값)
print(gray)
cv2.imshow('img', img_resize)
cv2.imshow('gray', gray)
#cv2.imshow('canny', canny)
cv2.imshow('thres', threshold)

key = cv2.waitKey(1) & 0xFF
if key == ord("q"):
    message = "exit"

cv2.waitKey(0)
cv2.destroyAllWindows()