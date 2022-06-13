import cv2
import numpy as np
import math

def calc_length(h, w):
    return math.sqrt((h - 191) ** 2 + (w - 128) ** 2)

cap = cv2.VideoCapture('../asset/test_avi.mp4')
frame_count = 0
for i in range(3):
    _, frame = cap.read()
width = 256 #640
half_width = 128 #320
height = 192 #480

lineV = np.ones((1, half_width)) # (1,320) 즉, 180도를 측정할 직선 성분
lineH = np.ones((height, 1)) # (480,1) 즉, 90도를 측정할 직선 성분
dim1 = np.zeros((height-1, half_width))
dim2 = np.zeros((height, half_width)) # 우측 빈 절반
dim3 = np.block([[dim1], [lineV]]) # (479,320) (1,320) -> (480,320) 직선
dim4 = np.eye(half_width) # (320,320) 대각 선분만 1
dim5 = np.rot90(dim4)
dim6 = np.zeros((height-half_width, half_width)) # dim3 윗 부분을 채워 줄 부분
dim7 = np.zeros((height, half_width)) # 우측 빈 절반
dim8 = np.zeros((height, half_width-1)) # 중앙 직선을 그리기 위해 -1
dim9 = np.vstack([dim6,dim4]) # 135도 직선 그림
dim10 = np.vstack([dim6, dim5]) # 135도 직선 그림

mask1 = np.block([dim3, dim2]) # (480,640) -좌측:180도 -우측:아무것도 없는 배경
mask2 = np.block([dim9, dim2]) # (480,640) -좌측:135도 -우측:아무것도 없는 배경
mask3 = np.block([dim8, lineH, dim7]) # (480,640) -중앙 직선
mask4 = np.block([dim7, dim10]) # (480,640) -좌측:아무것도 없는 배경 -우측:45도
mask5 = np.block([dim2, dim3])

# print(mask1.shape)
# print(mask2.shape)
# print(mask3.shape)
# print(mask4.shape)
# print(mask5.shape)
# cv2.imshow('mask1', mask1*255) # 180도 직선
# cv2.imshow('mask2', mask2*255) # 135도 직선
# cv2.imshow('mask3', mask3*255) # 90도 직선
# cv2.imshow('mask4', mask4*255) # 45도 직선
# cv2.imshow('mask5', mask5*255) # 0도 직선
# cv2.waitKey()

try:
    while cap.isOpened():
        _, frame = cap.read() # 영상을 받아왔으면
        #print(f'count{frame_count}') # 프레임 당 횟수 출력
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

        len1 = 0
        len2 = 0
        len3 = 0
        len4 = 0
        len5 = 0

        if np.transpose(np.nonzero(mask1 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            # print(np.transpose(np.nonzero(mask1 * canny))[-1][0])
            # print(np.transpose(np.nonzero(mask1 * canny))[-1][1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask1*canny))[-1][1], np.transpose(np.nonzero(mask1*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치
            len1 = calc_length(np.transpose(np.nonzero(mask1 * canny))[-1][1], np.transpose(np.nonzero(mask1 * canny))[-1][0]) / (calc_length(191, 0))
            print('180도:', len1)

        if np.transpose(np.nonzero(mask2 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask2*canny))[-1])
            # print(np.transpose(np.nonzero(mask2 * canny))[-1][0])
            # print(np.transpose(np.nonzero(mask2 * canny))[-1][1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask2*canny))[-1][1], np.transpose(np.nonzero(mask2*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치
            len2 = calc_length(np.transpose(np.nonzero(mask2 * canny))[-1][1],np.transpose(np.nonzero(mask2 * canny))[-1][0]) / (calc_length(191 - 127, 0))
            print('135도:', len2)

        if np.transpose(np.nonzero(mask3 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask3*canny))[-1])
            # print(np.transpose(np.nonzero(mask3 * canny))[-1][0])
            # print(np.transpose(np.nonzero(mask3 * canny))[-1][1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask3*canny))[-1][1], np.transpose(np.nonzero(mask3*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치
            len3 = calc_length(np.transpose(np.nonzero(mask3 * canny))[-1][1],np.transpose(np.nonzero(mask3 * canny))[-1][0]) / (calc_length(0, 127))
            print('90도:', len3)

        if np.transpose(np.nonzero(mask4 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask4*canny))[-1])
            # print(np.transpose(np.nonzero(mask4 * canny))[-1][0])
            # print(np.transpose(np.nonzero(mask4 * canny))[-1][1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask4*canny))[-1][1], np.transpose(np.nonzero(mask4*canny))[-1][0]), 10, (0, 255, 255), -1)  # 자동차 위치
            len4 = calc_length(np.transpose(np.nonzero(mask4 * canny))[-1][1],np.transpose(np.nonzero(mask4 * canny))[-1][0]) / (calc_length(192, 191 - 127))
            print('45도:', len4)
        if np.transpose(np.nonzero(mask5 * canny)).size > 0:
            # print(np.transpose(np.nonzero(mask1*canny))[-1])
            cv2.circle(img_resize, (np.transpose(np.nonzero(mask5*canny))[0][1], np.transpose(np.nonzero(mask5*canny))[0][0]), 10, (0, 255, 255), -1)  # 자동차 위치
            len5 = calc_length(np.transpose(np.nonzero(mask5 * canny))[0][1],np.transpose(np.nonzero(mask5 * canny))[0][0]) / (calc_length(191, 255))

        crop = img_resize[int(height/2):,:,:]
        crop_resize = cv2.resize(crop, (width, height))

        cv2.imshow("orig", frame)
        cv2.imshow("update", img_resize)
        cv2.imshow("crop_resize", crop_resize)
        cv2.imshow("crop",crop)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count = frame_count + 1

finally:
    cap.release()
    cv2.destroyAllWindows()