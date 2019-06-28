import numpy as np	

class Creep:
    def __init__(self):
        # Creep Parameters
        self.DEFAULT_X = 6.5
        self.DEFAULT_Z = -16.2
        self.Y_MAX = 7
        self.Y_MIN = -2
        self.Y_MEAN = (self.Y_MIN+self.Y_MAX)/2  
        self.Z_STEP_UP_HEIGHT = -14
        self.totalShiftSize = (self.Y_MAX-self.Y_MIN)/2
        self.stanceIncrements = 2.5
        # Delays
        self.shiftAllInterDelay = 0.01

class Trot:	
    def __init__(self):
        # Trot Parameters
        self.DEFAULT_X = 6.5
        self.DEFAULT_Z = -16.2
        self.Y_MAX = 7
        self.Y_MIN = -2
          
        self.Z_STEP_UP_HEIGHT = -14.8

        self.trotDelay = 0.1

# Servo Props
servoId = [11,10,7,9,8,3,10,8,4,6,0,14]

#Set-Point of Each Servo
# FixedPoints = [ 103,99,35,91,80,45,94,102,45,98,98,45 ]  
FixedPoints = [ 103,99,0,91,80,0,94,102,0,98,98,20 ]  

# Direction of Motion
dirVector = [-1,1,-1, 
              1,-1,1,
              1,1,-1,
              -1,-1,1]

# Venom Props

linkLength = [5.5,0,8.3,16.2]
# linkLength = [1,0,1,1]

import board
import busio
from adafruit_servokit import ServoKit

i2c = busio.I2C(board.SCL,board.SDA)
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