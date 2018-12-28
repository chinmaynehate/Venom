import smartServo as sServo
import constants as k

if __name__=="__main__":
    sServo.init()
    servoList=[]
    for i in range(0,12):
        servo = sServo.SmartServo(ID=k.servoId[i],dirVector=k.dirVector[i],fixedPoint=k.FixedPoints[i],enableTorque=False)
        servoList.append(servo)
        
    while True:
        for i in range(0,12):
            if i ==0:
                print("Leg0:",end="- ")
            if i ==3:
                print(" Leg1:",end="- ")
            if i ==6:
                print(" Leg2:",end="- ")
            if i ==9:
                print(" Leg3:",end="- ")
            # print(servoList[i].readStandardAngle(),end=" ,")
            print(servoList[i].readRawAngle(),end=" ,")
            
        print()

