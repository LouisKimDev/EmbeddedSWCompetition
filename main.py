#!/usr/bin/env pybricks-micropython

# Version_1.20 / 2022-11-13
# Author : 은대영/ 김도윤

# V_1.30 변경사항
# Back(4) 함수 변경 및 추가

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

#################  상수 설정값 setting  #######################
##  상수 설정값 setting  ##
# Reference #
#  Black = 9  7  /  8
#  White = 60  53 /  63
#  threshold = (B+W) / 2  고정
#  DRIVE_SPEED = 100
#  PG(Proportional_gain) = 1.0
#  G(gain) = 0.8  고정
#  RV(Reflection valuable) = 30  반사광 광도 
#  BP(BREAK_POINT) = 1
#  robot.settings(0,0,0,0) = (strait속도,strait가속도,turn속도,turn가속도)
#  BYPASS = 50  바이패스 거리
#  OPEN = Grap open = -200
#  CLOSE = Grap close = 200
#  Distance = 115  물체 감지 거리
#  Node = 노드 카운트용
B = 8
W = 63 
threshold = (B+W) / 2
DRIVE_SPEED = 280
PG = 0.8
G = 0.8
RV = 30
BP = 1
robot.settings(400,600,800,1000)
BYPASS = 50
OPEN = -150
CLOSE = 300
Distance = 125
Node = 0
#######  Function List  ######################################
##  Function name  ##
#  Instruction #
# Reference #


##  Grap OPEN & CLOSE  ## 
# duty_limit = 50
def Grap(grep):  # grep에 OPEN or CLOSE 입력
    grab_motor.run_until_stalled(grep, Stop.COAST, 200)


##  Line tracing  ##
def Reflection(g, reflect):  # 왼쪽 or 오른쪽라인 보정, 오른쪽 센서를 사용할 때는 -PG 보정 필요
    deviation = reflect - threshold
    turn_rate = g * deviation
    robot.drive(DRIVE_SPEED, turn_rate)
    wait(10)

def Follow_left():  # Follow left line 왼쪽 추적하여 직진 / 오른쪽 완전히 Black 감지 시 정지
    while csR.reflection() > RV:
        Reflection(PG,csL.reflection())

def Follow_left_by(speedo):  # Follow left by manual / parameter(speedo)로 속도 조절
    while csR.reflection() > RV:
        deviation = csL.reflection() - threshold
        turn_rate = PG * deviation
        robot.drive(speedo, turn_rate)
        wait(10)

def Follow_right():  #  Follow Right line, 오른쪽 추적하여 직진 / 왼쪽 완전히 Black 감지 시 정지
    while csL.reflection() > RV:
        Reflection(-PG,csR.reflection())
        
def Follow_right_by(speedo):  # Follow right by manual / parameter(speedo)로 속도 조절
    while csL.reflection() > RV:
        deviation = csR.reflection() - threshold
        turn_rate = -PG * deviation
        robot.drive(speedo, turn_rate)
        wait(10)
#  현재 Bypass 함수의 즉각적인 feedback이 늦어 사용을 제한해야 함
def Bypass_do_not_use():  # 안에 설명 있음
    print("Not yet")
    # Bypass 이후 Turn을 해야 할 경우 필요한 구간은 Bypass 함수 사용 대신 다음 예시를 따를 것
    
    # ex) 1칸을 bypass 해야 할 경우
    
    # Follow_left()
    # wait(150)                                  <- 바이패스와 같은 역할, 0.15초 이후에 완전히 검은라인 벗어남
    # Follow_left() or Follow_left_by(speed)     <- 다음 라인에서 멈춤
    
    # Turn_L/R(speed,time)

