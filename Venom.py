import smartServo as servo
import kinematics as ik
import constants as k
from constants import TOP,MIDDLE,BOTTOM
import time 

# Leg Constants
A=0
B=1
C=2
D=3


class Venom:
    def __init__(self,servoIndexes=None,totalShiftSize = None,shiftStepSize = None,shiftAllDelay=None):
        self.Legs = [Leg(),Leg(),Leg(),Leg()]
        if servoIndexes!=None:
            self.setID(servoIndexes)

        if totalShiftSize==None:
            self.totalShiftSize = 0
        else:
            self.totalShiftSize = totalShiftSize

        if shiftStepSize==None:
            self.shiftStepSize = 0
        else:
            self.shiftStepSize = shiftStepSize

        if shiftAllDelay==None:
            self.shiftAllDelay = 0
        else:
            self.shiftAllDelay = shiftAllDelay

        self.currentYa = 0
        self.currentYb = 0
        self.currentYc = 0
        self.currentYd = 0


    def setID(self,ID):
        for i in range(0,3):
                self.Legs[i].setIDs(ID[i:i+2])

    def setParams(self,dirParams,fixedPtsParams):
        for i in range(0,3):
                self.Legs[i].setParams(dirParams[i:i+2],fixedPtsParams[i:i+2])


    def stanceBackward(self,increments):
        currentShift = 0
        # Temp Vars
        x=0
        y=0
        z=0

        while currentShift < self.totalShiftSize:
            currentShift += increments
            self.Legs[A].setLegPos(x,self.currentYa - currentShift ,z)
            self.Legs[B].setLegPos(x,self.currentYb - currentShift ,z)
            self.Legs[C].setLegPos(x,self.currentYc - currentShift ,z)
            self.Legs[D].setLegPos(x,self.currentYd - currentShift ,z)
            time.sleep(self.shiftAllDelay)

        self.currentYa = self.currentYa - currentShift + increments
        self.currentYb = self.currentYb - currentShift + increments
        self.currentYc = self.currentYc - currentShift + increments
        self.currentYd = self.currentYd - currentShift + increments

    def go2StartPos(self):
        print("Going to Starting Position")
        # self.Legs[0].setLegPos(x,y,z)
        # self.Legs[1].setLegPos(x,y,z)
        # self.Legs[2].setLegPos(x,y,z)
        # self.Legs[3].setLegPos(x,y,z)

    def Creep(self):

        # Step 1 - Step Leg B Forward
        self.Legs[B].StepInY(0,0)

        # Step 1.2 - Push Forward
        self.stanceBackward(0)

        # Step 2 - Step Leg D Forward
        self.Legs[D].StepInY(0,0)

        # Step 2.1 - Step Leg A Forward
        self.Legs[A].StepInY(0,0)

        # Step 2.2 - Push Forward
        self.stanceBackward(0)

        # Step 3 - Step Leg C Forward
        self.Legs[C].StepInY(0,0)
    

class Leg:
    def __init__(self,ID = None):
        self.joints = [servo.SmartServo(),servo.SmartServo(),servo.SmartServo()]

        if (ID != None):
            self.setIDs(ID)
    
        self.Z_STEP_UP_HEIGHT = 0
        self.STEP_UP_DELAY = 0


    def setIDs(self,ID):
        self.joints[TOP].setID(ID[TOP])
        self.joints[MIDDLE].setID(ID[MIDDLE])
        self.joints[BOTTOM].setID(ID[BOTTOM])
    
    def setParams(self,dirParams,fixedPointParams):
        self.joints[TOP].setParams(dirParams[TOP],fixedPointParams[TOP])
        self.joints[MIDDLE].setParams(dirParams[MIDDLE],fixedPointParams[MIDDLE])
        self.joints[BOTTOM].setParams(dirParams[BOTTOM],fixedPointParams[BOTTOM])
        
        

    def setLegPos(self,x,y,z):
        t1,t2,t3,isPossible = ik.getInverse(x,y,z)

        if isPossible:
            # Store the Current Value of X,Y,Z
            self.x = x
            self.y = y
            self.z = z

            self.joints[TOP].writeAngle(t1)
            self.joints[MIDDLE].writeAngle(t2)
            self.joints[BOTTOM].writeAngle(t3)
            
        else:
            print("Inverse Not Possible")
        

    def StepInY(self,from_y,to_y):
        # Pickup the Leg
        self.setLegPos(self.x,from_y,self.Z_STEP_UP_HEIGHT)
        time.sleep(self.STEP_UP_DELAY)
        # Rotate Top
        self.setLegPos(self.x,to_y,self.Z_STEP_UP_HEIGHT)
        self.y = to_y 
        time.sleep(self.STEP_UP_DELAY)
        # Drop Down the Leg
        self.setLegPos(self.x,to_y,self.z)
        time.sleep(self.STEP_UP_DELAY)




