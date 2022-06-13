import cv2
import numpy as np

img = cv2.imread('./asset/edge_pt_img.png')
img_copy = img.copy()
img_resize = cv2.resize(img, (640, 480)) # (640,480,3)

height, width, channel = img_resize.shape
crop = img_resize[int(height/2):, :, :]

gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 30, 70)

# 직선 성분 검출
lines = cv2.HoughLinesP(canny, 1, np.pi / 180., 160, minLineLength=50, maxLineGap=5)
img_lines = cv2.line(crop, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0,0,255), 5)

contours, _ = cv2.findContours(canny.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_image = cv2.drawContours(crop, contours, -1, (0,255,0), 3)
#cv2.imshow('contours_image', contours_image)

contours_xy = np.array(contours, dtype=object)
# contours_xy[i][j][0][0] / contours_xy[i][j][0][1]
print(contours_xy[0][0][0][0])
print(contours_xy[0][0][0][1])
print(contours_xy[1][0][0][0])
print(contours_xy[1][0][0][1])

#dot_draw = cv2.line(crop, (contours_xy[0][0][0][0], contours_xy[0][0][0][1]), (contours_xy[0][0][0][0], contours_xy[0][0][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[1][0][0][0], contours_xy[1][0][0][1]), (contours_xy[1][0][0][0], contours_xy[1][0][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[2][0][0][0], contours_xy[2][0][0][1]), (contours_xy[2][0][0][0], contours_xy[2][0][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[3][0][0][0], contours_xy[3][0][0][1]), (contours_xy[3][0][0][0], contours_xy[3][0][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[4][0][0][0], contours_xy[4][0][0][1]), (contours_xy[4][0][0][0], contours_xy[4][0][0][1]), (0,255,0), 20)

dot_draw = cv2.line(crop, (contours_xy[0][1][0][0], contours_xy[0][1][0][1]), (contours_xy[0][1][0][0], contours_xy[0][1][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[1][1][0][0], contours_xy[1][1][0][1]), (contours_xy[1][1][0][0], contours_xy[1][1][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[2][1][0][0], contours_xy[2][1][0][1]), (contours_xy[2][1][0][0], contours_xy[2][1][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[3][1][0][0], contours_xy[3][1][0][1]), (contours_xy[3][1][0][0], contours_xy[3][1][0][1]), (0,255,0), 20)
#dot_draw = cv2.line(crop, (contours_xy[4][1][0][0], contours_xy[4][1][0][1]), (contours_xy[4][1][0][0], contours_xy[4][1][0][1]), (0,255,0), 20)

cv2.imshow('canny', canny)
cv2.imshow('crop', crop)

key = cv2.waitKey(1) & 0xFF
if key == ord("q"):
    message = "exit"

cv2.waitKey(0)
cv2.destroyAllWindows()