def Follow_left_line(bypass_limit):  # parameter(bypass_limit)만큼 오른쪽 Black 감지 시 무시
    bypass_counter = 0
    if bypass_limit == 0:  # Follow_left와 동일
        Follow_left()
    else:
        while bypass_counter != bypass_limit + 1:  # bypass_counter가 bypass_limit과 같으면 정지
            if ((csR.reflection() > RV) and (ultra.distance() > Distance)):  # 아래가 흰색이고 앞에 장애물 X 일때
                Reflection(PG,csL.reflection())  # 직진
            elif ((csR.reflection() < RV) and (ultra.distance() > Distance)):  # 아래가 검은색, 앞에 장애물 X 일때
                bypass_counter = bypass_counter + 1  # bypass_counter 1 증가
                print("---------------")
                print("Bypass: ",bypass_counter)
                print("Color : ",csR.reflection())
                print("---------------")
                wait(150)
                Reflection(PG,csL.reflection())  # 직진

def Follow_right_line(bypass_limit):  #  parameter(bypass_limit)만큼 왼쪽 Black 감지 시 무시 
    bypass_counter = 0
    if (bypass_limit == 0):  # Follow_right와 동일
        Follow_right()
    else:
        while bypass_counter != bypass_limit + 1:  # bypass_counter가 bypass_limit과 같으면 정지
            if ((csL.reflection() > RV) and (ultra.distance() > Distance)):  # 아래가 흰색이고 앞에 장애물 X 일때
                Reflection(-PG,csR.reflection())  # 직진
            elif ((csL.reflection() < RV) and (ultra.distance() > Distance)):  # 아래가 검은색, 앞에 장애물 X 일때
                bypass_counter = bypass_counter + 1  # bypass_counter 1 증가
                print("---------------")
                print("Bypass: ",bypass_counter)
                print("Color : ",csL.reflection())
                print("---------------")
                wait(150)
                Reflection(-PG,csR.reflection())  # 직진


##  Turn  ##
#  회전 함수
def Turn(degree):  # 제자리에서 회전, degree만큼 회전 / 90도 회전 시 5~10도 더 줄것
    robot.turn(degree)

def Turn_L(turn, timee):  # turn 만큼 회전, timee만큼 회전시간 조정
    robot.drive(0,-turn)  # -90도
    wait(timee)

def Turn_R(turn, timee):  # turn 만큼 회전, timee만큼 회전시간 조정
    robot.drive(0,turn)  # 90도
    wait(timee)

def Turn_LL(rotate_speed,revolution):  # 한쪽 바퀴만 굴려서 회전 parameter: (회전속도,바퀴 회전수)
    Turn(0)
    robot.stop()
    right_motor.run_angle(rotate_speed, revolution, Stop.BRAKE, True)  # Stop.BRAKE(역제동토크) or Stop.COAST(부드럽게)

def Turn_RR(rotate_speed,revolution):  # 한쪽 바퀴만 굴려서 회전 parameter: (회전속도,바퀴 회전수)
    Turn(0)
    robot.stop()
    left_motor.run_angle(rotate_speed, revolution, Stop.BRAKE, True)  # Stop.BRAKE(역제동토크) or Stop.COAST(부드럽게))


##  Object detect and stop  ##
#  초음파 센서로 거리 감지하여 정지, 감지하는 동안 Line tracing 작동됨
def Find_object_left():  #  Find object by left sensor
    while ultra.distance() > Distance:
        rate = G * (csL.reflection() - threshold)
        robot.drive(DRIVE_SPEED, rate)
        wait(100)

def Find_object_right():  #  Find object by right sensor
    while ultra.distance() > Distance:
        rate = -G * (csR.reflection() - threshold)
        robot.drive(DRIVE_SPEED, rate)
        wait(100)

def Find_object_left_by(speedo):  #  Find object by left sensor by manual / speedo로 속도 조절
    while ultra.distance() > Distance:
        rate = G * (csL.reflection() - threshold)
        robot.drive(speedo, rate)

def Find_object_right_by(speedo):  #  Find object by right sensor by manual / speedo로 속도 조절
    while ultra.distance() > Distance:
        rate = -G * (csR.reflection() - threshold)
        robot.drive(speedo, rate)


