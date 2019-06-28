import sys
sys.path.insert(0, "../Core")
sys.path.insert(0, "..")
import pwmServo as sServo
import constants as k

if __name__ == '__main__':
    # Open port
    print("Opening Port!")
    if sServo.init():
    	#take Id for the Servos as Input

        servoList=[]
        for i in range(0,12):
            servo=None
            if i<6:
                servo = sServo.pwmServo(ID=k.servoId[i],dirVector=k.dirVector[i],fixedPoint=k.FixedPoints[i],kit=k.kit2)
            else:
                servo = sServo.pwmServo(ID=k.servoId[i],dirVector=k.dirVector[i],fixedPoint=k.FixedPoints[i],kit=k.kit1)
            servoList.append(servo)
            
        Tangle = 0
        for i in range(0,12):
            servoList[i].writeAngle(Tangle)

