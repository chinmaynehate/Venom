import smartServo as sServo
import constants as k

if __name__=="__main__":
    sServo.init()
    servoList=[]
    for i in range(0,12):
        servo = sServo.SmartServo(ID=k.servoId[i],dirVector=k.dirVector[i],fixedPoint=k.FixedPoints[i],enableTorque=True)
        servoList.append(servo)
        
    while True:
        print("Enter the Target Servo Index:",end=" ")
        index = int(input())
        print("Enter the Angle:",end=" ")
        angle = int(input())

        servoList[index].writeAngle(angle)
        