##  Object define by huskylens  ##
#  허스키 렌즈로 물체 인식
def Define_ID():  #  ID=1:포카리  ID=2:삼다수  ID=3:실패
    global ID
    while True:
        ID = h1.get_blocks()[0].ID
        while(ID==0):
            ID = h1.get_blocks()[0].ID
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
#  Red or Blue 존 진입시 색 판단용 함수
def Detect_blue_L(): # 직진, 왼쪽 센서 사용, 파란색 발견시 정지
    while csL.color()!= Color.BLUE:
        print("Find",csL.color())
        robot.drive(250,0)
        wait(100)

def Detect_blue_R(): # 직진, 오른쪽 센서 사용, 파란색 발견시 정지
    while csR.color()!= Color.BLUE:
        print("Find",csR.color())
        robot.drive(250,0)
        wait(100)

def Detect_red_L(): # 직진, 왼쪽 센서 사용, 빨간색 발견시 정지
    while csL.color() != Color.RED:
        print("Find",csL.color())
        robot.drive(250,0)
        wait(100)

def Detect_red_R(): # 직진, 오른쪽 센서 사용, 빨간색 발견시 정지
    while csR.color() != Color.RED:
        print("Find",csR.color())
        robot.drive(250,0)
        wait(100)


##  Distribute from intersection  ##
# 삼거리에서 빨강, 파랑으로 분배함
def Back(number):  
    # number = 1: 1번 라인 / number = 2: 5번 라인 / number = 3: 3번 라인
    # number = 4: 1번 라인 Turn_LL/RR 사용

    if number == 1:  # 1번 라인
        
        if ID == 1:  # 포카리

            Turn_L(250,400)  # 삼거리, 복귀할 때 속도 280 기준

            Follow_left_by(250)

            Turn_R(150,600)  # 속도 150에서 올리다가 실패, 150 고정

            Follow_left_by(200)  # Red zone 진입
            wait(200)

            Detect_red()
            robot.stop()
            wait(200)
            Grap(OPEN)

            robot.straight(-320)  # 후진

            Turn(100)

            Follow_left()

            Turn_R(150,700)  # 삼거리, 150에서 올리다가 실패, 150 고정

            Follow_left_by(200)
            wait(150)

            #Turn(0)  # Node 1

        elif ID == 2:  # 삼다수

            Turn_L(250,400)  # 삼거리, 복귀할 때 속도 280 기준

            Follow_left()
            wait(150)
            Follow_left_by(250)

            Turn_R(200,510)

            Follow_left_by(200)  # Blue zone 진입
            wait(200)

            Detect_blue()
            robot.stop()
            wait(200)
            Grap(OPEN)

            robot.straight(-320)  # 후진

            Turn(100)

            Follow_left()
            wait(150)
            Follow_left()

            Turn_R(150,710)  # 삼거리

            Follow_left_by(200)
            wait(150)

            #Turn(0)  # Node 1

    elif number == 2:  # 5번 라인
        
        if ID == 1:     # 포카리
            
            robot.straight(250)     # 2번 삼거리 복귀

            Follow_right_by(220)     # Red zone 앞

            Detect_red_R()          # Red 감지
            wait(400)
            Turn(0)
            Grap(OPEN)

            robot.straight(-80)     # 후진
            Turn(-195)               # 회전

            Follow_left()          # csL colour -> reflection swith
            wait(100)               # csL colour -> reflection swith        

            Follow_left_by(200)    # Node 5로 전진
            wait(200)
            Turn(0)

            robot.straight(250)
            
            wait(150)
            Turn(0)
            robot.stop()

        elif ID == 2:   # 삼다수

            robot.straight(230)     # 2번 삼거리 복귀

            Turn_LL(1000,360)       # 좌회전

            Follow_left_by(300)

            Turn_RR(1000,360)       # 우회전

            Follow_right_by(280)    # Blue zone 진입

            Detect_blue_L()         # Blue 감지
            Turn(0)
            Grap(OPEN)
            
            robot.straight(-300)    # 후진

            Turn_RR(1000,360)

            Follow_right()          # csL colour -> reflection swith
            wait(50)                # csL colour -> reflection swith

            Follow_right_by(300)
            Turn(0)                 # 2번 삼거리, 정지
            robot.straight(-20)

            Turn_RR(1000,360)       # 우회전
            wait(100)

            robot.straight(250)
            
            wait(100)
            Turn(0)                 # Node 5에서 정지
            robot.stop()

    elif number == 3:  # 9번 라인
        
        if ID == 1: # 포카리

            robot.straight(270)     # 3번 삼거리 복귀

            Turn(100)               # 우회전

            Follow_right_by(300) 
            Turn(0)

            Turn_LL(1000,360)       # Red zone 앞 좌회전

            Follow_left()           # Red Zone 진입

            Detect_red_R()
            Turn(0)
            Grap(OPEN)

            robot.straight(-280)    # 후진

            Turn_LL(1000,360)

            Follow_left()           # csR switch 
            wait(50)                # csR switch 

            Follow_left_by(250)     # 3번 삼거리 복귀
            wait(150)
            Turn(0)                 # 3번 삼거리 정지

            Turn(-100)              # 좌회전 

            robot.straight(250)

            wait(150)
            Turn(0)                             # Node 9 복귀

        elif ID == 2 : # 삼다수

            robot.straight(270)     # 3번 삼거리 복귀

            Follow_left_by(200)

            Detect_blue_R()          # Blue 감지
            Turn(0)
            Grap(OPEN)

            robot.straight(-80)     # 후진
            Turn(200)               # 회전

            Follow_right_by(200)
            wait(200)
            Turn(0)

            robot.straight(250)

    elif number == 4:  # 1번 라인 Turn_LL/RR 사용
    
        if ID == 1:  # 포카리

            Turn(0)
            Turn_LL(1000,360)  # 삼거리, 좌회전

            Follow_left_by(300)

            Turn_RR(1000,360)  # 우회전

            Follow_right_by(350)  # Red zone 진입

            Detect_red_L()
            Turn(0)
            Grap(OPEN)

            robot.straight(-300)    # 후진

            Turn_RR(1000,360)

            Follow_right()          # csL colour -> reflection swith
            wait(150)               # csL colour -> reflection swith

            Follow_right_by(300)
            wait(100)
            Turn(0)                 # 삼거리, 정지

            Turn(100)               # 우회전

            Follow_left_by(250)
            wait(250)               # Node 1에서 정지
            Turn(0)

        elif ID == 2:   # 삼다수

            Turn(0)
            Turn_LL(1000,360)       # 삼거리, 좌회전 / 복귀할 때 속도 280 기준

            Follow_left_by(350)
            wait(150)               # 한줄 바이패스
            Follow_left_by(300)

            Turn_RR(1000,360)       # 우회전

            Follow_right_by(350)    # Blue zone 진입

            Detect_blue_L()
            Turn(0)
            Grap(OPEN)

            robot.straight(-300)    # 후진

            Turn_RR(1000,360)

            Follow_right()          # csL colour -> reflection swith
            wait(150)               # csL colour -> reflection swith

            Follow_right_by(350)
            wait(150)
            Follow_right_by(300)
            wait(100)
            Turn(0)                 # 삼거리, 정지

            Turn(100)               # 우회전

            Follow_left_by(250)
            wait(250)               # Node 1에서 정지
            Turn(0)

