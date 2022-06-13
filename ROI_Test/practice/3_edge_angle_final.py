import cv2
import numpy as np

_SHOW_IMAGE = False
_SHOW_PRINT = False

def crop_img(img):
    img_resize = cv2.resize(img, (640, 480))  # (480,640,3)
    height, width, channel = img_resize.shape
    crop = img_resize[int(height/2):,:,:]
    return crop

def edge_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 30, 70)
    return canny

def find_xy(edge, crop, show=_SHOW_IMAGE):
    lines = cv2.HoughLinesP(edge, 1, np.pi/180., 160, minLineLength=50, maxLineGap=5)
    cv2.line(crop, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0, 0, 255), 5)
    cv2.line(crop, (lines[1][0][0], lines[1][0][1]), (lines[1][0][2], lines[1][0][3]), (0, 0, 255), 5)
    line_xy = set()
    for i in range(0, crop.shape[0]):
        for j in range(0, crop.shape[1]):
            this_img = crop[i][j]
            if this_img[0] == 0 and this_img[1] == 0 and this_img[2] == 255:
                line_xy.add((j, i))
    line_xy_list = list(line_xy)
    line_xy_list.sort()

    if show:
        cv2.imshow('edge_xy', crop)

    return line_xy_list

def draw_find_xy(crop, line_xy_list, show=_SHOW_IMAGE):
    for z in range(len(line_xy_list)):
        cv2.circle(crop, line_xy_list[z], 1, (255, 0, 0), -1)
    if show:
        show_image('draw_xy', crop, show)

def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)

def read_img(root):
    img = cv2.imread(root)
    img_copy = img.copy()

    cropping = crop_img(img)
    edge = edge_img(cropping)

    xy = find_xy(edge, cropping, show=True) # 허프변환 후 선 그리기
    print(f'선분 좌표:{xy}')

    draw_find_xy(cropping, xy, show=True) # 찾은 선분의 좌표를 점으로 그리기

    show_image('orig', img_copy, show=True)
    show_image('edge', edge, show=True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    read_img('./asset/edge_pt_img.png')