from adafruit_servokit import ServoKit

# ServoKit Object
kit = None

def init():
    print("Connecting to the Servo Driver........")
    kit = ServoKit(channels=16)
    print("Connected to the Servo Driver.")
    return True

def setPwmRange(index,lowerPWM,higherPWM):
    kit.servo[index].set_pulse_width_range(lowerPWM,higherPWM)

def writeAngle(index,Angle): #( _ , 0-180)
    kit.servo[index].angle=Angle   

# Servo Object 
class pwmServo:

    def __init__(self,index=None,dirVector=None,fixedPoint=None):
        if index!=None:
            self.setIndex(index)
        if dirVector!=None:
            self.dirVector = dirVector
        if fixedPoint!=None:
            self.fixedPoint=fixedPoint
        

    def setIndex(self,index):
        self.index = index

    def setParams(self,dirVector,fixedPoint):
        self.dirVector=dirVector
        self.fixedPoint=fixedPoint

    def writeRawAngle(self,Angle): #( _ , 0-1023)
        return writeAngle(self.index,Angle)


    def writeAngle(self,Angle):
        RawAngle =   (Angle * self.dirVector) + self.fixedPoint  
        #print("Writing Raw :",RawAngle)
        if RawAngle>180:
            RawAngle=180
        elif RawAngle<0:
            RawAngle=0
        return writeAngle(self.index,RawAngle)


if __name__=="__main__":
    pass
