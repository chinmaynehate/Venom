import sys
sys.path.insert(0, "Core")
sys.path.insert(0, "unit_Tests")

from constants import *
import smartServo as servo
import kinematics as ik
import time
import math

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
        self.Legs[A].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYa ,self.slope.currentZa)
        self.Legs[B].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYb  ,self.slope.currentZb)
        self.Legs[C].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYc ,self.slope.currentZc)
        self.Legs[D].setLegPos(self.slope.DEFAULT_X ,self.slope.currentYd  ,self.slope.currentZd)


    def go2CreepStartPosition(self):
        # Starting Position for Creep Position
        
        self.Legs[A].setLegPos(self.creep.DEFAULT_X, self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        self.Legs[B].setLegPos(self.creep.DEFAULT_X, self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[C].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MIN,self.creep.DEFAULT_Z)
        self.Legs[D].setLegPos(self.creep.DEFAULT_X,-self.creep.Y_MEAN,self.creep.DEFAULT_Z)
        

        self.creep.currentYa =  self.creep.Y_MEAN
        self.creep.currentYb =  self.creep.Y_MIN
        self.creep.currentYc = -self.creep.Y_MIN
        self.creep.currentYd = -self.creep.Y_MEAN

    def go2SlopeStartPosition(self,mode):  #$
        # Starting Position for Slope Climbing
        if mode == 1:
            self.Legs[A].setLegPos(self.slope.DEFAULT_X, self.slope.FRONT_Y_MEAN,self.slope.FRONT_Z_MEAN)
            self.Legs[B].setLegPos(self.slope.DEFAULT_X, self.slope.FRONT_Y_MIN,self.slope.FRONT_Z_MIN)
            self.Legs[C].setLegPos(self.slope.DEFAULT_X,-self.slope.BACK_Y_MIN,self.slope.BACK_Z_MIN)
            self.Legs[D].setLegPos(self.slope.DEFAULT_X,-self.slope.BACK_Y_MEAN,self.slope.BACK_Z_MEAN)

            self.slope.currentYa =  self.slope.FRONT_Y_MEAN
            self.slope.currentYb =  self.slope.FRONT_Y_MIN
            self.slope.currentYc = -self.slope.BACK_Y_MIN
            self.slope.currentYd = -self.slope.BACK_Y_MEAN
            
            self.slope.currentZa = self.slope.FRONT_Z_MEAN
            self.slope.currentZb = self.slope.FRONT_Z_MIN
            self.slope.currentZc = self.slope.BACK_Z_MIN
            self.slope.currentZd = self.slope.BACK_Z_MEAN
        
        else:
            self.Legs[A].setLegPos(self.slope.DEFAULT_X, self.slope.FRONT_Y_MIN,self.slope.FRONT_Z_MIN)
            self.Legs[B].setLegPos(self.slope.DEFAULT_X, self.slope.FRONT_Y_MEAN,self.slope.FRONT_Z_MEAN)
            self.Legs[C].setLegPos(self.slope.DEFAULT_X,-self.slope.BACK_Y_MEAN,self.slope.BACK_Z_MEAN)
            self.Legs[D].setLegPos(self.slope.DEFAULT_X,-self.slope.BACK_Y_MAX,self.slope.BACK_Z_MAX)

            # mf1 = (self.slope.FRONT_Z_MIN - self.slope.FRONT_Z_MEAN)/(self.slope.FRONT_Y_MIN - self.slope.FRONT_Y_MEAN)
            # mf2 = (self.slope.FRONT_Z_MEAN - self.slope.FRONT_Z_MAX)/(self.slope.FRONT_Y_MEAN - self.slope.FRONT_Y_MAX)
            # mb1 = (self.slope.BACK_Z_MIN - self.slope.BACK_Z_MEAN)/(self.slope.BACK_Y_MIN - self.slope.BACK_Y_MEAN)
            # mb2 = (self.slope.BACK_Z_MEAN - self.slope.BACK_Z_MAX)/(self.slope.BACK_Y_MEAN - self.slope.BACK_Y_MAX)
            # print(math.atan(mf1)*180/np.pi, math.atan(mf2)*180/np.pi, math.atan(mb1)*180/np.pi, math.atan(mb2)*180/np.pi)
            # print("FRONT_Y :",self.slope.FRONT_Y_MAX,self.slope.FRONT_Y_MEAN,self.slope.FRONT_Y_MIN)
            # print("FRONT_Z :",self.slope.FRONT_Z_MIN,self.slope.FRONT_Z_MEAN,self.slope.FRONT_Z_MAX)
            # print("BACK_Y :",self.slope.BACK_Y_MIN,self.slope.BACK_Y_MEAN,self.slope.BACK_Y_MAX)
            # print("BACK_Z :",self.slope.BACK_Z_MIN,self.slope.BACK_Z_MEAN,self.slope.BACK_Z_MAX)

            self.slope.currentYa =  self.slope.FRONT_Y_MIN
            self.slope.currentYb =  self.slope.FRONT_Y_MEAN
            self.slope.currentYc = -self.slope.BACK_Y_MEAN
            self.slope.currentYd = -self.slope.BACK_Y_MAX
            
            self.slope.currentZa = self.slope.FRONT_Z_MIN
            self.slope.currentZb = self.slope.FRONT_Z_MEAN
            self.slope.currentZc = self.slope.BACK_Z_MEAN
            self.slope.currentZd = self.slope.BACK_Z_MAX

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

        self.Legs[B].setLegPos(self.trot.DEFAULT_X,right_Y_MIN,self.trot.Z_PICKUP_HEIGHT_TROT)
        self.Legs[D].setLegPos(self.trot.DEFAULT_X,-left_Y_MAX,self.trot.Z_PICKUP_HEIGHT_TROT)

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
        
    def Creep(self,slope,mode,diffFactor=None):
       
        if not slope:
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

            # input("Press Any Key to PushBack2")
            # Step 2.2 - Push Forward
            self.stanceBackward(self.creep.totalShiftSize,diffFactor)

            # Step 3 - Step Leg C Forward
            self.Legs[C].StepInY(-right_Y_MAX,-right_Y_MIN)
            self.creep.currentYc = -right_Y_MIN
        
        else:
            FRONT_Y_MAX = self.slope.FRONT_Y_MAX
            FRONT_Y_MIN = self.slope.FRONT_Y_MIN
            FRONT_Y_MEAN = self.slope.FRONT_Y_MEAN
            BACK_Y_MAX = self.slope.BACK_Y_MAX
            BACK_Y_MIN = self.slope.BACK_Y_MIN
            BACK_Y_MEAN = self.slope.BACK_Y_MEAN
            FRONT_Z_MAX = self.slope.FRONT_Z_MAX
            FRONT_Z_MIN = self.slope.FRONT_Z_MIN
            FRONT_Z_MEAN = self.slope.FRONT_Z_MEAN
            BACK_Z_MAX = self.slope.BACK_Z_MAX
            BACK_Z_MIN = self.slope.BACK_Z_MIN
            BACK_Z_MEAN = self.slope.BACK_Z_MEAN
            
            if mode == 1:
                # Step 1 - Step Leg B Forward
                self.Legs[B].StepInYZ(FRONT_Y_MIN,FRONT_Y_MAX,FRONT_Z_MAX)
                self.slope.currentYb = FRONT_Y_MAX
                self.slope.currentZb = FRONT_Z_MAX

                # input("Press Any Key to PushBack1")
                # Step 1.2 - Push Forward

                self.setSpeedAllLegs("SLOW")
                self.stanceBackwardSlope(self.slope.Y_STEP/2,self.slope.Z_STEP)
                self.setSpeedAllLegs("NORMAL")

                # Step 2 - Step Leg D Forward
                self.Legs[D].StepInYZ(-BACK_Y_MAX,-BACK_Y_MIN,BACK_Z_MIN)
                self.slope.currentYd = -BACK_Y_MIN
                self.slope.currentZd = BACK_Z_MIN

                # Step 2.1 - Step Leg A Forward
                self.Legs[A].StepInYZ(FRONT_Y_MIN,FRONT_Y_MAX,FRONT_Z_MAX)
                self.slope.currentYa = FRONT_Y_MAX
                self.slope.currentZa = FRONT_Z_MAX

                # input("Press Any Key to PushBack2")
                # Step 2.2 - Push Forward
                self.setSpeedAllLegs("SLOW")
                self.stanceBackwardSlope(self.slope.Y_STEP/2,self.slope.Z_STEP)
                self.setSpeedAllLegs("NORMAL")

                # Step 3 - Step Leg C Forward
                self.Legs[C].StepInYZ(-BACK_Y_MAX,-BACK_Y_MIN,BACK_Z_MIN)
                self.slope.currentYc = -BACK_Y_MIN
                self.slope.currentZc = BACK_Z_MIN
            
            else:
                # Step 1 - Step Leg D Forward
                self.Legs[D].StepInYZ(-BACK_Y_MAX,-BACK_Y_MIN,BACK_Z_MIN)
                self.slope.currentYd = -BACK_Y_MIN
                self.slope.currentZd = BACK_Z_MIN

                input("Press Any Key for STEP 2")
                # Step 2 - Step Leg A Forward
                self.Legs[A].StepInYZ(FRONT_Y_MIN,FRONT_Y_MAX,FRONT_Z_MAX)
                self.slope.currentYa = FRONT_Y_MAX
                self.slope.currentZa = FRONT_Z_MAX

                input("Press Any Key for STEP 3")
                # Step 3 - Push Forward
                self.setSpeedAllLegs("SLOW")
                self.stanceBackwardSlope(self.slope.Y_STEP/2,self.slope.Z_STEP)
                self.setSpeedAllLegs("NORMAL")

                input("Press Any Key for STEP 4")
                # Step 4 - Step Leg C Forward
                self.Legs[C].StepInYZ(-BACK_Y_MAX,-BACK_Y_MIN,BACK_Z_MIN)
                self.slope.currentYc = -BACK_Y_MIN
                self.slope.currentZc = BACK_Z_MIN

                input("Press Any Key for STEP 5")
                # Step 5 - Step Leg B Forward
                self.Legs[B].StepInYZ(FRONT_Y_MIN,FRONT_Y_MAX,FRONT_Z_MAX)
                self.slope.currentYb = FRONT_Y_MAX
                self.slope.currentZb = FRONT_Z_MAX

                input("Press Any Key for STEP 6")
                # Step 6 - Push Forward
                self.setSpeedAllLegs("SLOW")
                self.stanceBackwardSlope(self.slope.Y_STEP/2,self.slope.Z_STEP)
                self.setSpeedAllLegs("NORMAL")


    def walk(self,Mode,diffFactor=None):
        self.go2CreepStartPosition()
        # input("Press Enter")
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
    
        self.Z_STEP_UP_HEIGHT = -9  #$ -9
        self.STEP_UP_DELAY = 0.4


    def setIDs(self,ID):
        self.joints[TOP].setID(ID[TOP])
        self.joints[MIDDLE].setID(ID[MIDDLE])
        self.joints[BOTTOM].setID(ID[BOTTOM])

    
    def setParams(self,dirParams,fixedPointParams):
        self.joints[TOP].setParams(dirParams[TOP],fixedPointParams[TOP])
        self.joints[MIDDLE].setParams(dirParams[MIDDLE],fixedPointParams[MIDDLE])
        self.joints[BOTTOM].setParams(dirParams[BOTTOM],fixedPointParams[BOTTOM])
        self.doOnce = True
        
        

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
        self.setLegPos(self.x,to_y,self.z)
        time.sleep(self.STEP_UP_DELAY)

    def setSpeed(self,Mode):
        if Mode == "SLOW":
            SLOW_SPEED = 200
            self.joints[TOP].setSpeed(SLOW_SPEED)
            self.joints[MIDDLE].setSpeed(SLOW_SPEED)
            self.joints[BOTTOM].setSpeed(SLOW_SPEED)
        elif Mode == "NORMAL":
            Normal_SPEED = 400
            self.joints[TOP].setSpeed(Normal_SPEED)
            self.joints[MIDDLE].setSpeed(Normal_SPEED)
            self.joints[BOTTOM].setSpeed(Normal_SPEED)

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


if __name__=="__main__":
    venom = Quadruped(servoId)
    venom.setParams(dirVector,FixedPoints)
    # venom.walk(TROT,-0.2)
    venom.go2SlopeStartPosition(2)
    input("Press Enter")

    while True:
        venom.Creep(True,2)