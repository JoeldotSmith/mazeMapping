#!/usr/bin/env python3
from eye import *
import math

SIM_WORLD_SIZE = 2000
SPEED = 300


def drawLine(x, y, lidar_x, lidar_y):
    if lidar_x > SIM_WORLD_SIZE:
        lidar_x = SIM_WORLD_SIZE
    if lidar_x < 0:
        lidar_x = 0
    if lidar_y > SIM_WORLD_SIZE:
        lidar_y = SIM_WORLD_SIZE
    if lidar_y < 0:
        lidar_y = 0
    print("x = " +str(2*int(128*x/SIM_WORLD_SIZE))+ ", y = " + str(256-2*int(y/SIM_WORLD_SIZE)))
    LCDLine(2*int(128*x/SIM_WORLD_SIZE), 256-2*int(128*y/SIM_WORLD_SIZE), 2 * int(128*lidar_x/SIM_WORLD_SIZE), 256-2*int(128*lidar_y/SIM_WORLD_SIZE), WHITE)
    LCDCircle(2*int(128*lidar_x/SIM_WORLD_SIZE), 256-2 * int(128*lidar_y/SIM_WORLD_SIZE), 5, GREEN, 1)


def mapping():

    lidarValues = LIDARGet()  # (360) elements
    # left: lidarValues[90]
    # front: lidarValues[180]
    # right: lidarValues[270]

    x, y, phi = VWGetPosition()
    LCDCircle(2*int(128*x/SIM_WORLD_SIZE), 256-2 *int(y/SIM_WORLD_SIZE), 5, RED, 1)

    # 360 elements: [-180°... 9° 180]
    for angle, lidarValue in enumerate(lidarValues):
        if lidarValue > SIM_WORLD_SIZE:  # Maximum value, so don't bother drawing a line until we can see the end
            continue

        angle_to_object = phi - angle + 180

        lidar_x = int(x+lidarValue*math.cos(angle_to_object*math.pi/180))
        lidar_y = int(y+lidarValue*math.sin(angle_to_object*math.pi/180))

        
        #drawLine(x, y, lidar_x, lidar_y)
        # KEYWait(KEY3)


def explore():

    while True:
        if KEYRead() == KEY4:
            VWSetSpeed(0, 0)
            break
        else:
            lidarValues = LIDARGet()
            print("Distance to wall: ", lidarValues[180])
            while lidarValues[180] > 200:
                print("Distance to wall: ", lidarValues[180])
                mapping()
                lidarValues = LIDARGet()
                tooFar = PSDGet(PSD_RIGHT) > 200
                tooClose = PSDGet(PSD_RIGHT) < 100
                print("PSDRIGHT = "+ str(PSDGet(PSD_RIGHT)))
                if tooFar:
                    VWTurn(-15, 45)
                    VWWait()
                elif tooClose:
                    VWTurn(15, 45)
                    VWWait()
                
                else:
                    VWStraight(50, 200)
                    VWWait()
            else:
                VWTurn(15, 45)
                VWWait()
                


if __name__ == "__main__":
    # SIMSetRobot(0, 300, 300, 100, -90)
    VWSetPosition(180, 180, 0)

    LCDMenu("Start", "Mapping", " ", "End")

    # Initialise the map with a grey box
    KEYWait(KEY1)
    LCDArea(0, 0, 256, 256, NAVY, 1)
    x = 180
    y = 180
    LCDCircle(2*int(128*x/SIM_WORLD_SIZE), 256-2 *int(y/SIM_WORLD_SIZE), 5, RED, 1)

    KEYWait(KEY2)
    explore()

    KEYWait(KEY4)
