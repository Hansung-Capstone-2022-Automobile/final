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
#cv2.line(crop, (lines[0][0][2], lines[0][0][3]), (lines[0][0][2], lines[0][0][3]), (0,0,255), 5)

'''
cv2.line(crop, (lines[1][0][0], lines[1][0][1]), (lines[1][0][0], lines[1][0][1]), (0,0,255), 5)
cv2.line(crop, (lines[1][0][2], lines[1][0][3]), (lines[1][0][2], lines[1][0][3]), (0,0,255), 5)
cv2.line(crop, (lines[2][0][0], lines[2][0][1]), (lines[2][0][0], lines[2][0][1]), (0,0,255), 5)
cv2.line(crop, (lines[2][0][2], lines[2][0][3]), (lines[2][0][2], lines[2][0][3]), (0,0,255), 5)
cv2.line(crop, (lines[3][0][0], lines[3][0][1]), (lines[3][0][0], lines[3][0][1]), (0,0,255), 5)
cv2.line(crop, (lines[3][0][2], lines[3][0][3]), (lines[3][0][2], lines[3][0][3]), (0,0,255), 5)
'''
#cv2.line(crop, (lines[4][0][0], lines[4][0][1]), (lines[4][0][0], lines[4][0][1]), (0,0,255), 5)
#cv2.line(crop, (lines[4][0][2], lines[4][0][3]), (lines[4][0][2], lines[4][0][3]), (0,0,255), 5)
#print(lines[0][0][0], lines[0][0][1])
#print(lines[0][0][2], lines[0][0][3])
#print(lines[0])

'''
line_xy = np.array(img_lines)
print(line_xy[0][0][0])
dot_draw = cv2.line(crop, (line_xy[0][0][0], line_xy[0][0][1]), (line_xy[0][0][0], line_xy[0][0][1]), (0,255,0), 5)
'''

line_xy = set()
for i in range(0, crop.shape[0]):
    for j in range(0, crop.shape[1]):
        this_img = crop[i][j]
        if this_img[0] == 0 and this_img[1] == 0 and this_img[2]==255:
            line_xy.add((j,i))

line_xy_list = list(line_xy)
line_xy_list.sort()
print(f'선분 좌표:{line_xy_list}')
print(f'선분 좌표 1 : {line_xy_list[0]}')
print(f'선분 좌표 10 : {line_xy_list[200]}')
dot_draw = cv2.line(crop, line_xy_list[0], line_xy_list[0], (0,255,0), 5)
dot_draw = cv2.line(crop, line_xy_list[200], line_xy_list[200], (0,255,0), 5)

#cv2.imshow('orig', img)
#cv2.imshow('gray', gray)
cv2.imshow('canny', canny)
cv2.imshow('crop', crop)
#print(img_resize.shape)
#print(img.shape)

key = cv2.waitKey(1) & 0xFF
if key == ord("q"):
    message = "exit"

cv2.waitKey(0)
cv2.destroyAllWindows()