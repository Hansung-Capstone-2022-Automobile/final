import cv2  # OpenCV(실시간 이미지 프로세싱) 모듈
import numpy as np
import onnxruntime
import torchvision.transforms as transforms
import math

model = "./DuckieWithoutCamera.onnx"
sess = onnxruntime.InferenceSession(model)
to_tensor = transforms.ToTensor()

width = 256
half_width = 128
height = 192

resize = transforms.Resize([height, width])

lineV = np.ones((1, half_width))
lineH = np.ones((height, 1))
dim1 = np.zeros((height - 1, half_width))
dim2 = np.zeros((height, half_width))
dim3 = np.block([[dim1], [lineV]])
dim4 = np.eye(half_width)
dim5 = np.rot90(dim4)
dim6 = np.zeros((height-half_width, half_width))
dim7 = np.zeros((height, half_width))
dim8 = np.zeros((height, half_width - 1))
dim9 = np.vstack([dim6, dim4])
dim10 = np.vstack([dim6, dim5])

mask1 = np.block([dim3, dim2])
mask2 = np.block([dim9, dim2])
mask3 = np.block([dim8, lineH, dim7])
mask4 = np.block([dim7, dim10])
mask5 = np.block([dim2, dim3])


def calc_length(h, w):
    return math.sqrt((h - 191) ** 2 + (w - 127) ** 2)

# level = 0
# def onChange(j):
#     level = j
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     np.putmask(gray, gray > level, 255)
#     np.putmask(gray, gray < level, 0)
#     cv2.imshow('Gray', gray)

frame = cv2.imread('road1.jpg')
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray', gray)
# cv2.createTrackbar('level', 'Gray', 0, 255, onChange)
# cv2.waitKey()

while True:
    # 프레임 출력
    # cv2.imshow('Frame', frame)
    img_resize = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    # cv2.createTrackbar('level', 'Gray', 0, 255, onChange)
    '''
    이미지 마스킹
    '''
    np.putmask(gray, gray > 117, 255) # 임계점을 넘으면 255
    np.putmask(gray, gray < 117, 0) # 임계점 보다 낮으면 0
    cv2.imshow('Gray', gray)
    canny = (gray + 1)*255 # 색 반전
    # canny = cv2.Canny(gray, 10, 90)
    # frame = cv2.resize(frame, (256, 192))
    # img = to_tensor(frame)
    # Input = np.expand_dims(img, axis=0)

    len1 = 0
    len2 = 0
    len3 = 0
    len4 = 0
    len5 = 0

    if np.transpose(np.nonzero(mask1 * canny)).size > 0:
        len1 = calc_length(np.transpose(np.nonzero(mask1 * canny))[-1][0],
                           np.transpose(np.nonzero(mask1 * canny))[-1][1]) / (calc_length(191, 0))
        cv2.circle(img_resize,
                   (np.transpose(np.nonzero(mask1 * canny))[-1][1], np.transpose(np.nonzero(mask1 * canny))[-1][0]), 10,
                   (0, 255, 255), -1)  # 자동차 위치

    if np.transpose(np.nonzero(mask2 * canny)).size > 0:
        len2 = calc_length(np.transpose(np.nonzero(mask2 * canny))[-1][0],
                           np.transpose(np.nonzero(mask2 * canny))[-1][1]) / (
                   calc_length(191 - 127, 0))
        cv2.circle(img_resize,
                   (np.transpose(np.nonzero(mask2* canny))[-1][1], np.transpose(np.nonzero(mask2 * canny))[-1][0]), 10,
                   (0, 255, 255), -1)  # 자동차 위치

    if np.transpose(np.nonzero(mask3 * canny)).size > 0:
        len3 = calc_length(np.transpose(np.nonzero(mask3 * canny))[-1][0],
                           np.transpose(np.nonzero(mask3 * canny))[-1][1]) / (
                   calc_length(0, 127))
        cv2.circle(img_resize,
                   (np.transpose(np.nonzero(mask3 * canny))[-1][1], np.transpose(np.nonzero(mask3 * canny))[-1][0]), 10,
                   (0, 255, 255), -1)  # 자동차 위치

    if np.transpose(np.nonzero(mask4 * canny)).size > 0:
        len4 = calc_length(np.transpose(np.nonzero(mask4 * canny))[-1][0],
                           np.transpose(np.nonzero(mask4 * canny))[-1][1]) / (
                   calc_length(191 - 127, 255))
        cv2.circle(img_resize,
                   (np.transpose(np.nonzero(mask4 * canny))[-1][1], np.transpose(np.nonzero(mask4 * canny))[-1][0]), 10,
                   (0, 255, 255), -1)  # 자동차 위치

    if np.transpose(np.nonzero(mask5 * canny)).size > 0:
        len5 = calc_length(np.transpose(np.nonzero(mask5 * canny))[0][0],
                           np.transpose(np.nonzero(mask5 * canny))[0][1]) / (
                   calc_length(191, 255))
        cv2.circle(img_resize,
                   (np.transpose(np.nonzero(mask5 * canny))[0][1], np.transpose(np.nonzero(mask5 * canny))[0][0]), 10,
                   (0, 255, 255), -1)  # 자동차 위치
        # cv2.circle(img_resize,
        #            (255, 191), 10,
        #            (0, 255, 255), -1)  # 자동차 위치

    obs_1 = np.array([[len1, len2, len3, len4, len5]]).astype(np.float32)
    # output = sess.run(["discrete_actions"],
    #                   {"obs_0": Input, "obs_1": obs_1,
    #                    "action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

    output = sess.run(["discrete_actions"],
                      {"obs_0": obs_1,
                       "action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

    message = "stop"
    if output[0][0][0] == 0:
        message = "stop"
    elif output[0][0][0] == 1:
        message = "go"
    elif output[0][0][0] == 2:
        message = "back"
    elif output[0][0][0] == 3:
        message = "left"
    elif output[0][0][0] == 4:
        message = "right"
    print(message)
    cv2.imshow('asdf', canny)
    cv2.imshow('Frame', img_resize)
    '''
    MQTT SERVER
    '''
    # 'test/hello' 라는 topic 으로 메세지 발행
    # client_mqtt.loop_stop()

    # # 'q' 키를 입력하면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


# 소켓 닫기

# MQTT 닫기

print('연결 종료')

# 모든 창 닫기
cv2.destroyAllWindows()