######################  TEST ZONE  ###########################
# 일정 구간에서 실행 안되는 것들 여기다 넣어서 먼저 테스트

#wait(50000)
########################  START  #############################
Grap(OPEN)
print("Proseed to 1st Sequence at start point")
print("")
##############################################################

#  Node 1 check at start point
print("Node 1 Check... Initial distance :", ultra.distance())
print("")
if ultra.distance() < 700:  # Node 1 Ok in start point
    print("Node 1 First detect! Distance :", ultra.distance())
    print("")
    Node = 1

    # 1번 노드 실행
    robot.drive(260,0)
    wait(1200)

    Follow_left_by(230)     # 삼거리 passing
    Find_object_left_by(220)# 물체 감지
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()

    Turn(-190)

    Follow_right_by(350)    # 삼거리로 복귀
    Turn(0)                 # 삼거리 정지

    Back(4)                 # 분배 후 Node 1 복귀

    print("Node 1 Clear!")
    print("")
else:  # Move to node 1
    print("Node 1 Undetect! Distance :", ultra.distance())
    print("")
    print("Move to node 1")
    print("")
    Node = -1

    robot.drive(260,0)
    wait(1200)

    Follow_left_by(230)     # 초기 안정성을 위한 감속 1
    wait(150)               # 삼거리 passing

    Follow_left_by(250)     # Node 1으로 전진
    wait(250)            

    Turn(0)                 # Node 1 정지 & 관측

