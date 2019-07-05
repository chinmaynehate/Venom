import sys
sys.path.insert(0, "../Core")
sys.path.insert(0, "..")
import pwmServo as servo

if __name__ == '__main__':
    # Open port
    print("Opening Port!")
    if servo.init():
    	#take Id for the Servos as Input

        Id = int(input("Enter The Servo ID(Enter -1 to Quit)s:"))
        while True:
            exAngle = int(input("Enter the Servo Angle(0-180)"))
            servo.writeAngle(Id,exAngle)
            print("------------------------------------------------------------------")

