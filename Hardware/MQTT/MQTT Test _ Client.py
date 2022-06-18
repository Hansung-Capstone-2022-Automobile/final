import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from time import sleep

# Motor stat
STOP = 0
FORWARD = 1
BACKWORD = 2
RIGHT = 3
LEFT = 4

# Motor Channel
CH1 = 0  # RIGHT
CH2 = 1  # LEFT

# Pin IO Setting
OUTPUT = 1
INPUT = 0

# Pin Setting
HIGH = 1
LOW = 0

# PWM PIN
ENA = 26  # 37 pin
ENB = 0  # 27 pin

# GPIO PIN
IN1 = 19  # 37 pin
IN2 = 13  # 35 pin
IN3 = 6  # 31 pin
IN4 = 5  # 29 pin


# PIN Setting function
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz PWM move
    pwm = GPIO.PWM(EN, 100)
    # PWM STOP
    pwm.start(0)
    return pwm


# Motor Setting function
def setMotorContorl(pwm, INA, INB, speed, stat):
    # Motor Speed Control PWM
    pwm.ChangeDutyCycle(speed)

    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)

    # BACKWORD
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)

    # STOP
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)


def setMotor(ch, speed, stat):
    if ch == CH1:
        # pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        # pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmB, IN3, IN4, speed, stat)


# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
# 핀 설정후 PWM 핸들 얻어옴
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)


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
    if str(msg.payload.decode("utf-8")) == "forward":
        setMotor(CH1, 25, FORWARD)
        setMotor(CH2, 24, FORWARD)

        print("forward")
    elif str(msg.payload.decode("utf-8")) == "backward":
        setMotor(CH1, 25, BACKWORD)
        setMotor(CH2, 24, BACKWORD)

        print("backward")
    elif str(msg.payload.decode("utf-8")) == "right":
        setMotor(CH1, 30, BACKWORD)
        setMotor(CH2, 30, FORWARD)

        print("right")
    elif str(msg.payload.decode("utf-8")) == "left":
        setMotor(CH1, 30, FORWARD)
        setMotor(CH2, 30, BACKWORD)

        print("left")
    elif str(msg.payload.decode("utf-8")) == "stop":
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)

        print("stop")
    elif str(msg.payload.decode("utf-8")) == "exit":
        GPIO.cleanup()
        print("exit")


client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect('broker.hivemq.com', 1883)

client.subscribe('test/hello', 1)
client.loop_forever()

GPIO.cleanup()
