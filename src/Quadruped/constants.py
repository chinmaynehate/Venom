import numpy as np	

class Creep:
    def __init__(self):
        # Creep Parameters
        self.DEFAULT_X = 5.5
        self.DEFAULT_Z = -16.3
        self.Y_MAX = 4
        self.Y_MIN = -1
        self.Y_MEAN = (self.Y_MIN+self.Y_MAX)/2  
        self.Z_STEP_UP_HEIGHT = -15.2
        self.totalShiftSize = (self.Y_MAX-self.Y_MIN)/2
        self.stanceIncrements = 1.0
        # Delays
        self.shiftAllInterDelay = 0.01

class Trot:	
    def __init__(self):
        # Trot Parameters
        self.DEFAULT_X = 6.5
        self.DEFAULT_Z = -16.3
        self.Y_MAX = 5
        self.Y_MIN = -2
          
        self.Z_STEP_UP_HEIGHT = -14

        self.trotDelay = 0.5

# Servo Props
servoId = [9,8,3,
            10,8,4,
            2,0,14,
            11,10,7]

#Set-Point of Each Servo
# FixedPoints = [91 - 45,40 + 50,116,
#                 94 + 45,51 + 50,0,
#                 98 -45,49 + 50,90, 
#                 103+45,50 + 50,0 ]

FixedPoints = [91 - 45,40 ,116,
                94 + 45,51 ,0,
                98 -45,49 ,90, 
                103+45,50 ,0 ]  

# Direction of Motion
dirVector = [ 1,1,1,
              1,1,1,
              -1,1,-1,
            -1,1,1,]

# Venom Props

linkLength = [5.5,0,7.6,16.3]
# linkLength = [1,0,1,1]

import board
import busio
from adafruit_servokit import ServoKit

i2c = busio.I2C(board.SCL_1,board.SDA_1)
# kit1=None
# kit2=None

# def i2c_init():
print("Connecting to the I2C Bus......")
kit1 = ServoKit(channels=16,i2c=i2c,address=0x40)
kit2= ServoKit(channels=16,i2c=i2c,address=0x41)
print("I2C Bus Connected.")

# Reference Constants
A = 0
B = 1
C = 2
D = 3
TOP = 0
MIDDLE = 1
BOTTOM = 2

CREEP = 0
TROT = 1
TROT_BACK=2
