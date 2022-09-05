#!/usr/bin/env pybricks-micropython

#VERSION_1.01 : 코드 최적화, 변수 값, 로직은 조정 X
#AUTHOR : 김도윤

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pyhuskylens import *

ev3 = EV3Brick()
GRAB_MOTOR = Motor(Port.C)
LEFT_MOTOR = Motor(Port.B)
RIGHT_MOTOR = Motor(Port.D)
robot = DriveBase(LEFT_MOTOR,RIGHT_MOTOR,55.5,104)
COLOR_SENSOR_L = ColorSensor(Port.S1)
COLOR_SENSOR_R = ColorSensor(Port.S2)
HUSKYLENS = HuskyLens(Port.S3, debug=False)
ULTRASONIC_SENSOR = UltrasonicSensor(Port.S4) 
ev3.speaker.beep()

###########################################

GRAB_OPEN = -200 # 그랩 오픈 시 강도
GRAB_CLOSE = 200 # 그랩 닫을 시 강도
ULTRA_SENSSOR_DISTANCE = 115 # 초음파 감지 거리
BYPASS = 50 # 바이패스 거리

BREAK_POINT = 1

# P제어 설정
BLACK = 7 # 검은색 정의
WHITE = 60 # 흰색 정의
REFLECTION_VALUE = 30 # 반사광 강도
THRESHOLD = (BLACK+WHITE) / 2
DRIVE_SPEED = 100
PROPORTIONAL_GAIN = 1.2
GAIN = 0.8

B = 7  # Black 
W = 60  # White
G = 0.8  # gain
RV=30 # reflection value
BP = 1 # break point

###########################################

def Beep(): # 비프음 출력
    ev3.speaker.beep()

def Grab(grep):  # 그랩 닫기, 열기
    GRAB_MOTOR.run_until_stalled(grep, then = Stop.COAST, duty_limit=50)

def Reflection(g, reflect):  # 왼쪽라인 or 오른쪽라인 보정 / 오른쪽 센서일때 -PROPORTIONAL_GAIN
 보정 필요
    deviation = reflect - THRESHOLD
 # 선에서 벗어난 정도
    turn_rate = g * deviation
    robot.drive(DRIVE_SPEED, turn_rate)
    wait(100)

def Turn(degree): # 돌기
    robot.turn(degree)

def Follow_left_line(): # 왼쪽라인 따라가기
    while COLOR_SENSOR_R.reflection() > REFLECTION_VALUE: 
        Reflection(PROPORTIONAL_GAIN, COLOR_SENSOR_L.reflection())

def Follow_right_line(): # 오른쪽라인 따라가기
    while COLOR_SENSOR_R.reflection() > REFLECTION_VALUE: 
        Reflection(PROPORTIONAL_GAIN, COLOR_SENSOR_L.reflection())

def ULTRA_Distance(): # 초음파 센서 거리 감지 
    while ULTRASONIC_SENSOR.distance() > ULTRA_SENSSOR_DISTANCE: 
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD)
    robot.drive(100,rate)
    wait(80)

def DRIVE_UNTIL_BLUE(): # 직진, 파란색 발견시 정지
        while COLOR_SENSOR_L.color()!= Color.BLUE:  
            print(COLOR_SENSOR_L.color())
            robot.drive(100,0)
            wait(100)

def DRIVE_UNTIL_RED(): # 직진, 빨간색 발견시 정지
    while COLOR_SENSOR_L.color() != Color.RED: 
        robot.drive(100,0)
        wait(100)

def DEFINE_ID(): # 물체인식 ID 1:포카리 2:삼다수 3:실패

    while True:
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ULTRASONIC_SENSOR.distance())
            wait(100)
            BREAK_POINT = 0 
            if BREAK_POINT == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수",ULTRASONIC_SENSOR.distance())
            BREAK_POINT = 0
            if BREAK_POINT == 0:
                break
        elif BREAK_POINT == 0:
                break
        else:
            print("인식실패",ULTRASONIC_SENSOR.distance())

def RETURN(): # 물체인식 후 되돌아 가기 제자리에 갖다 놓기

## 1번 ###########################################

Grab(-200)  # grab open

while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

while ultra.distance() > 115:  # 초음파 센서 거리 감지 
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(80)

Grab(200)  # grab close

robot.stop()

Turn(190)  # 180도 턴

if ID == 1:  # 포카리
    print("포카리로 감")
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())
    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())
    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())
    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    
    robot.straight(50)
    Turn(100)

## 2번 ###########################################
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

while ULTRASONIC_SENSOR.distance() > 115:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD)
    robot.drive(100,rate)
    wait(80)

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(80)

Grab(200)  # grab close

robot.stop()

Turn(190)  # 180도 턴

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

robot.straight(50)

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

if ID == 1:  # 포카리   
    print("포카리로 감")
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

    robot.straight(50)
    Turn(100)

if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()

## 3번
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())
robot.straight(50)
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())
robot.straight(50)
while ultra.distance() > 115:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD
)
    robot.drive(100,rate)
    wait(80)

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(80)

Grab(200)  # grab close

robot.stop()

Turn(190)  # 180도 턴

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())
robot.straight(50)
while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())
robot.straight(50)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 5번
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

robot.straight(20)
robot.stop()
Turn(100)

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())
    print("reflection")

while ultra.distance() > 130:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD
)
    robot.drive(100,rate)
    print(ultra.distance())
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(100)
Grab(200)  # grab close
robot.stop()
Turn(190)  # 180도 턴

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(30)
robot.stop()
Turn(-100)

if ID == 1:  # 포카리
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 6번
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

robot.straight(50)

while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD
)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(100)
Grab(200)  # grab close
robot.stop()
Turn(190)  # 180도 턴

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 7번
while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

while COLOR_SENSOR_R.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

robot.straight(50)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN
,COLOR_SENSOR_L.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD
)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = HUSKYLENS.get_blocks()
    if len(blocks) > 0:
        ID  = blocks[0].ID
        wait(100)
        if ID == 1:
            ev3.speaker.beep()
            print("포카리",ultra.distance())
            wait(100)
            BP = 0 
            if BP == 0:
                break
        elif ID == 2:
            ev3.speaker.beep()
            wait(100)
            print("삼다수")
            BP = 0
            if BP == 0:
                break
        else:
                print("인식실패",ultra.distance())
        if BP == 0:
                break

robot.straight(120)
Grab(200)  # grab close
robot.stop()
Turn(190)  # 180도 턴

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)  # 바이패스

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PROPORTIONAL_GAIN
,COLOR_SENSOR_R
.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-90)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while COLOR_SENSOR_R
.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PROPORTIONAL_GAIN
    ,COLOR_SENSOR_L.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while COLOR_SENSOR_L.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(COLOR_SENSOR_L.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)
    Turn(-100)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())

    robot.straight(50)  #  바이패스

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN
    ,COLOR_SENSOR_R
    .reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()
robot.straight(-200)