import cv2
import numpy as np

cap = cv2.VideoCapture('./asset/test_avi.mp4')

for i in range(3):
    _, frame = cap.read()

try:
    while cap.isOpened():
        _, frame = cap.read()
        img_resize = cv2.resize(frame, (640,480)) # (480,640,3)
        height, width, channel = img_resize.shape

        crop = img_resize[int(height / 2):, :, :]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 30, 70)

        # 직선 성분 검출
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180., 160, minLineLength=50, maxLineGap=5)
        img_lines = cv2.line(crop, (lines[0][0][0], lines[0][0][1]), (lines[0][0][2], lines[0][0][3]), (0, 0, 255), 5)
        img_lines = cv2.line(crop, (lines[1][0][0], lines[1][0][1]), (lines[1][0][2], lines[1][0][3]), (0, 0, 255), 5)
        line_xy = set()
        for i in range(0, crop.shape[0]):
            for j in range(0, crop.shape[1]):
                this_img = crop[i][j]
                if this_img[0] == 0 and this_img[1] == 0 and this_img[2] == 255:
                    line_xy.add((j, i))

        line_xy_list = list(line_xy)
        line_xy_list.sort()

        print(f'선분 좌표:{line_xy_list}')
        for z in range(len(line_xy_list)):
            cv2.circle(crop, line_xy_list[z], 1, (255, 0, 0), -1)

        # print(line_xy_list[0][0], line_xy_list[0][1])
        # print(type(line_xy_list), type(line_xy_list[0][0]))

        # 자동차 위치 = (int(width/2), height)
        height_crop, width_crop, channel_crop = crop.shape
        x = int(width_crop / 2)
        y = height_crop
        cv2.circle(crop, (x, y), 10, (0, 0, 255), -1)  # 자동차 위치
        cv2.circle(crop, (0, 0), 10, (0, 0, 255), -1)  # (0,0) 지점
        cv2.circle(crop, (640, 240), 10, (0, 0, 255), -1)  # (640,240) 지점
        print('가준 좌표:', x, y)

        # 선분 좌표 저장
        target_0 = []
        target_45 = []
        target_90 = []
        target_135 = []
        target_180 = []
        for find in line_xy_list:
            # 0도 (우측)
            if find[1] == y - 1 and find[0] > x:
                target_0.append(find)
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_0: {find}')
            # 45도 (우측)
            elif -find[0] + 560 == find[1]:
                target_45.append(find)
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_45: {find}')
            # 90도 (수직)
            elif find[0] == x - 1:
                target_90.append(find)
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_90: {find}')
            # 135도 (좌측)
            elif find[0] - 80 == find[1]:
                target_135.append(find)
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_135: {find}')
            # 180도 (좌측)
            elif find[1] == y - 1 and find[0] < x:
                target_180.append(find)
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_180: {find}')

        # 기준점과 이어진 선 그리기
        ## target=0
        if len(target_0) >= 1:
            target_center_num0 = len(target_0) // 2
            print('---target degree = 0---')
            print(f'target_index:{target_center_num0}')
            print(f'target_len:{len(target_0)}')
            print(f'target:{target_0[target_center_num0]}')
            cv2.circle(crop, (target_0[target_center_num0][0], target_0[target_center_num0][1]), 10, (0, 255, 0), -1)
            cv2.line(crop, (x, y), (target_0[target_center_num0][0], target_0[target_center_num0][1]), (0, 255, 0), 5)
        elif len(target_0) == 0:
            cv2.line(crop, (x, y), (2 * x, y), (255, 255, 0), 3)

        ## target=45
        if len(target_45) >= 1:
            target_center_num45 = len(target_45) // 2
            print('---target degree = 45---')
            print(f'target_index:{target_center_num45}')
            print(f'target_len:{len(target_45)}')
            print(f'target:{target_45[target_center_num45]}')
            cv2.circle(crop, (target_45[target_center_num45][0], target_45[target_center_num45][1]), 10, (0, 255, 0),
                       -1)
            cv2.line(crop, (x, y), (target_45[target_center_num45][0], target_45[target_center_num45][1]), (0, 255, 0),
                     5)
        elif len(target_45) == 0:
            cv2.line(crop, (x, y), (x, y // 2), (255, 255, 0), 3)

        ## target=90
        if len(target_90) >= 1:
            target_center_num90 = len(target_90) // 2
            print('---target degree = 90---')
            print(f'target_index:{target_center_num90}')
            print(f'target_len:{len(target_90)}')
            print(f'target:{target_90[target_center_num90]}')
            cv2.circle(crop, (target_90[target_center_num90][0], target_90[target_center_num90][1]), 10, (0, 255, 0),
                       -1)
            cv2.line(crop, (x, y), (target_90[target_center_num90][0], target_90[target_center_num90][1]), (0, 255, 0),
                     5)
        # 90도에 해당하는 선분 좌표가 없는경우 기준선으로 직선 그리기
        elif len(target_90) == 0:
            cv2.line(crop, (x, y), (x, 0), (255, 255, 0), 3)

        ## target=135
        if len(target_135) >= 1:
            target_center_num135 = len(target_135) // 2
            print('---target degree = 135---')
            print(f'target_index:{target_center_num135}')
            print(f'target_len:{len(target_135)}')
            print(f'target:{target_135[target_center_num135]}')
            cv2.circle(crop, (target_135[target_center_num135][0], target_135[target_center_num135][1]), 10,
                       (0, 255, 0), -1)
            cv2.line(crop, (x, y), (target_135[target_center_num135][0], target_135[target_center_num135][1]),
                     (0, 255, 0), 5)
        elif len(target_135) == 0:
            cv2.line(crop, (x, y), (0, y // 2), (255, 255, 0), 3)

        ## target=180
        if len(target_180) >= 1:
            target_center_num180 = len(target_180) // 2
            print('---target degree = 180---')
            print(f'target_index:{target_center_num180}')
            print(f'target_len:{len(target_180)}')
            print(f'target:{target_180[target_center_num180]}')
            cv2.circle(crop, (target_180[target_center_num180][0], target_180[target_center_num180][1]), 10,
                       (0, 255, 0), -1)
            cv2.line(crop, (x, y), (target_180[target_center_num180][0], target_180[target_center_num180][1]),
                     (0, 255, 0), 5)
        elif len(target_180) == 0:
            cv2.line(crop, (x, y), (0, y), (255, 255, 0), 3)

        cv2.imshow("orig", frame)
        cv2.imshow("update", crop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()