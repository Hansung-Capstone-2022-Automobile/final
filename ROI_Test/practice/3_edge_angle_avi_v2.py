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

        crop = img_resize[int(height / 2):, :, :]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 30, 70)
        cv2.imshow('canny', canny)
        # 직선 성분 검출
        line_xy = set()
        #print(f'canny detect shape:{canny.shape}')
        for i in range(0, canny.shape[0]):
            for j in range(0, canny.shape[1]):
                this_img = canny[i][j]
                if this_img == 255:
                    line_xy.add((j, i))
        line_xy_list = list(line_xy)
        line_xy_list.sort()
        #print(f'선분 좌표:{line_xy_list}')

        #for z in range(len(line_xy_list)):
            #cv2.circle(crop, line_xy_list[z], 1, (255, 0, 0), -1)

        # 자동차 위치 = (int(width/2), height)
        height_crop, width_crop, channel_crop = crop.shape
        x = int(width_crop / 2)
        y = height_crop
        cv2.circle(crop, (x, y), 10, (0, 0, 255), -1)  # 자동차 위치
        #print('기준 좌표:', x, y)

        # 선분 좌표 저장
        target_0 = []
        dis_0 = []
        target_45 = []
        dis_45 = []
        target_90 = []
        dis_90 = []
        target_135 = []
        dis_135 = []
        target_180 = []
        dis_180 = []

        for find in line_xy_list:
            # 0도
            if find[1] == y - 1 and find[0] > x:
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_0: {find}')
                dis_0.append(math.sqrt(math.pow(find[0] - x, 2) + math.pow(find[1] - y, 2)))
                target_0.append(find)

            # 45도
            elif -find[0] + 560 == find[1]:
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_45: {find}')
                dis_45.append(math.sqrt(math.pow(find[0] - x, 2) + math.pow(find[1] - y, 2)))
                target_45.append(find)

            # 90도
            elif find[0] == x - 1:
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_90: {find}')
                dis_90.append(math.sqrt(math.pow(find[0] - x, 2) + math.pow(find[1] - y, 2)))
                target_90.append(find)

            # 135도 (좌측)
            elif find[0] - 80 == find[1]:
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_135: {find}')
                dis_135.append(math.sqrt(math.pow(find[0] - x, 2) + math.pow(find[1] - y, 2)))
                target_135.append(find)

            # 180도 (좌측)
            elif find[1] == y - 1 and find[0] < x:
                cv2.circle(crop, (find[0], find[1]), 10, (0, 255, 255), -1)
                # print(f'target_135: {find}')
                dis_180.append(math.sqrt(math.pow(find[0] - x, 2) + math.pow(find[1] - y, 2)))
                target_180.append(find)

        # 기준점과 이어진 선 그리기
        if len(target_0) >= 1:
            min_dis_index_0 = dis_0.index(min(dis_0))
            cv2.line(crop, (x, y), (target_0[min_dis_index_0][0], target_0[min_dis_index_0][1]), (0, 255, 0), 5)
        elif len(target_0) == 0:
            cv2.line(crop, (x, y), (2 * x, y), (255, 255, 0), 3)

        if len(target_45) >= 1:
            min_dis_index_45 = dis_45.index(min(dis_45))
            cv2.line(crop, (x, y), (target_45[min_dis_index_45][0], target_45[min_dis_index_45][1]), (0, 255, 0), 5)
        elif len(target_45) == 0:
            cv2.line(crop, (x, y), (x, y // 2), (255, 255, 0), 3)

        if len(target_90) >= 1:
            min_dis_index_90 = dis_90.index(min(dis_90))
            cv2.line(crop, (x, y), (target_90[min_dis_index_90][0], target_90[min_dis_index_90][1]), (0, 255, 0), 5)
        elif len(target_90) == 0:
            cv2.line(crop, (x, y), (x, 0), (255, 255, 0), 3)

        if len(target_135) >= 1:
            min_dis_index_135 = dis_135.index(min(dis_135))
            cv2.line(crop, (x, y), (target_135[min_dis_index_135][0], target_135[min_dis_index_135][1]), (0, 255, 0), 5)
        elif len(target_135) == 0:
            cv2.line(crop, (x, y), (0, y // 2), (255, 255, 0), 3)

        if len(target_180) >= 1:
            min_dis_index_180 = dis_180.index(min(dis_180))
            cv2.line(crop, (x, y), (target_180[min_dis_index_180][0], target_180[min_dis_index_180][1]), (0, 255, 0), 5)
        elif len(target_180) == 0:
            cv2.line(crop, (x, y), (0, y), (255, 255, 0), 3)

        cv2.imshow("orig", frame)
        cv2.imshow("update", crop)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count = frame_count+1
finally:
    cap.release()
    cv2.destroyAllWindows()