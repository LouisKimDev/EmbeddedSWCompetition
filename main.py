#!/usr/bin/env pybricks-micropython

# Version_1.00
# Author : 은대영


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


##############################################################
##  상수 설정값 setting  ##
# Reference #
#  Black = 9  도윤 15
#  White = 60  도윤 60
#  threshold = (B+W) / 2  고정
#  DRIVE_SPEED = 100
#  PG(Proportional_gain) = 1.2  도윤 1.3
#  G(gain) = 0.8  고정
#  RV(Reflection valuable) = 30  반사광 광도 
#  BREAK_POINT = 1
#  robot.settings(0,0,0,0) = (strait속도,strait가속도,turn속도,turn가속도)
#  BYPASS = 50  바이패스 거리
#  OPEN = Grap open = -200
#  CLOSE = Grap close = 200
#  Distance = 115  물체 감지 거리
B = 10
W = 70
threshold = (B+W) / 2
DRIVE_SPEED = 250
PG = 1.5
G = 0.8
RV = 40
BREAK_POINT = 1
robot.settings(300,400,300,400)
BYPASS = 50
OPEN = -300 
CLOSE = 300
Distance = 115
##############################################################


#######  Function List  ######################################
# Reference #

##  Grap OPEN & CLOSE  ## 
# duty_limit = 50
def Grap(grep):
    grab_motor.run_until_stalled(grep, then = Stop.COAST, duty_limit=150)


##  Line tracing  ##
def Reflection(g, reflect):  #  왼쪽 or 오른쪽라인 보정, 오른쪽 센서를 사용할 때는 -PG 보정 필요
    deviation = reflect - threshold
    turn_rate = g * deviation
    robot.drive(DRIVE_SPEED, turn_rate)
    wait(100)

def Follow_left():  #  Follow left line 왼쪽 추적하여 직진 / 오른쪽 완전히 Black 감지 시 정지
    while csR.reflection() > RV:
        Reflection(PG,csL.reflection())

def Follow_right():  #  Follow Right line, 오른쪽 추적하여 직진 / 왼쪽 완전히 Black 감지 시 정지
    while csL.reflection() > RV:
        Reflection(-PG,csR.reflection())

def Follow_left_line(bypass_limit):  #  parameter(bypass_limit)만큼 오른쪽 Black 감지 시 무시
    bypass_counter = 0
    if (bypass_limit == 0):  # Follow_left와 동일
        Follow_left()
    while bypass_counter != (bypass_limit + 1):  # bypass_counter가 bypass_limit과 같으면 정지
        if ((csR.reflection() > RV) and (ultra.distance() > Distance)):  # 아래가 흰색이고 앞에 장애물 X 일때
            Reflection(PG,csL.reflection())  # 직진 
        elif ((csR.reflection() < RV) and (ultra.distance() > Distance)):  # 아래가 검은색, 앞에 장애물 X 일때
            bypass_counter = bypass_counter +1  # bypass_counter 1 증가
            print("---------------")
            print("Bypass: ",bypass_counter)
            print("Color : ",csR.reflection())
            print("---------------")
            wait(200)
            Reflection(PG,csL.reflection())  # 직진

def Follow_right_line(bypass_limit):  #  parameter(bypass_limit)만큼 왼쪽 Black 감지 시 무시
    bypass_counter = 0
    if (bypass_limit == 0):  # Follow_right와 동일
        Follow_right()
    while bypass_counter != (bypass_limit + 1):  # bypass_counter가 bypass_limit과 같으면 정지
        if ((csL.reflection() > RV) and (ultra.distance() > Distance)):  # 아래가 흰색이고 앞에 장애물 X 일때
            Reflection(PG,csR.reflection())  # 직진 
        elif ((csL.reflection() < RV) and (ultra.distance() > Distance)):  # 아래가 검은색, 앞에 장애물 X 일때
            bypass_counter = bypass_counter +1  # bypass_counter 1 증가
            print("---------------")
            print("Bypass: ",bypass_counter)
            print("Color : ",csL.reflection())
            print("---------------")
            wait(200)
            Reflection(-PG,csR.reflection())  # 직진


##  Turn  ##
def Turn(degree):
    robot.turn(degree)


##  Object detect and stop  ##
#  초음파 센서 거리 감지
def Find_object_left():  #  Find object by left sensor
    while ultra.distance() > Distance:
        rate = G * (csL.reflection() - threshold)
        robot.drive(DRIVE_SPEED,rate)
        wait(50)

def Find_object_right():  #  Find object by right sensor
    while ultra.distance() > Distance:
        rate = G * (csR.reflection() - threshold)
        robot.drive(DRIVE_SPEED,rate)
        wait(50)


##  Object define by huskylens  ##
#  허스키 렌즈로 물체 인식
def Define_ID():  #  ID=1:포카리  ID=2:삼다수  ID=3:실패
    while True:
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
                print("삼다수",ultra.distance())
                BP = 0
                if BP == 0:
                    break
            else:
                print("인식 실패",ultra.distance())
            if BP == 0:
                break


##  Detect Colour  ##
def Detect_blue(): # 직진, 파란색 발견시 정지
    while COLOR_SENSOR_L.color()!= Color.BLUE:  
        print("Find",COLOR_SENSOR_L.color())
        robot.drive(DRIVE_SPEED,0)
        wait(100)

def Detect_red(): # 직진, 빨간색 발견시 정지
    while COLOR_SENSOR_L.color() != Color.RED:
        print("Find",COLOR_SENSOR_L.color()) 
        robot.drive(DRIVE_SPEED,0)
        wait(100)


