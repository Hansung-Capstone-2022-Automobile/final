#GPIO (https://rudalskim.tistory.com/112)
#MOTOR CONTROL (https://github.com/JuyeolRyu/self-driving-rc-car)
#GPIO (https://rudalskim.tistory.com/112)
#MOTOR CONTROL (https://github.com/JuyeolRyu/self-driving-rc-car)

import RPi.GPIO as GPIO
from time import sleep

# Motor State
STOP = 0
FORWARD = 1
BACKWARD = 2

# Motor Channel
CHLF = 0  # 좌측 앞 모터
CHLB = 1  # 좌측 뒤 모터
CHRF = 2  # 우측 앞 모터
CHRB = 3  # 우측 뒤 모터

# PIN I/O Setting
OUTPUT = 1
INPUT = 0

# PIN Setting
HIGH = 1
LOW = 0

# Real PIN define
# PWM PIN (BCM PIN)
ENLF = 16  # 36 PIN
ENLB = 26  # 37 PIN
ENRF = 2  # 3 PIN
ENRB = 0  # 27 PIN

# GPIO PIN
IN1 = 12  # 32 PIN (LEFT FRONT)
IN2 = 18  # 12 PIN (LEFT FRONT)
IN3 = 19  # 37 PIN (LEFT BACK)
IN4 = 13  # 35 PIN (LEFT BACK)
IN5 = 24  # 18 PIN (RIGHT FRONT)
IN6 = 23  # 16 PIN (RIGHT FRONT)
IN7 = 6  # 31 PIN (RIGHT BACK)
IN8 = 5  # 29 PIN (RIGHT BACK)


# PIN Setting Algorithm
def setPinConfig(EN, INF, INO):  # EN, OFF, ON
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INF, GPIO.OUT)
    GPIO.setup(INO, GPIO.OUT)
    # Activate PWM in 100KHZ
    pwm = GPIO.PWM(EN, 100)
    # FIRST, PWM is STOP
    pwm.start(0)
    return pwm


# Motor Control Algorithm
def setMotorControl(pwm, INO, INF, speed, stat):
    # Motor speed Control to PWM
    pwm.ChangeDutyCycle(speed)

    # Forward
    if stat == FORWARD:
        GPIO.output(INO, HIGH)
        GPIO.output(INF, LOW)
    # Backward
    elif stat == BACKWARD:
        GPIO.output(INO, LOW)
        GPIO.output(INF, HIGH)
    # STOP
    elif stat == STOP:
        GPIO.output(INO, LOW)
        GPIO.output(INF, LOW)


# Motor Control Easily
def setMotor(ch, speed, stat):
    if ch == CHLF:
        setMotorControl(pwmLF, IN1, IN2, speed, stat)
    elif ch == CHLB:
        setMotorControl(pwmLB, IN3, IN4, speed, stat)
    elif ch == CHRF:
        setMotorControl(pwmRF, IN5, IN6, speed, stat)
    elif ch == CHRB:
        setMotorControl(pwmRB, IN7, IN8, speed, stat)


# GPIO Library Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor Pin Setting (Global Var)
pwmLF = setPinConfig(ENLF, IN1, IN2)  # in 100Hz
pwmLB = setPinConfig(ENLB, IN3, IN4)  # in 100Hz
pwmRF = setPinConfig(ENRF, IN5, IN6)  # in 100Hz
pwmRB = setPinConfig(ENRB, IN7, IN8)  # in 100Hz
# print('ENLF, ENLB, ENRF, ENRB =' ENLF, ENLB, ENRF, ENRB)

# def forward():
setMotor(CHLF, 20, FORWARD)
setMotor(CHLB, 20, FORWARD)
setMotor(CHRF, 20, FORWARD)
setMotor(CHRB, 20, FORWARD)
sleep(5)
print("forward")

# def backward():
setMotor(CHLF, 20, BACKWARD)
setMotor(CHLB, 20, BACKWARD)
setMotor(CHRF, 20, BACKWARD)
setMotor(CHRB, 20, BACKWARD)
sleep(5)
print("backward")

# def right():
setMotor(CHLF, 20, FORWARD)
setMotor(CHLB, 20, FORWARD)
setMotor(CHRF, 50, STOP)
setMotor(CHRB, 10, FORWARD)
sleep(5)
print("right")

# def left():
setMotor(CHLF, 50, STOP)
setMotor(CHLB, 10, FORWARD)
setMotor(CHRF, 20, FORWARD)
setMotor(CHRB, 20, FORWARD)
sleep(5)
print("left")

# def stop():
setMotor(CHLF, 0, STOP)
setMotor(CHLB, 0, STOP)
setMotor(CHRF, 0, STOP)
setMotor(CHRB, 0, STOP)
sleep(5)
print("stop")

GPIO.cleanup()



