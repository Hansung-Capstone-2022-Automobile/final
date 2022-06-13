import cv2
import numpy as np

img = cv2.imread('./asset/edge_pt_img.png')
img_copy = img.copy()
img_resize = cv2.resize(img, (640, 480)) # (640,480,3)

height, width, channel = img_resize.shape

# (width, height)
# 자동차 위치 = (int(width/2), height)
x = int(width/2)
y = height
infinity = 10000
#dot_draw = cv2.line(img_resize, (x, y), (x, y), (0,255,0), 20)

cv2.circle(img_resize, (x,y), 10, (255,0,0), -1)

for i in range(0,7):
    angle = 0+30*i
    if(angle >= 360):
        break
    print(f'angle: {angle}')

    # y,x 좌표를 각도 기준으로 회전
    # 기존 좌표와 회전한 좌표를 선으로 이었을 때, 이미지 끝 점과 교차점이 생기도록
    # 회전한 좌표는 이미지 밖에 두도록 한다. 따라서 length는 아주 큰 값 infinity로 둔다.
    y_rotated = y + int(np.sin(-np.pi / 180 * angle)*infinity)
    x_rotated = x + int(np.cos(-np.pi / 180 * angle)*infinity)
    print(f'y회전좌표, x회전좌표: {y_rotated, x_rotated}')

    # 기존 좌표와 이미지 끝에 교차된 점 까지를 이은 직선을 그린다.
    ret, inner_point, clipped_point = cv2.clipLine((0,0,width-1, height-1), (x,y), (x_rotated, y_rotated))
    cv2.line(img_resize, (x,y), clipped_point, (255,0,0), 10)

key = cv2.waitKey(1) & 0xFF
if key == ord("q"):
    message = "exit"

cv2.imshow('img',img_resize)
cv2.waitKey(0)
cv2.destroyAllWindows()