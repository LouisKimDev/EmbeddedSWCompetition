#!/usr/bin/env pybricks-micropython

#VERSION_1.01 : 코드 최적화, 변수 값, 로직은 조정 X
#AUTHOR : 김도윤

## 1번 ###########################################

Grab(GRAB_OPEN)  # grab open

Follow_left_line()

ULTRA_Distance()

robot.stop()

DEFINE_ID()

robot.straight(80)

Grab(GRAB_CLOSE)  # grab close

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
    robot.straight(BYPASS) 

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

## 2번 ###########################################

Follow_left_line()

ULTRA_Distance()

DEFINE_ID()

robot.straight(80)
Grab(GRAB_CLOSE)
robot.stop()

Turn(190)  # 180도 턴

Follow_right_line()

robot.straight(50)

Follow_right_line()

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
    robot.straight(BYPASS) 

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()

## 3번 ###########################################
Follow_left_line()

robot.straight(50)

Follow_left_line()

robot.straight(50)

ULTRA_Distance()

DEFINE_ID()

robot.straight(80)

Grab(GRAB_CLOSE)

robot.stop()

Turn(190)  # 180도 턴

Follow_left_line()

robot.straight(50)

Follow_right_line()

robot.straight(50)

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
    robot.straight(BYPASS)

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()

## 5번 ###########################################
Follow_left_line()

robot.straight(20)
robot.stop()
Turn(100)

Follow_right_line()

ULTRA_Distance()

robot.stop()

DEFINE_ID()

robot.straight(100)
Grab(GRAB_CLOSE)
robot.stop()
Turn(190)  # 180도 턴

Follow_right_line()

robot.straight(30)
robot.stop()
Turn(-100)

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
    robot.straight(BYPASS)

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()

## 6번 ###########################################
Follow_left_line()

robot.straight(50)

Follow_left_line()

robot.straight(50)
robot.stop()
Turn(100)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD)
    robot.drive(100,rate)
    wait(80)

robot.stop()

DEFINE_ID()

robot.straight(100)
Grab(GRAB_CLOSE)
robot.stop()
Turn(190)  # 180도 턴

Follow_right_line()

robot.straight(50)
robot.stop()
Turn(-100)

Follow_right_line()

robot.straight(50)

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
    robot.straight(BYPASS)

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()


## 7번 ###########################################
Follow_left_line()

robot.straight(50)
robot.stop()
Turn(100)

Follow_right_line()

robot.straight(50)
robot.stop()

Turn(-100)
Follow_left_line()

robot.straight(50)

while ultra.distance() > 60:  # 직진 왼쪽라인 보정, 오른쪽 검은색 정지 
    Reflection(PROPORTIONAL_GAIN,COLOR_SENSOR_L.reflection())

while ultra.distance() > 60:  # 초음파 센서 거리 감지
    rate = G * (COLOR_SENSOR_L.reflection() - THRESHOLD)
    robot.drive(100,rate)
    wait(80)

robot.stop()

DEFINE_ID()

robot.straight(120)

Grab(GRAB_CLOSE)

Turn(190)  # 180도 턴

Follow_right_line()

robot.straight(BYPASS)

Follow_right_line()

robot.straight(50)
robot.stop()
Turn(100)

Follow_right_line()

robot.straight(50)
robot.stop()
Turn(-100)

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
    robot.straight(BYPASS)

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

    robot.straight(BYPASS)

    while COLOR_SENSOR_L.reflection() > RV:  # 직진 오른쪽라인 보정, 왼쪽 검은색 정지
        Reflection(-PROPORTIONAL_GAIN,COLOR_SENSOR_R.reflection())
    
    robot.straight(50)
    Turn(100)

robot.stop()
robot.straight(-200)