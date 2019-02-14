import sys
sys.path.insert(0, "../Core")
sys.path.insert(0, "..")

import smartServo as sServo
import constants as k

if __name__=="__main__":
    sServo.init()
    servoList=[]
    for i in range(0,12):
        servo = sServo.SmartServo(ID=k.servoId[i],dirVector=k.dirVector[i],fixedPoint=k.FixedPoints[i],enableTorque=True)
        servoList.append(servo)
        
    Tangle = 0
    for i in range(0,12):
        servoList[i].writeAngle(Tangle)
        

