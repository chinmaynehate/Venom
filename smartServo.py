import servo_functions as servos
import constants as k

def init():
    return servos.enable_port()

def enable(ID):
    return servos.enable_bot(ID)

def disable(ID):
    return  servos.disable_bot(ID)

def setSpeed(ID,Speed): #(0-1023)
    return servos.set_speed(ID,Speed)

def writeRawAngle(ID,Angle): #( _ , 0-1023)
    return servos.write_pos(ID,Angle) 

def writeAngle(Angle,Servo_Index):
    # servoId = k.servoId[Servo_Index]
    # RawAngle = toRawAngle(Angle,servoId)
    # writeRawAngle(servoId,RawAngle)
    pass


def readRawAngle(ID):
    return servos.read_pos(ID,0)


def toStandardAngle(angle,dirVector,fixedPoint):
    return dirVector*(angle - fixedPoint) * k.SERVO_RES 

def toRawAngle(angle,dirVector,fixedPoint):
    return (angle) * 1/k.SERVO_RES * 1/dirVector + fixedPoint 


# Servo Object 
class SmartServo:

    def __init__(self,ID=None,dirVector=None,fixedPoint=None,enableTorque=True):
        self.Speed = 100
        if ID!=None:
            self.setID(ID)
        if dirVector!=None:
            self.dirVector = dirVector
        if fixedPoint!=None:
            self.fixedPoint=fixedPoint
        

        if not enableTorque and ID!=None:
            self.disable()
        elif ID!=None:
            self.enable()
        

    
    def setID(self,ID):
        self.ID = ID
        self.setSpeed(self.Speed)
        self.enable()

    def setParams(self,dirVector,fixedPoint):
        self.dirVector=dirVector
        self.fixedPoint=fixedPoint
    
    def enable(self):
        return enable(self.ID)

    def disable(self):
        return  disable(self.ID)

    def setSpeed(self,Speed): #(0-1023)
        self.Speed = Speed
        return setSpeed(self.ID,self.Speed)

    def writeRawAngle(self,Angle): #( _ , 0-1023)
        return writeRawAngle(self.ID,Angle)

    def writeAngle(self,Angle):
        RawAngle = toRawAngle(Angle,self.dirVector,self.fixedPoint)
        return writeRawAngle(self.ID,int(RawAngle))

    def readRawAngle(self):
        return readRawAngle(self.ID)

    def readStandardAngle(self):
        RawAngle = readRawAngle(self.ID)
        # return RawAngle
        return int(toStandardAngle(RawAngle,self.dirVector,self.fixedPoint))


    def testfunc(self):
        return 1+1

if __name__=="__main__":
    pass
