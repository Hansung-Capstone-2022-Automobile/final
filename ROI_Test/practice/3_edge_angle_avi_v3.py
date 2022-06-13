import cv2
import numpy as np
import math

cap = cv2.VideoCapture('./asset/test_avi.mp4')
frame_count = 0
for i in range(3):
    _, frame = cap.read()

try:
    while cap.isOpened():
        _, frame = cap.read()
        print(f'count{frame_count}')
        img_resize = cv2.resize(frame, (640,480)) # (480,640,3)
        height, width, channel = img_resize.shape

        gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 30, 70)
        #cv2.imshow('canny', canny)

        mask = np.zeros_like(canny)  # (480,640)

        # 자동차 위치 = (int(width/2), height)
        height, width = mask.shape  # height = 480 / width = 640
        x = int(width / 2)
        y = height
        # print('기준 좌표:', x,y)

        # mask 0, 45, 90, 135, 180
        mask_0 = cv2.line(mask.copy(), (x, y - 1), (2 * x, y - 1), (255), 3)  # 0도
        mask_45 = cv2.line(mask.copy(), (x, y), (width, height // 2), (255), 1)  # 45도
        mask_90 = cv2.line(mask.copy(), (x, y), (x, 0), (255), 3)  # 90도
        mask_135 = cv2.line(mask.copy(), (x, y), (0, height // 2), (255), 3)  # 135도
        mask_180 = cv2.line(mask.copy(), (x, y - 1), (0, y - 1), (255), 3)  # 180도

        for index, mask_n in enumerate([mask_0, mask_45, mask_90, mask_135, mask_180]):
            mask_img = cv2.bitwise_and(canny, mask_n)
            globals()[f'line_xy_{index}'] = []
            globals()[f'line_dis_{index}'] = []
            for i in range(0, mask_img.shape[0]):
                for j in range(0, mask_img.shape[1]):
                    this_img = mask_img[i][j]
                    if this_img == 255:  # and (j<317 or j>323):
                        globals()[f'line_xy_{index}'].append((j, i))
                        globals()[f'line_dis_{index}'].append(math.sqrt(math.pow(j - x, 2) + math.pow(i - y, 2)))
                        # cv2.circle(mask, (x,y), 3, (255), -1) # 그려서 확인하기 (작동에서는 뺌)
            # print("xy:",globals()[f'line_xy_{index}'])
            # print("dis:",globals()[f'line_dis_{index}'])
            min_index = globals()[f'line_dis_{index}'].index(min(globals()[f'line_dis_{index}']))
            # print("min_index:",min_index)
            if len(globals()[f'line_dis_{index}']) >= 1:
                cv2.line(img_resize, (x, y),
                         (globals()[f'line_xy_{index}'][min_index][0], globals()[f'line_xy_{index}'][min_index][1]),
                         (0, 255, 0), 5)
            elif len(globals()[f'line_dis_{index}']) == 0:
                if index == 0:
                    cv2.line(img_resize, (x, y), (2 * x, y), (255, 255, 0), 3)
                elif index == 1:
                    cv2.line(img_resize, (x, y), (x, y // 2), (255, 255, 0), 3)
                elif index == 2:
                    cv2.line(img_resize, (x, y), (x, 0), (255, 255, 0), 3)
                elif index == 3:
                    cv2.line(img_resize, (x, y), (0, y // 2), (255, 255, 0), 3)
                elif index == 4:
                    cv2.line(img_resize, (x, y), (0, y), (255, 255, 0), 3)

        cv2.imshow("orig", frame)
        cv2.imshow("update", img_resize)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count = frame_count +1
finally:
    cap.release()
    cv2.destroyAllWindows()