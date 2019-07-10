import sys
sys.path.insert(0, "..")
import constants as k

def init():
    # k.i2c_init()
    return True

def setPwmRange(index,lowerPWM,higherPWM,kit):
    kit.servo[index].set_pulse_width_range(lowerPWM,higherPWM)

def writeAngle(index,Angle,kit): #( _ , 0-180)
    # print("Writing Angle:",Angle," to Index:",index)
    kit.servo[index].angle=Angle   

# Servo Object 
class pwmServo:

    def __init__(self,index=None,dirVector=None,fixedPoint=None,kit=None):
        if index!=None:
            self.setIndex(index)
        if dirVector!=None:
            self.dirVector = dirVector
        if fixedPoint!=None:
            self.fixedPoint=fixedPoint
        if kit!=None:
            self.kit=kit
        

    def setIndex(self,index):
        self.index = index

    def setPWM(self,minPWM,maxPWM):
        setPwmRange(self.index,minPWM,maxPWM,self.kit)

    def setParams(self,dirVector,fixedPoint):
        self.dirVector=dirVector
        self.fixedPoint=fixedPoint

    def setKit(self,kit):
        self.kit = kit

    def writeRawAngle(self,Angle): #( _ , 0-1023)
        return writeAngle(self.index,Angle,self.kit)


    def writeAngle(self,Angle):
        RawAngle =   (Angle * self.dirVector) + self.fixedPoint  
        #print("Writing Raw :",RawAngle)
        if RawAngle>=180:
            print("Angle Limit Reached of Servo:",self.index)
            RawAngle=180
        elif RawAngle<=0:
            print("Angle Limit Reached of Servo:",self.index)
            RawAngle=0
        # print(self.kit)
        return writeAngle(self.index,RawAngle,self.kit)


if __name__=="__main__":
    pass

