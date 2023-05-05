#!/usr/bin/env python3
from eye import *
import math

SIM_WORLD_SIZE = 5000


def Mapping():

    lidarValues = LIDARGet()  # [20, 25, 10] (360) elements
    # left: lidarValues[90]
    # front: lidarValues[180]
    # right: lidarValues[270]

    # If in C:
    # int distances [360]; #IDARGet (distances);
    # int x, y, phi;
    # VWGetPosition(&x, &y, &phi);

    x, y, phi = VWGetPosition()

    # for (int angle 0; angle < 360; angle++ ) {
    # lidarValue = lidarvalues[angle];
    # }

    # 360 elements: [-180°... 9° 180]
    for angle, lidarValue in enumerate(lidarValues):
        if lidarValue > SIM_WORLD_SIZE:  # Maximum value, so don't bother drawing a line until we can see the end
            continue

        # TODO  (will be a function of angle and phi), in the world frame
        angle_to_object = 0     # phi - angle + 180 ?

        lidar_x = int(x-lidarValue*math.cos(angle_to_object))
        lidar_y = int(y-lidarValue*math.sin(angle_to_object))

        drawLine(x, y, lidar_x, lidar_y)


def explore():
    # Initialise the map with a grey box

    while True:
        if KEYRead() == KEY4:
            VWSetSpeed(0, 0)
            break


if __name__ == "__main__":
    # SIMSetRobot(0, 300, 300, 100, -90)
    VWSetPosition(500, 200, 0)

    LCDMenu("Start", "Mapping", " ", "End")

    KEYWait(KEY1)
    LCDPrintf("Welcome\n")

    KEYWait(KEY2)
    LCDPrintf("Mapping of the environment\n")
    Mapping()

    KEYWait(KEY4)