wait(200)

# Node 2 check in node 1
if ultra.distance() < 500:  # Node 2 check
    print("Node 2 Detect! Distance :", ultra.distance())
    print("")
    Node = 2

    # 2번 노드 실행
    Find_object_left_by(220)# Node 2 바로 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()

    Turn(-190)

    Follow_right_by(350)
    wait(150)               # Node 1 passing

    Follow_right_by(300)    # 삼거리로 복귀
    Turn(0)                 # 삼거리 정지

    Back(4)                 # 분배 후 Node 1 복귀

    print("Node 2 Clear!")
    print("")
else:  # Node 2 X  Node 3 check
    print("Node 2 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 3 Check...")
    print("")

# Node 3 check in node 1
if ultra.distance() < 900:  # Node 3 check
    print("Node 3 Detect! Distance :", ultra.distance())
    print("")
    Node = 3

    # 3번 노드 실행
    Follow_left_by(350)
    wait(150)               # Node 2 passing

    Find_object_left_by(250)# Node 3 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()

    Turn(-190)              # 180 Turn

    Follow_right_by(350)
    wait(150)               # Node 2 passing

    Follow_right_by(350)
    wait(150)               # Node 1 passing

    Follow_right_by(300)    # 삼거리로 전진
    Turn(0)                 # 삼거리 정지

    Back(4)

    print("Node 3 Clear!")
    print("")
else:  # Node 3 X  Node 4 check
    print("Node 3 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 4 Check...")
    print("")

# Node 4 check in node 1
if ultra.distance() < 1300:  # Node 4 check
    print("Node 4 Detect! Distance :", ultra.distance())
    print("")
    Node = 4

    # 4번 노드 실행
    Follow_left_by(350)
    wait(150)               # Node 2 passing

    Follow_left_by(300)     # Node 3 전 감속
    wait(150)

    while ultra.distance() > 170:
        robot.drive(230,0)

    Define_ID()
    Turn(0)

    Grap(CLOSE)

    robot.straight(-350)    # 후진
    Turn(-195)              # 180도 회전

    Follow_right_by(300)
    wait(150)               # Node 2 passing

    Follow_right_by(350)
    wait(100)               # Node 1 passing

    Follow_right_by(300)    # 삼거리로 전진, 감속
    Turn(0)

    Back(4)

    print("Node 4 Clear!")
    print("")
else:  # Node 4 X, Move to node 5
    print("Node 4 Undetect! Distance :", ultra.distance())
    print("")
    print("All clear and proseed to 2nd Sequence at node 5")
    print("")

print("Proseed to 2nd Sequence at node 5")
print("")

# Proseed to 2nd Sequence in node 5

print("Turn in node 1")
print("")

Turn(0)
Turn(100)                       # Node 5로 Turn

