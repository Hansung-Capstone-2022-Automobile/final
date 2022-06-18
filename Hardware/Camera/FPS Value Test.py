# 필요한 패키지 import
import cv2  # OpenCV(실시간 이미지 프로세싱) 모듈
import time  # 시간 처리 모듈

# 동영상 파일 경로 또는 카메라 index 번호
#video_path = "0"

# VideoCapture : 동영상 파일 또는 카메라 열기
capture = cv2.VideoCapture(0)

# FPS 평균값을 계산하기 위한 리스트
fps_list = []

while True:
    # FPS 측정 시작 시간
    start_time = time.time()

    # read : 프레임 읽기
    # [return]
    # 1) 읽은 결과(True / False)
    # 2) 읽은 프레임
    retval, frame = capture.read()

    # 읽은 프레임이 없는 경우 종료
    if not retval:
        break

    # 프레임 출력
    cv2.imshow("frame", frame)

    # 'q' 를 입력하면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # FPS 측정 중지 시간
    stop_time = time.time()

    # 프레임 10개의 평균 FPS 계산
    if len(fps_list) < 10:
        fps_list.append(1 / (stop_time - start_time))
    else:
        fps_list.append(1 / (stop_time - start_time))

        # FPS 측정 결과 출력
        print("[FPS : {:.2f}]".format(sum(fps_list) / len(fps_list)))

        # FPS 리스트 초기화
        fps_list = []

# 동영상 파일 또는 카메라를 닫고 메모리를 해제
capture.release()

# 모든 창 닫기
cv2.destroyAllWindows()