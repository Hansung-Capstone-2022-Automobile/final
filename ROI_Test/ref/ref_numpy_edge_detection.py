import cv2
import numpy as np
import math

cap = cv2.VideoCapture('./asset/test_avi.mp4')
frame_count = 0
for i in range(3):
    _, frame = cap.read()
width = 640
half_width = 320
height = 240
lineV = np.ones((1, half_width))
lineH = np.ones((height, 1))
dim1 = np.zeros((height-1, half_width))
dim2 = np.zeros((height, half_width))
dim3 = np.block([[dim1], [lineV]])
dim4 = np.eye(height)
dim5 = np.rot90(dim4)
dim6 = np.zeros((height, half_width-height))
dim7 = np.zeros((height, half_width))
dim8 = np.zeros((height, half_width-1))

mask1 = np.block([dim3, dim2])
mask2 = np.block([dim6, dim4, dim7])
mask3 = np.block([dim8, lineH, dim7])
mask4 = np.block([dim7, dim5, dim6])
mask5 = np.block([dim2, dim3])

# cv2.imshow('mask1', mask1*255)
# cv2.imshow('mask2', mask2*255)
# cv2.imshow('mask3', mask3*255)
# cv2.imshow('mask4', mask4*255)
# cv2.imshow('mask5', mask5*255)
# cv2.waitKey()

try:
    while cap.isOpened():
        _, frame = cap.read() # 영상을 받아왔으면
        print(f'count{frame_count}') # 프레임 당 횟수 출력
        img_resize = cv2.resize(frame, (width,height)) # (480,640,3) -> 크기 변경
        # i_height, i_width, channel = img_resize.shape # 이미지 크기 변경

        # crop = img_resize[int(i_height / 2):, :, :] # 아래 절반만 추출
        gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY) # 그레이 스케일로 변경
        canny = cv2.Canny(gray, 30, 70) # Canny edge를 사용하여 선분 추출
        cv2.imshow('canny', canny) # 선분 보여주기
        # cv2.imshow('mask1', mask1*canny)
        # cv2.imshow('mask2', mask2*canny)
        # cv2.imshow('mask3', mask3*canny)
        # cv2.imshow('mask4', mask4*canny)
        # cv2.imshow('mask5', mask5*canny)
        # 직선 성분 검출
        # line_xy = set()
        # #print(f'canny detect shape:{canny.shape}')
        # for i in range(0, canny.shape[0]): # 캐니 좌표 흰색 부분만 찾아서 좌표에 더하기 이 부분은 마스크 만드는 걸로 변경
        #     for j in range(0, canny.shape[1]):
        #         this_img = canny[i][j]
        #         if this_img == 255:
        #             line_xy.add((j, i))
        # line_xy_list = list(line_xy)
        # line_xy_list.sort() # 정렬

        # 자동차 위치 = (int(width/2), height)
        height_crop, width_crop, channel_crop = img_resize.shape  # 중심점 좌표 찾기
        x = int(width_crop / 2)
        y = height_crop
        cv2.circle(img_resize, (x, y), 10, (0, 0, 255), -1)  # 자동차 위치

        if np.transpose(np.nonzero(mask1 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask1*canny))[-1][1], np.transpose(np.nonzero(mask1*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치

        if np.transpose(np.nonzero(mask2 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask2*canny))[-1][1], np.transpose(np.nonzero(mask2*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치

        if np.transpose(np.nonzero(mask3 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask3*canny))[-1][1], np.transpose(np.nonzero(mask3*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치

        if np.transpose(np.nonzero(mask4 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask4*canny))[-1][1], np.transpose(np.nonzero(mask4*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치

        if np.transpose(np.nonzero(mask5 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask5*canny))[0][1], np.transpose(np.nonzero(mask5*canny))[0][0]), 10, (0, 255, 255), -1)  # 자동차 위치

        cv2.imshow("orig", frame)
        cv2.imshow("update", img_resize)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count = frame_count + 1

finally:
    cap.release()
    cv2.destroyAllWindows()