print("Node 5 check... Distance :", ultra.distance())
# Node 5 check in node 1
if ultra.distance() < 400:  # Node 5 OK in 2nd intersection
    print("Node 5 Detect! Distance :", ultra.distance())
    print("")
    Node = 5

    # 5번 노드 실행
    while ultra.distance() > 80:        # Find_object_right()
        rate = -G * (csR.reflection() - threshold)
        robot.drive(220, rate)
    Turn(0)                             # 정지

    Define_ID()                         # 판별
    
    robot.straight(50)                  # 소폭 전진

    Grap(CLOSE)

    Follow_right_by(250)                # Node 5 정렬
    wait(200)
    Turn(0)

    Turn(100)                           # 우회전

    Back(2)

    print("Node 5 Clear!")
    print("")
else:
    print("Node 5 Undetect! Distance :", ultra.distance())
    print("")
    Follow_right()
    Turn(0)

    robot.straight(60)
    Turn(-100)
    robot.stop()

wait(200)

print("Node 6 check... Distance :", ultra.distance())
print("")
# Node 6 check in node 5
if ultra.distance() < 400:  # Node 6 check
    print("Node 6 Detect! Distance :", ultra.distance())
    print("")
    Node = 6

    # 6번 노드 실행
    Find_object_left_by(230)    # Node 6 바로 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    Turn(0)

    Turn(-190)

    Follow_right_by(230)        # Node 5로 복귀
    wait(150)
    Turn(0)                     # 삼거리 정지

    Back(2)                     # 분배 후 Node 1 복귀

    print("Node 6 Clear!")
    print("")
else:  # Node 6 X  Node 7 check
    print("Node 6 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 7 Check...")
    print("")

print("Node 7 check... Distance :", ultra.distance())
print("")
# Node 7 check in node 5
if ultra.distance() < 900:  # Node 7 check
    print("Node 7 Detect! Distance :", ultra.distance())
    print("")
    Node = 7

    # 7번 노드 실행
    Follow_left_by(300)
    wait(150)               # Node 5 passing

    Find_object_left_by(230)# Node 7 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()

    Turn(-190)              # 180 Turn

    Follow_right_by(300)
    wait(150)               # Node 6 passing

    Follow_right_by(300)     # Node 5로 전진
    wait(100)
    Turn(0)                 # Node 5 복귀

    Back(2)

    print("Node 7 Clear!")
    print("")
else:  # Node 7 X  Node 8 check
    print("Node 7 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 8 Check...")
    print("")

print("Node 8 check... Distance :", ultra.distance())
print("")
# Node 8 check in node 5
if ultra.distance() < 1300:  # Node 8 check
    print("Node 8 Detect! Distance :", ultra.distance())
    print("")
    Node = 8

    # 8번 노드 실행
    Follow_left_by(350)
    wait(150)               # Node 2 passing

    Follow_left_by(300)     # Node 3 전 감속
    wait(150)

    while ultra.distance() > 170:
        robot.drive(225,0)

    Define_ID()
    Turn(0)

    Grap(CLOSE)

    robot.straight(-325)    # 후진
    Turn(-195)              # 180도 회전

    Follow_right_by(300)
    wait(150)               # Node 6 passing

    Follow_right_by(300)
    wait(100)               # Node 5 passing
    Turn(0)                 # 2번 삼거리로 전진

    Back(2)

    print("Node 8 Clear!")
    print("")
else:  # Node 8 X, Move to node 9
    print("Node 8 Undetect! Distance :", ultra.distance())
    print("")
    print("All clear and proseed to 3rd Sequence at node 9")
    print("")

#robot.straight(20)      # 살짝 전진
Turn(100)

wait(200)

