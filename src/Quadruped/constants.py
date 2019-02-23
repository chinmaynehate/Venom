ttyUSB_USB2DYNAMIXEL = "/dev/ttyUSB0"

DXL_LIB_PATH = "/home/carnage/DynamixelSDK/c/build/linux64/libdxl_x64_c.so"


ENABLE_DXL_MESSAGES = False

import numpy as np	#$

class Creep:
    def __init__(self):
        # Creep Parameters
        self.DEFAULT_X = 8   
        self.DEFAULT_Z = -16
        self.Y_MAX = 7
        self.Y_MIN = -2
        self.Y_MEAN = (self.Y_MIN+self.Y_MAX)/2  
        self.Z_STEP_UP_HEIGHT = -15
        self.totalShiftSize = (self.Y_MAX-self.Y_MIN)/2
        self.stanceIncrements = 2.5
        # Delays
        self.shiftAllInterDelay = 0.01

class Trot:	
    def __init__(self):
        # Trot Parameters
        self.DEFAULT_X = 6.5
        self.DEFAULT_Z = -17
        self.Y_MAX = 7
        self.Y_MIN = -2
          
        self.Z_STEP_UP_HEIGHT = -15
        self.Z_PICKUP_HEIGHT_TROT = -18


        self.trotDelay = 0.1

class Slope:
    def __init__(self):
        #slope Parameters
        self.DEFAULT_X = 6.5
        BETA        = 18.4        #Distance between servo origns along the direction of motion 
        self.Y_STEP = 4       #Step Size
        CLEARANCE   = 14.0        #clearance between FRONT_MAX and bot height
        THETA       = (7.9) * np.pi / 180      #Slope angle
        Y_MINIMUM   = -1.5              #Change this to set Minimum Y for all legs		
        SHIFT       = self.Y_STEP/2 - abs(Y_MINIMUM)    #Shift if Motion

        self.FRONT_Y_MAX  = self.Y_STEP/2 - SHIFT
        self.FRONT_Y_MIN  = self.FRONT_Y_MAX - self.Y_STEP
        self.FRONT_Y_MEAN = (self.FRONT_Y_MIN + self.FRONT_Y_MAX)/2

        self.BACK_Y_MAX  = self.Y_STEP/2 + SHIFT
        self.BACK_Y_MIN  = self.BACK_Y_MAX - self.Y_STEP
        self.BACK_Y_MEAN = (self.BACK_Y_MIN + self.BACK_Y_MAX)/2

        self.Z_STEP = self.Y_STEP*np.tan(THETA)/2

        #Front Legs are A and B
        self.FRONT_Z_MAX  = -1 * (CLEARANCE)
        self.FRONT_Z_MIN  = self.FRONT_Z_MAX - self.Y_STEP*np.tan(THETA)
        self.FRONT_Z_MEAN = (self.FRONT_Z_MIN + self.FRONT_Z_MAX)/2

        #Back Legs are C and D
        self.BACK_Z_MAX  = -1 * (np.tan(THETA)*(BETA + self.Y_STEP + CLEARANCE/np.tan(THETA)))
        self.BACK_Z_MIN  = self.BACK_Z_MAX + self.Y_STEP*np.tan(THETA)
        self.BACK_Z_MEAN = (self.BACK_Z_MIN + self.BACK_Z_MAX)/2




# Servo Props
servoId = [ 9,18,16,
            7, 2, 3,
           12,13,17,
           14, 8,15]
SERVO_RES = 0.2932551319648094

#Set-Point of Each Servo
FixedPoints = [516+153.45,512,508,
               810-153.45,500,825,
               512+153.45,512,502,
               512-153.45,512,498]  
# Direction of Motion
dirVector = [-1,1,1, 
              1,-1,-1,
              1,1,1,
              -1,-1,1]

# Venom Props

linkLength = [5.5,0,8.3,16.2]
# linkLength = [1,0,1,1]

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