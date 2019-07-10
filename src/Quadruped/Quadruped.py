import sys
sys.path.insert(0, "Core")
sys.path.insert(0, "unit_Tests")

from constants import *
import pwmServo as servo
import kinematics as ik
import time
import math
from helpers import *

class Quadruped:
    def __init__(self,servoIndexes=None):
        servo.init()                                #Open Port and Set Baud Rate
        self.Legs = [Leg(),Leg(),Leg(),Leg()]
        if servoIndexes!=None:
            self.setID(servoIndexes)

        # Setup the GAIT Pattern Variables
        self.setDefaults()
            

    def setDefaults(self):
        self.creep = Creep()
        self.trot = Trot()

    def setID(self,ID):
        for i in range(0,4):
                self.Legs[i].setIDs(ID[i*3:i*3+3])

    def setParams(self,dirParams,fixedPtsParams):
        for i in range(0,4):
                self.Legs[i].setParams(dirParams[i*3:i*3+3],fixedPtsParams[i*3:i*3+3])
        
        self.Legs[A].setKit(kit2)
        self.Legs[B].setKit(kit2)
        self.Legs[C].setKit(kit1)
        self.Legs[D].setKit(kit1)


    def stanceBackward(self,totalShift,diffFactor=None):
        #Push the Legs Backwards Together i.e Push THe Bot Forward   (Creep Gait)
        # If Differential_Factor -> 1 then there is no push from either side of the Leg
        # If Differential_Factor -> 0 then there is slow Differential Turning from either Side of the Leg
        
            # Calculate the Destination Y  Position
        # For Non Turning Part (differential Factor == 0)
        if diffFactor==None:        
            self.creep.currentYa = self.creep.currentYa - totalShift 
            self.creep.currentYb = self.creep.currentYb - totalShift 
            self.creep.currentYc = self.creep.currentYc - totalShift 
            self.creep.currentYd = self.creep.currentYd - totalShift
        else:  # For Differential Turning ( -1  <->  +1)
            if diffFactor>=0:       
                #Turn Left
                self.creep.currentYa = self.creep.currentYa - totalShift 
                self.creep.currentYb = self.creep.currentYb - totalShift*(1-abs(diffFactor))
                self.creep.currentYc = self.creep.currentYc - totalShift*(1-abs(diffFactor))
                self.creep.currentYd = self.creep.currentYd - totalShift 
            else:
                #Turn Right
                self.creep.currentYa = self.creep.currentYa - totalShift*(1-abs(diffFactor))
                self.creep.currentYb = self.creep.currentYb - totalShift
                self.creep.currentYc = self.creep.currentYc - totalShift
                self.creep.currentYd = self.creep.currentYd - totalShift*(1-abs(diffFactor)) 
        
        
        # Write the Input Position to the Legs
        self.Legs[A].setLegPos(self.creep.DEFAULT_X ,self.creep.currentYa ,self.creep.DEFAULT_Z)
        self.Legs[B].setLegPos(self.creep.DEFAULT_X ,self.creep.currentYb  ,self.creep.DEFAULT_Z)
        self.Legs[C].setLegPos(self.creep.DEFAULT_X ,self.creep.currentYc ,self.creep.DEFAULT_Z)
        self.Legs[D].setLegPos(self.creep.DEFAULT_X ,self.creep.currentYd  ,self.creep.DEFAULT_Z)

    def go2CreepStartPosition(self):
        # Starting Position for Creep Position
        
        self.Legs[A].setLegPos(self.creep.DEFAULT_X, self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[B].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[C].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        self.Legs[D].setLegPos(self.creep.DEFAULT_X,self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        

        self.creep.currentYa =  self.creep.Y_MIN
        self.creep.currentYb = -self.creep.Y_MIN
        self.creep.currentYc = -self.creep.Y_MEAN
        self.creep.currentYd = self.creep.Y_MEAN

    def Trot(self,diffFactor=None,direction=1):
        
        if diffFactor!=None:
            if diffFactor>=0:       #Turn Right
                left_Y_MAX = self.trot.Y_MAX
                left_Y_MIN = self.trot.Y_MIN
                right_Y_MAX = self.trot.Y_MAX*(1.0-diffFactor)/2
                right_Y_MIN = self.trot.Y_MIN*(1.0-diffFactor)/2    
            else:                   #Turn Left
                left_Y_MAX = self.trot.Y_MAX*(1.0+diffFactor)/2
                left_Y_MIN = self.trot.Y_MIN*(1.0+diffFactor)/2
                right_Y_MAX = self.trot.Y_MAX
                right_Y_MIN = self.trot.Y_MIN
        else:
            left_Y_MAX = self.trot.Y_MAX
            left_Y_MIN = self.trot.Y_MIN
            right_Y_MAX = self.trot.Y_MAX
            right_Y_MIN = self.trot.Y_MIN

        
        if direction <0:        # Change the Direction of Motion 
            # Swap the right_Y and Left Y
            right_Y_MAX,right_Y_MIN = right_Y_MIN,right_Y_MAX
            left_Y_MAX,left_Y_MIN = left_Y_MIN,left_Y_MAX


        # Step 1 - Step Leg B And D Forward and PushBack Leg A and C Back
            # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)

        time.sleep(self.trot.trotDelay)
        
            # 1.Rotate Top
        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.DEFAULT_Z)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.DEFAULT_Z)

        time.sleep(self.trot.trotDelay)
        
            # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.DEFAULT_Z)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.DEFAULT_Z)
        time.sleep(self.trot.trotDelay)
        

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
            # 2.Pickup the Leg
        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)

        time.sleep(self.trot.trotDelay)
            # 2.Rotate Top
        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.DEFAULT_Z)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.DEFAULT_Z)

        time.sleep(self.trot.trotDelay)
        
            # 2.Drop Down the Leg
        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MAX,self.trot.DEFAULT_Z)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MIN,self.trot.DEFAULT_Z)

        time.sleep(self.trot.trotDelay)
        
    def Creep(self,diffFactor=None):
       
        if diffFactor==None:
            left_Y_MAX=self.creep.Y_MAX
            left_Y_MIN=self.creep.Y_MIN
            right_Y_MAX=self.creep.Y_MAX
            right_Y_MIN=self.creep.Y_MIN
        else:
            if diffFactor>=0:       #Turn Right
                left_Y_MAX=self.creep.Y_MAX
                left_Y_MIN=self.creep.Y_MIN
                right_Y_MAX=self.creep.Y_MAX*(1.0-diffFactor)/2
                right_Y_MIN=self.creep.Y_MIN*(1.0-diffFactor)/2
            else:                   #Turn Left
                left_Y_MAX=self.creep.Y_MAX*(1.0+diffFactor)/2
                left_Y_MIN=self.creep.Y_MIN*(1.0+diffFactor)/2
                right_Y_MAX=self.creep.Y_MAX
                right_Y_MIN=self.creep.Y_MIN

        
        # Step 2.1 - Step Leg A Forward
        # input("Step A Forward")
        self.Legs[A].StepInY(left_Y_MIN,left_Y_MAX)
        self.creep.currentYa = left_Y_MAX
        time.sleep(0.1)
        
        # input("Press Any Key to PushBack1")
        # Step 1.2 - Push Forward
        self.stanceBackward(self.creep.totalShiftSize,diffFactor)
        

        time.sleep(0.1)
        # Step 3 - Step Leg C Forward
        # input("Step C Forward")
        self.Legs[C].StepInY(-right_Y_MAX,-right_Y_MIN)
        self.creep.currentYc = -right_Y_MIN

        time.sleep(0.1)

        # Step 2 - Step Leg D Forward
        # input("Step D Forward")
        self.Legs[D].StepInY(left_Y_MIN,left_Y_MAX)
        self.creep.currentYd = left_Y_MAX

        time.sleep(0.1)

        # input("Press Any Key to PushBack2")
        # Step 2.2 - Push Forward
        self.stanceBackward(self.creep.totalShiftSize,diffFactor)


        # Step 1 - Step Leg B Forward
        # input("Step B Forward")
        self.Legs[B].StepInY(-right_Y_MAX,-right_Y_MIN)
        self.creep.currentYb = -right_Y_MIN

        time.sleep(0.1)
        
    

    def walk(self,Mode,diffFactor=None):
        self.go2CreepStartPosition()
        # input("Press Enter")
        while True:
            if Mode == CREEP:
                self.Creep(diffFactor)
            elif Mode == TROT:
                self.Trot(diffFactor)
            elif Mode == TROT_BACK:
                self.Trot(diffFactor,direction=-1)
            else:
                print("Walking Mode is Not Specified")
                quit()
        


