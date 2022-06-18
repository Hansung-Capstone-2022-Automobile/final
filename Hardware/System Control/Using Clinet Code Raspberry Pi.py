# 필요한 패키지 import
# Camera
import cv2  # OpenCV(실시간 이미지 프로세싱) 모듈
import socket  # 소켓 프로그래밍에 필요한 API를 제공하는 모듈
import pickle  # 바이트(bytes) 형식의 데이터 변환 모듈
import struct  # 바이트(bytes) 형식의 데이터 처리 모듈
# MQTT
import paho.mqtt.client as mqtt

'''
MQTT SERVER
'''
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))

'''
MQTT CLIENT
'''
# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# 로컬 아닌, 원격 mqtt broker에 연결
# address : broker.hivemq.com
# port: 1883 에 연결
client.connect('broker.hivemq.com', 1883)

'''
CAMERA SERVER
'''
# 서버 ip 주소 및 port 번호
ip = '192.168.101.15'
port = 50001

# 카메라 또는 동영상
capture = cv2.VideoCapture(0)

# 프레임 크기 지정
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 세로

# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 서버와 연결
    client_socket.connect((ip, port))

    print("연결 성공")

    # 메시지 수신
    while True:
        # 프레임 읽기
        retval, frame = capture.read()

        # imencode : 이미지(프레임) 인코딩
        # 1) 출력 파일 확장자
        # 2) 인코딩할 이미지
        # 3) 인코드 파라미터
        #   - jpg의 경우 cv2.IMWRITE_JPEG_QUALITY를 이용하여 이미지의 품질(0 ~ 100)을 설정
        #   - png의 경우 cv2.IMWRITE_PNG_COMPRESSION을 이용하여 이미지의 압축률(0 ~ 9)을 설정
        # [return]
        # 1) 인코딩 결과(True / False)
        # 2) 인코딩된 이미지
        retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

        # dumps : 데이터를 직렬화
        # - 직렬화(serialization) : 효율적으로 저장하거나 스트림으로 전송할 때 데이터를 줄로 세워 저장하는 것
        frame = pickle.dumps(frame)

        # print("전송 프레임 크기 : {} bytes".format(len(frame)))

        # sendall : 데이터(프레임) 전송
        # - 요청한 데이터의 모든 버퍼 내용을 전송
        # - 내부적으로 모두 전송할 때까지 send 호출
        # struct.pack : 바이트 객체로 변환
        # - > : 빅 엔디안(big endian)
        #   - 엔디안(endian) : 컴퓨터의 메모리와 같은 1차원의 공간에 여러 개의 연속된 대상을 배열하는 방법
        #   - 빅 엔디안(big endian) : 최상위 바이트부터 차례대로 저장
        # - L : 부호없는 긴 정수(unsigned long) 4 bytes
        client_socket.sendall(struct.pack(">L", len(frame)) + frame)
        # client_socket.recv(512)

        '''
        MQTT CLIENT
        '''
        # test/hello 라는 topic 구독
        client.subscribe('test/hello', 1)
        client.loop_start()
        # 새로운 thread()가 아니라 프로그램을 block() 한다.
        # 자동으로 reconnect 하는 것과, 멈출 때 loop_stop() 부르는 것은 똑같다.
        # client.loop_forever()

# 메모리를 해제
capture.release()