##  Distribute from node 1  ##
# test 이후 수정 필요
def Go_1():  #  Red 감지 시 정지 후 그랩 오픈
    Follow_right()
    Turn(-95)
    
    Follow_left()
    Turn(95)

    Follow_left()
    wait(800)

    Detect_red()
    Grap(OPEN)

def Go_2():  #  Blue 감지 시 정지 후 그랩 오픈
    Follow_right()
    Turn(-95)
    
    Follow_left_line(1)
    Turn(95)
    
    Follow_left()
    wait(800)
    
    Detect_blue()
    Grap(OPEN)


##  Return route from node 1  ##
# <Test 이후 수정 필요>
def Return_1():  # 포카리 배달 이후 Node 1 복귀
    wait(100)
    robot.straight(-120)
    Turn(195)
    FR()
    Turn(-95)
    FR()
    Turn(95)
    FL()

def Return_2():  # 삼다수 배달 이후 Node 1 복귀
    wait(100)
    robot.straight(-120)
    Turn(195)
    FR()
    Turn(-95)
    FR()
    robot.straight(50)
    FR()
    Turn(95)
    FL()
##############################################################


############ START ###########################################

##### Node 1 #####

# Node 1 Check
if ultra.distance() > 700:  # Node 1 물건 X
    print("Node 1 NO! 최초거리 :",ultra.distance())

    robot.straight(180)
    Follow_left_line(1)
    Turn(95)
    robot.stop()

    # Node 5 Check
    if ultra.distance() > 400:  # Node 5 물건 O
        print("Node 5 NO! 최초거리 :",ultra.distance())

        Follow_right_line(1)
        Find_object_right()
        Define_ID()
        robot.stop()

        Grap(CLOSE)
        robot.stop()
        Turn(190)

        Follow_left_line(1)
        Turn(-95)
        robot.stop()

        # Node 9 Check
        if ultra.distance() > 800:  # Node 9 물건 X --> Node 2
            print("Node 9 NO! 최초거리 :",ultra.distance())
            Turn(-95)
        else  # Node 9 물건 O
            print("Node 9 OK! 최초거리 :",ultra.distance())

            Follow_right_line(1)
            Find_object_right()
            Define_ID()
            robot.stop()

            Grap(CLOSE)
            robot.stop()
            Turn(190)

            Follow_left_line(1)
            Turn(-95)
            robot.stop()

            # 배치 & 복귀
            if ID == 1:
                Go_1()
                Return_1()
            elif ID == 2:
                Go_2()
                Return_2()
    else  # Node 5 물건 O
        print("Node 5 OK! 최초거리 :",ultra.distance())

        Follow_right_line(1)
        Find_object_right()
        Define_ID()
        robot.stop()

        Grap(CLOSE)
        robot.stop()
        Turn(190)

        Follow_left()
        Turn(-95)
        # 배치 & 복귀
        if ID == 1:
            Go_1()
            Return_1()
        elif ID == 2:
            Go_2()
            Return_2()
elif ultra.distance() < 700:  # Node 1 물건 O
    print("Node 1 OK! 최초거리 :",ultra.distance())

    Follow_left_line(1)
    Find_object_left()
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()
    Turn(190)

    # 배치 & 복귀
    if ID == 1:
        Go_1()
        Return_1()
    elif ID == 2: 
        Go_2()
        Return_2()
    
Turn(95)
robot.stop()



##############################################################
##### Renew

# Node 1 Check
if ultra.distance() < 700:  # Node 1 물건 O
    print("Node 1 OK! 최초거리 :",ultra.distance())

    Follow_left_line(1)
    Find_object_left()
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()
    Turn(190)

    if ID == 1:  # 포카리
        Go_1()
        Return_1()
    elif ID == 2:  # 삼다수 
        Go_2()
        Return_2()
    
    # Node 1 복귀 완료
elif ultra.distance() > 700:  # Node 1 물건 X
    print("Node 1 NO! 최초거리 :",ultra.distance())

    Follow_left_line(1)
    robot.stop()


# Node 5 Check
Turn(95)
robot.stop()
wait(1000)

if ultra.distance() < 400:  # Node 5 물건 O
    print("Node 5 NO! 최초거리 :",ultra.distance())

    Follow_right_line(1)
    Find_object_right()
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()
    Turn(190)

    Follow_left_line(1)
    Turn(-95)
    robot.stop()

    if ID == 1:  # 포카리
        Go_1()
        Return_1()
        Turn(95)
    elif ID == 2:  # 삼다수 
        Go_2()
        Return_2()
        Turn(95)
    
    # Node 1 복귀 완료
elif ultra.distance() > 400:  # Node 5 물건 X
    print("Node 5 NO! 최초거리 :",ultra.distance())

# Node 9 Check
if ultra.distance() > 800:  # Node 9 물건 X --> Node 2
    print("Node 9 NO! 최초거리 :",ultra.distance())
    Turn(-95)
else  # Node 9 물건 O
    print("Node 9 OK! 최초거리 :",ultra.distance())

    Follow_right_line(1)
    Find_object_right()
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()
    Turn(190)

    Follow_left_line(1)
    Turn(-95)
    robot.stop()

    # 배치 & 복귀
    if ID == 1:
        Go_1()
        Return_1()
    elif ID == 2:
        Go_2()
        Return_2()









    






### Node 2 ###



### Node 3 ###