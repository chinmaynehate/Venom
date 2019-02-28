import sys
sys.path.insert(0, "Core")
sys.path.insert(0, "unit_Tests")

from constants import *
import smartServo as servo
import kinematics as ik
import time
import math
from helpers import *
import cdynamixel as dynamixel
import interpolation as ip

class Quadruped:
    def __init__(self,servoIndexes=None):
        servo.init()                                #Open Port and Set Baud Rate
        self.Legs = [Leg(),Leg(),Leg(),Leg()]
        if servoIndexes!=None:
            self.setID(servoIndexes)

        self.setDefaults()
            

    def setDefaults(self):
        self.creep = Creep()
        self.trot = Trot()
        self.slope = Slope()

    def setID(self,ID):
        for i in range(0,4):
                self.Legs[i].setIDs(ID[i*3:i*3+3])

    def setParams(self,dirParams,fixedPtsParams):
        for i in range(0,4):
                self.Legs[i].setParams(dirParams[i*3:i*3+3],fixedPtsParams[i*3:i*3+3])

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

        # self.Legs[A].storeLegPos(self.creep.DEFAULT_X ,self.creep.currentYa ,self.creep.DEFAULT_Z)
        # self.Legs[B].storeLegPos(self.creep.DEFAULT_X ,self.creep.currentYb  ,self.creep.DEFAULT_Z)
        # self.Legs[C].storeLegPos(self.creep.DEFAULT_X ,self.creep.currentYc ,self.creep.DEFAULT_Z)
        # self.Legs[D].storeLegPos(self.creep.DEFAULT_X ,self.creep.currentYd  ,self.creep.DEFAULT_Z)

    def setSpeedAllLegs(self,Mode):
        self.Legs[A].setSpeed(Mode)
        self.Legs[B].setSpeed(Mode)
        self.Legs[C].setSpeed(Mode)
        self.Legs[D].setSpeed(Mode)

    def stanceBackwardSlope(self,YShift,ZShift):

        self.slope.currentZa = self.slope.currentZa - ZShift 
        self.slope.currentZb = self.slope.currentZb - ZShift 
        self.slope.currentZc = self.slope.currentZc - ZShift 
        self.slope.currentZd = self.slope.currentZd - ZShift

        self.slope.currentYa = self.slope.currentYa - YShift 
        self.slope.currentYb = self.slope.currentYb - YShift 
        self.slope.currentYc = self.slope.currentYc - YShift 
        self.slope.currentYd = self.slope.currentYd - YShift

        # Write the Input Position to the Legs
        self.Legs[B].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYb  ,self.slope.currentZb)
        self.Legs[A].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYa ,self.slope.currentZa)
        self.Legs[C].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYc ,self.slope.currentZc)
        self.Legs[D].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYd  ,self.slope.currentZd)


    def go2CreepStartPosition(self):
        # Starting Position for Creep Position
        
        # self.Legs[A].setLegPos(self.creep.DEFAULT_X, self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        # self.Legs[B].setLegPos(self.creep.DEFAULT_X, self.creep.Y_MIN,self.creep.DEFAULT_Z)
        # self.Legs[C].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MIN,self.creep.DEFAULT_Z)
        # self.Legs[D].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        
        self.Legs[A].storeLegPos(self.creep.DEFAULT_X, self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        self.Legs[B].storeLegPos(self.creep.DEFAULT_X, self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[C].storeLegPos(self.creep.DEFAULT_X,-self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[D].storeLegPos(self.creep.DEFAULT_X,-self.creep.Y_MEAN,self.creep.DEFAULT_Z)

        self.creep.currentYa =  self.creep.Y_MEAN
        self.creep.currentYb =  self.creep.Y_MIN
        self.creep.currentYc = -self.creep.Y_MIN
        self.creep.currentYd = -self.creep.Y_MEAN

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

        # self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.Z_PICKUP_HEIGHT_TROT)
        # self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.Z_PICKUP_HEIGHT_TROT)
        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)

        time.sleep(self.trot.trotDelay)
        
            # 1.Rotate Top
        # self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        # self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        # self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.DEFAULT_Z)
        # self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.DEFAULT_Z)
        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.DEFAULT_Z)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.DEFAULT_Z)

        time.sleep(self.trot.trotDelay)
        
            # 1.Drop Down the Leg
        # self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.DEFAULT_Z)
        # self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.DEFAULT_Z)
        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MAX,self.trot.DEFAULT_Z)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MIN,self.trot.DEFAULT_Z)
        time.sleep(self.trot.trotDelay)
        

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
            # 2.Pickup the Leg
        # self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)
        # self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)

        time.sleep(self.trot.trotDelay)
            # 2.Rotate Top
        # self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        # self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        # self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.DEFAULT_Z)
        # self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.DEFAULT_Z)
        self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MAX,self.trot.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MIN,self.trot.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.DEFAULT_Z)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.DEFAULT_Z)

        time.sleep(self.trot.trotDelay)
        
            # 2.Drop Down the Leg
        # self.Legs[A].setLegPos(self.trot.DEFAULT_X,left_Y_MAX,self.trot.DEFAULT_Z)
        # self.Legs[C].setLegPos(self.trot.DEFAULT_X,-right_Y_MIN,self.trot.DEFAULT_Z)
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

        # Step 1 - Step Leg B Forward
        self.Legs[B].StepInY(right_Y_MIN,right_Y_MAX)
        self.creep.currentYb = right_Y_MAX

        # input("Press Any Key to PushBack1")
        # Step 1.2 - Push Forward
        self.stanceBackward(self.creep.totalShiftSize,diffFactor)

        # Step 2 - Step Leg D Forward
        self.Legs[D].StepInY(-left_Y_MAX,-left_Y_MIN)
        self.creep.currentYd = -left_Y_MIN

        # Step 2.1 - Step Leg A Forward
        self.Legs[A].StepInY(left_Y_MIN,left_Y_MAX)
        self.creep.currentYa = left_Y_MAX
        time.sleep(0.1)

        # input("Press Any Key to PushBack2")
        # Step 2.2 - Push Forward
        self.stanceBackward(self.creep.totalShiftSize,diffFactor)

        # Step 3 - Step Leg C Forward
        self.Legs[C].StepInY(-right_Y_MAX,-right_Y_MIN)
        self.creep.currentYc = -right_Y_MIN
    

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
        self.joints = [servo.SmartServo(),servo.SmartServo(),servo.SmartServo()]

        if (ID != None):
            self.setIDs(ID)
    
        self.Z_STEP_UP_HEIGHT = -12  
        self.STEP_UP_DELAY = 0.2

        self.groupID = servo.createNewGroup()
        # Assign Group Id to each servos
        self.setGroup(self.groupID)

    def setIDs(self,ID):
        self.joints[TOP].setID(ID[TOP])
        self.joints[MIDDLE].setID(ID[MIDDLE])
        self.joints[BOTTOM].setID(ID[BOTTOM])

    def setGroup(self,groupID=None):
        if groupID!=None:
            for legServo in self.joints:
                legServo.setGroup(groupID)
        else:
            print("Group Not Defined")
            quit()
    
    def setParams(self,dirParams,fixedPointParams):
        self.joints[TOP].setParams(dirParams[TOP],fixedPointParams[TOP])
        self.joints[MIDDLE].setParams(dirParams[MIDDLE],fixedPointParams[MIDDLE])
        self.joints[BOTTOM].setParams(dirParams[BOTTOM],fixedPointParams[BOTTOM])
        self.doOnce = True

    def setVel(self,v1,v2,v3):
        self.joints[TOP].setSpeed(v1)
        self.joints[MIDDLE].setSpeed(v2)
        self.joints[BOTTOM].setSpeed(v3)

    def storeLegPos(self,x,y,z):
        t1,t2,t3,isPossible = ik.getInverse(x,y,z)

        if isPossible:
            # Store the Current Value of X,Y,Z
            if self.doOnce:
                self.doOnce=False
                self.x = x
                self.y = y
                self.z = z

            self.joints[TOP].storeAngle(t1)
            self.joints[MIDDLE].storeAngle(t2)
            self.joints[BOTTOM].storeAngle(t3)
            self.go2StoredPositions()
            self.clearParam()
        else:
            print("Inverse Not Possible")

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
        
    def storeLegPosWithSetSpeeds(self,x,y,z):
        t1,t2,t3,isPossible = ik.getInverse(x,y,z)

        if isPossible:
            # Store the Current Value of X,Y,Z
            if self.doOnce:
                self.doOnce=False
                self.x = x
                self.y = y
                self.z = z
                self.prevAngle1 = 0
                self.prevAngle2 = 0
                self.prevAngle3 = 0

            self.joints[TOP].storeAngle(t1)
            self.joints[MIDDLE].storeAngle(t2)
            self.joints[BOTTOM].storeAngle(t3)

            angle1 = t1
            angle2 = t2
            angle3 = t3

            diff1 = abs(float(self.prevAngle1) - float(angle1))
            diff2 = abs(float(self.prevAngle2) - float(angle2))
            diff3 = abs(float(self.prevAngle3) - float(angle3))
            diffSum = diff1 + diff2 + diff3

            if diffSum != 0:
                v1 = int(cmap(diff1/diffSum, 0, 1, 0, 500))
                v2 = int(cmap(diff2/diffSum, 0, 1, 0, 500))
                v3 = int(cmap(diff3/diffSum, 0, 1, 0, 500))

                self.joints[TOP].setSpeed(v1)
                self.joints[MIDDLE].setSpeed(v2)
                self.joints[BOTTOM].setSpeed(v3)

                # print("Diffs : ",diff1,diff2,diff3)
                # print("setSpeeds : ",v1,v2,v3)
                # print("Ratios : ",diff1/v1, diff2/v2, diff3/v3)

            self.prevAngle1 = angle1
            self.prevAngle2 = angle2
            self.prevAngle3 = angle3

        else:
            print("Inverse Not Possible")

    def StepInY(self,from_y,to_y):
        # input("Press Any Key:Leg Pickup")
        # Pickup the Leg
        # self.setLegPos(self.x,from_y,self.Z_STEP_UP_HEIGHT)
        self.storeLegPos(self.x,from_y,self.Z_STEP_UP_HEIGHT)
        
        time.sleep(self.STEP_UP_DELAY)
        # input("Press Any Key:Leg Rotate")
        # Rotate Top
        # self.setLegPos(self.x,to_y,self.Z_STEP_UP_HEIGHT)
        self.storeLegPos(self.x,to_y,self.Z_STEP_UP_HEIGHT)
        
        self.y = to_y 
        time.sleep(self.STEP_UP_DELAY)
        # input("Press Any Key:Leg Drop")
        # Drop Down the Leg
        # self.setLegPos(self.x,to_y,self.z)
        self.storeLegPos(self.x,to_y,self.z)
        time.sleep(self.STEP_UP_DELAY)

    def StepInYZ(self,from_y,to_y,to_z):
        # input("Press Any Key:Leg Pickup")
        # Pickup the Leg
        self.setLegPos(self.x,from_y,self.Z_STEP_UP_HEIGHT)
        # self.joints[BOTTOM].writeAngle(20);
        
        time.sleep(self.STEP_UP_DELAY)
        # input("Press Any Key:Leg Rotate")
        # Rotate Top
        self.setLegPos(self.x,to_y,self.Z_STEP_UP_HEIGHT)
        # self.joints[BOTTOM].writeAngle(20);
        
        self.y = to_y
        time.sleep(self.STEP_UP_DELAY)
        # input("Press Any Key:Leg Drop")
        # Drop Down the Leg
        self.setLegPos(self.x,to_y,to_z)
        time.sleep(self.STEP_UP_DELAY)

    def StepInZ(self,y,to_z):
        self.setLegPos(self.x,y,to_z)
        time.sleep(0.1)

    def setSpeed(self,Mode):
        if Mode == "SLOWER":   SPEED = 200
        elif Mode == "SLOW":   SPEED = 200
        elif Mode == "NORMAL": SPEED = 200

        self.joints[TOP].setSpeed(SPEED)
        self.joints[MIDDLE].setSpeed(SPEED)
        self.joints[BOTTOM].setSpeed(SPEED)
    
    def go2StoredPositions(self):
        if self.groupID!=None:
            servo.go2StoredPositions(self.groupID)
        else:
            print("Group Not Defined")
            quit()

    def clearParam(self):
        dynamixel.groupSyncWriteClearParam(self.groupID)


if __name__=="__main__":

    venom = Quadruped(servoId)
    venom.setParams(dirVector,FixedPoints)
    venom.go2CreepStartPosition()
    input("Press Enter")

    venom.walk(TROT) 
