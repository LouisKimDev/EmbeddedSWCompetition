#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pyhuskylens import *

ev3 = EV3Brick()
grab_motor = Motor(Port.C)
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)
robot = DriveBase(left_motor,right_motor,55.5,104)
csL = ColorSensor(Port.S1)
csR = ColorSensor(Port.S2)
h1 = HuskyLens(Port.S3, debug=False)
ultra = UltrasonicSensor(Port.S4) 
ev3.speaker.beep()


def Grab(grep):  # grab open & close
    grab_motor.run_until_stalled(grep, then = Stop.COAST, duty_limit=50)

def Reflection(g, reflect):  # 왼쪽라인 or 오른쪽라인 보정 / 오른쪽 센서일때 -PG 보정 필요
    deviation = reflect - threshold
    turn_rate = g * deviation
    robot.drive(DRIVE_SPEED, turn_rate)
    wait(100)

def Turn(degree):
    robot.turn(degree)

B = 7  # Black 
W = 60  # White
threshold = (B+W) / 2
DRIVE_SPEED = 100
PG = 1.2  # Proportional_gain
G = 0.8  # gain
RV = 30  # Reflection valuable
BP = 1


Grab(-200)  # grab open


## 1번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

while ultra.distance() > 115:  # 초음파 센서 거리 감지 
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

## 2번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

while ultra.distance() > 115:  # 초음파 센서 거리 감지
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    wait(80)

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

if ID == 1:  # 포카리   
    print("포카리로 감")
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()

## 3번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())
robot.straight(50)
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())
robot.straight(50)
while ultra.distance() > 115:  # 초음파 센서 거리 감지
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    wait(80)

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())
robot.straight(50)
while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())
robot.straight(50)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 5번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

robot.straight(20)
robot.stop()
Turn(100)

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())
    print("reflection")

while ultra.distance() > 130:  # 초음파 센서 거리 감지
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    print(ultra.distance())
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(30)
robot.stop()
Turn(-100)

if ID == 1:  # 포카리
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 6번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

robot.straight(50)

while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 7번
while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

robot.straight(50)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PG,csL.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (csL.reflection() - threshold)
    robot.drive(100,rate)
    wait(80)

robot.stop()

while True:  # 물체인식 ID 1:포카리 2:삼다수 3:실패
    blocks = h1.get_blocks()
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

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)  # 바이패스

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)
robot.stop()
Turn(100)

while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
    Reflection(-PG,csR.reflection())

robot.straight(50)
robot.stop()
Turn(-100)

if ID == 1:  # 포카리   
    print("포카리로 감")
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color() != Color.RED:  # 직진, 빨간색 발견시 정지
        robot.drive(100,0)
        wait(100)

    wait(500)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    wait(500)
    
    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-90)

    while csL.reflection() > RV:  # 직진 오른쪽 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(100)
if ID == 2 : # 삼다수
    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    robot.straight(50)
    robot.stop()
    Turn(-100)

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)  ## 바이패스 초기값 80

    while csR.reflection() > RV:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
        Reflection(PG,csL.reflection())

    robot.straight(50)
    robot.stop()
    Turn(100)

    while csL.color()!= Color.BLUE:  # 직진, 파란색 발견시 정지
        print(csL.color())
        robot.drive(100,0)
        wait(100)
    robot.straight(100)
    robot.stop()

    Grab(-200)  # grap open

    robot.straight(-100)
    Turn(-190)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)
    Turn(-100)

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())

    robot.straight(50)  #  바이패스

    while csL.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PG,csR.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()
robot.straight(-200)