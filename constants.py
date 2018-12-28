ttyUSB_USB2DYNAMIXEL = "/dev/ttyUSB6"

DXL_LIB_PATH = "/home/chinmay/DynamixelSDK/c/build/linux64/libdxl_x64_c.so"


ENABLE_DXL_MESSAGES = True
ENABLE_DEBUG_MESSAGES = True



# Servo Props
servoId = [9,6,5,16,2,3,12,13,18,14,1,8]
SERVO_RES = 0.2932551319648094

#Set-Point of Each Servo
FixedPoints = [820+153.45,512,194,512-153.45,495,210,512+153.45,512,194,512-153.45,512,194]  
# Direction of Motion
dirVector = [-1,1,1,1,1,1,1,-1,1,-1,-1,1]

# Venom Props

linkLength = [5.5,0,8.3,14.1]
# linkLength = [1,0,1,1]

# Reference Constants
A = 0
B = 3
C = 6
D = 9
TOP = 0
MIDDLE = 1
BOTTOM = 2