class Leg:
    def __init__(self,ID = None):
        self.joints = [servo.pwmServo(),servo.pwmServo(),servo.pwmServo()]

        if (ID != None):
            self.setIDs(ID)
    
        self.Z_STEP_UP_HEIGHT = -13
        self.STEP_UP_DELAY = 0.15


    def setIDs(self,ID):
        self.joints[TOP].setIndex(ID[TOP])
        self.joints[MIDDLE].setIndex(ID[MIDDLE])
        self.joints[BOTTOM].setIndex(ID[BOTTOM])
    
    def setParams(self,dirParams,fixedPointParams):
        self.joints[TOP].setParams(dirParams[TOP],fixedPointParams[TOP])
        self.joints[MIDDLE].setParams(dirParams[MIDDLE],fixedPointParams[MIDDLE])
        self.joints[BOTTOM].setParams(dirParams[BOTTOM],fixedPointParams[BOTTOM])
        self.doOnce = True
    
    def setKit(self,kit):
        for x in self.joints:
            x.setKit(kit)
            x.setPWM(500,2500)

    def setLegPos(self,x,y,z):
        t1,t2,t3,isPossible = ik.getInverse(x,y,z)

        if isPossible:
            # Store the Current Value of X,Y,Z
            if self.doOnce:
                self.doOnce=False
                self.x = x
                self.y = y
                self.z = z

            self.joints[TOP].writeAngle(t1)
            self.joints[MIDDLE].writeAngle(t2)
            self.joints[BOTTOM].writeAngle(t3)
            
        else:
            print("Inverse Not Possible")

    

    def StepInY(self,from_y,to_y):

        # input("Press Any Key:Leg Pickup")
        # Pickup the Leg
        self.setLegPos(self.x,from_y,self.Z_STEP_UP_HEIGHT)
        time.sleep(self.STEP_UP_DELAY)


        # input("Press Any Key:Leg Rotate")
        # Rotate Top
        self.setLegPos(self.x,to_y,self.Z_STEP_UP_HEIGHT)
        time.sleep(self.STEP_UP_DELAY)
        self.y = to_y 

        # input("Press Any Key:Leg Drop")
        # Drop Down the Leg
        self.setLegPos(self.x,to_y,self.z)
        time.sleep(self.STEP_UP_DELAY)



if __name__=="__main__":

    venom = Quadruped(servoId)
    venom.setParams(dirVector,FixedPoints)
    venom.go2CreepStartPosition()
    input("Press Enter")

    venom.walk(CREEP)
