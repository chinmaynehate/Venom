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
    servoId = k.servoId[Servo_Index]
    RawAngle = toRawAngle(Angle,servoId)
    writeRawAngle(servoId,RawAngle)


def readRawAngle(ID):
    return servos.read_pos(ID,0)

def toStandardAngle(angle,ServoIndex):
    return (angle - k.dirVector[ServoIndex]*k.FixedPoints[ServoIndex]) * k.SERVO_RES

def toRawAngle(angle,ServoIndex):
    return (angle) * 1/k.SERVO_RES + k.dirVector[ServoIndex]*k.FixedPoints[ServoIndex]


# Servo Object 
class SmartServo:

    def __init__(self,ID=None):
        if ID!=None:
            self.setID(ID)
        self.Speed = 200
        self.setSpeed(self.Speed)

    
    def setID(self,ID):
        self.ID = ID
    
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
        # RawAngle = toRawAngle(Angle,servoId)
        # return writeRawAngle(servoId,RawAngle)
        pass


    def readRawAngle(self):
        return readRawAngle(self.ID)


if __name__=="__main__":
    pass




