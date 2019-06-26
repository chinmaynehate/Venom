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
servoId = [x for x in range(0,16)]

#Set-Point of Each Servo
FixedPoints = [ 90 ] * 12  

# Direction of Motion
dirVector = [-1,1,-1, 
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