print("Node 9 check... Distance :", ultra.distance())
print("")
# Node 9 check in node 5
if ultra.distance() < 400:  # Node 6 check
    print("Node 9 Detect! Distance :", ultra.distance())
    print("")
    Node = 9

    # 9번 노드 실행
    while ultra.distance() > 80:        # Find_object_right()
        rate = -G * (csR.reflection() - threshold)
        robot.drive(220, rate)
    Turn(0)                             # 정지

    Define_ID()                         # 판별

    robot.straight(50)                  # 소폭 전진

    Grap(CLOSE)

    Follow_right_by(250)                # Node 5 정렬
    wait(160)
    Turn(0)

    Turn(100)                           # 우회전

    Back(3)                     # 분배 후 Node 9 복귀

    print("Node 9 Clear!")
    print("")
else:  # Node 9 X  Node 10 check
    print("Node 9 Undetect! Distance :", ultra.distance())
    print("")
    Follow_right()
    Turn(0)

    robot.straight(30)
    Turn(-100)
    robot.stop()

wait(200)

print("Node 10 check... Distance :", ultra.distance())
print("")
# Node 10 check in node 9
if ultra.distance() < 400:  # Node 10 check
    print("Node 10 Detect! Distance :", ultra.distance())
    print("")
    Node = 10

    # 10번 노드 실행
    Find_object_right_by(230)    # Node 10 바로 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    Turn(0)

    Turn(-190)

    Follow_left_by(250)        # Node 9로 복귀
    wait(150)
    Turn(0)                     # 삼거리 정지

    Back(3)                     # 분배 후 Node 9 복귀

    print("Node 10 Clear!")
    print("")
else:  # Node 10 X  Node 11 check
    print("Node 10 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 11 Check...")
    print("")

print("Node 11 check... Distance :", ultra.distance())
print("")
# Node 11 check in node 9
if ultra.distance() < 900:  # Node 11 check
    print("Node 11 Detect! Distance :", ultra.distance())
    print("")
    Node = 11

    # 11번 노드 실행
    Follow_right_by(300)
    wait(150)               # Node 10 passing

    Find_object_right_by(230)# Node 11 관측
    Define_ID()
    robot.stop()

    Grap(CLOSE)
    robot.stop()

    Turn(-190)              # 180 Turn

    Follow_left_by(300)
    wait(150)               # Node 10 passing

    Follow_left_by(300)     # Node 9로 전진
    wait(100)
    Turn(0)                 # Node 9 복귀

    Back(3)

    print("Node 11 Clear!")
    print("")
else:  # Node 11 X  Node 12 check
    print("Node 11 Undetect! Distance :", ultra.distance())
    print("")
    print("Node 12 Check...")
    print("")

print("Node 12 check... Distance :", ultra.distance())
print("")
# Node 12 check in node 9
if ultra.distance() < 1300:  # Node 12 check
    print("Node 12 Detect! Distance :", ultra.distance())
    print("")
    Node = 8

    # 12번 노드 실행
    Follow_right_by(350)
    wait(150)               # Node 10 passing

    Follow_right_by(300)     # Node 11 전 감속
    wait(150)

    while ultra.distance() > 170:
        robot.drive(225,0)

    Define_ID()
    Turn(0)

    Grap(CLOSE)

    robot.straight(-325)    # 후진
    Turn(-195)              # 180도 회전

    Follow_left_by(300)
    wait(150)               # Node 10 passing

    Follow_left_by(300)
    wait(100)               # Node 9 passing
    Turn(0)                 # 3번 삼거리로 전진

    Back(3)

    print("Node 12 Clear!")
    print("")
else:  # Node 12 X, Move to node 9
    print("Node 12 Undetect! Distance :", ultra.distance())
    print("")
    print("All clear and Back to Start line")
    print("")

print("그린 존으로 복귀")

Turn_LL(1000,360)

Follow_left_by(350) 
wait(150)               # Node 5 바이패스

Follow_left_by(300)     # Node 5 바이패스
Turn(0)

Turn_LL(1000,360)
wait(50)

Follow_left_by(400)
wait(470)
Turn(0)
