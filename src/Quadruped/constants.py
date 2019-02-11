ttyUSB_USB2DYNAMIXEL = "/dev/ttyUSB0"

DXL_LIB_PATH = "/home/shanks/Downloads/Libraries/DynamixelSDK-master/c/build/linux64/libdxl_x64_c.so"

ENABLE_DXL_MESSAGES = False

import numpy as np	#$

class Creep:
    def __init__(self):
        # Creep Parameters
        self.DEFAULT_X = 6.5
        self.DEFAULT_Z = -17
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
		self.BETA = 18.4
		self.Y_STEP = 4
		self.Y_MIN = (-1) * self.Y_STEP / 2
		self.Y_MAX = self.Y_MIN + self.Y_STEP
		self.Y_MEAN = (self.Y_MIN + self.Y_MAX)/2
		self.CLEARANCE = 20 #17

		self.THETA = (5) * np.pi / 180
		self.Z_STEP = self.Y_STEP*np.tan(self.THETA)/2

		#Front Legs are A and B
		self.FRONT_Z_MAX = -1 * self.CLEARANCE
		self.FRONT_Z_MIN = -1 * (self.CLEARANCE + self.Y_STEP*np.tan(self.THETA))
		self.FRONT_Z_MEAN = (self.FRONT_Z_MIN + self.FRONT_Z_MAX)/2

		#Back Legs are C and D
		self.BACK_Z_MIN = -1 * (np.tan(self.THETA)*(self.BETA + self.Y_STEP + (self.CLEARANCE/np.tan(self.THETA))))
		self.BACK_Z_MAX = self.BACK_Z_MIN + self.Y_STEP*(np.tan(self.THETA))
		self.BACK_Z_MEAN = (self.BACK_Z_MIN + self.BACK_Z_MAX)/2



# Servo Props
servoId = [9,18,11,7,2,3,12,13,17,14,8,15]
SERVO_RES = 0.2932551319648094

#Set-Point of Each Servo
FixedPoints = [516+153.45,512,515,
               810-153.45,495,210,
               512+153.45,512,515,
               512-153.45,512,819]  
# Direction of Motion
dirVector = [-1,1,1,
              1,1,1,
              1,1,1,
              -1,-1,1]

# Venom Props

linkLength = [5.5,0,8.3,14.1]
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