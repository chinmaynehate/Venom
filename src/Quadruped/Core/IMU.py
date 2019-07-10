import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

from threading import Thread

y=0.0
p=0.0
r=0.0

def read():
    return y,p,r


def init():

    SETTINGS_FILE = "/home/jetson/Documents/Venom/src/Quadruped/Core/imu/scripts/RTIMULib"

    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
        print("Settings file does not exist, will be created")

    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)

    print("IMU Name: " + imu.IMUName())

    if (not imu.IMUInit()):
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded")

    # this is a good time to set any fusion parameters

    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)

    poll_interval = imu.IMUGetPollInterval()
    print("Recommended Poll Interval: %dmS\n" % poll_interval)
    global y,p,r
    while True:
        if imu.IMURead():
            # x, y, z = imu.getFusionData()
            # print("%f %f %f" % (x,y,z))
            data = imu.getIMUData()
            fusionPose = data["fusionPose"]
            r = math.degrees(fusionPose[0])
            p = math.degrees(fusionPose[1])
            y = math.degrees(fusionPose[2])
            # print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
            #     math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
            time.sleep(poll_interval*1.0/1000.0)

def start():
    process = Thread(target=init)
    process.start()


if __name__=="__main__":
    start()
    time.sleep(0.3)
    while True:
        print(read())
        time.sleep(0.05)