import sys
sys.path.insert(0, "..")

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

def storeRawAngle(group_id,ID,Angle):
    return servos.store_value_single(group_id,ID,Angle)

def writeAngle(Angle,Servo_Index):
    # servoId = k.servoId[Servo_Index]
    # RawAngle = toRawAngle(Angle,servoId)
    # writeRawAngle(servoId,RawAngle)
    pass

def readTorque(ID):
    return servos.read_torque(ID)


def readRawAngle(ID):
    return servos.read_pos(ID,0)


def toStandardAngle(angle,dirVector,fixedPoint):
    return dirVector*(angle - fixedPoint) * k.SERVO_RES 

def toRawAngle(angle,dirVector,fixedPoint):
    return (angle) * 1/k.SERVO_RES * 1/dirVector + fixedPoint 

def createNewGroup():
    return servos.get_new_group()

def go2StoredPositions(groupID):
    return servos.go2storedPosition(groupID)
# Servo Object 
class SmartServo:

    def __init__(self,ID=None,dirVector=None,fixedPoint=None,enableTorque=True):
        self.Speed = 200
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

        self.group_id=None
        

    
    def setID(self,ID):
        self.ID = ID
        self.setSpeed(self.Speed)
        self.enable()

    def setGroup(self,group_id):
        self.group_id = group_id

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

    def storeRawAngle(self,Angle):
        if self.group_id !=None:
            return storeRawAngle(self.group_id,self.ID,Angle)
        else:
            print("Group is Not Defined for the Servo. Storing Value Failed")
            quit()

    def writeAngle(self,Angle):
        RawAngle = int(round(toRawAngle(Angle,self.dirVector,self.fixedPoint)))
        #print("Writing Raw :",RawAngle)
        if RawAngle>1023:
            RawAngle=1023
        elif RawAngle<0:
            RawAngle=0
        return writeRawAngle(self.ID,RawAngle)

    def storeAngle(self,Angle):
        RawAngle = int(round(toRawAngle(Angle,self.dirVector,self.fixedPoint)))
        #print("Writing Raw :",RawAngle)
        if RawAngle>1023:
            RawAngle=1023
        elif RawAngle<0:
            RawAngle=0

        if self.group_id !=None:
            return storeRawAngle(self.group_id,self.ID,RawAngle)
        else:
            print("Group is Not Defined for the Servo. Storing Value Failed")
            quit()



    def readRawAngle(self):
        return readRawAngle(self.ID)

    def readStandardAngle(self):
        RawAngle = readRawAngle(self.ID)
        # return RawAngle
        return int(toStandardAngle(RawAngle,self.dirVector,self.fixedPoint))


if __name__=="__main__":
    pass
