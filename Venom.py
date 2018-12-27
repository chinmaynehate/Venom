import smartServo as servo
import kinematics as ik
import constants as k
from constants import A,B,C,D
import time 

class Venom:
    def __init__(self,servoIndexes=None,totalShiftSize = None,shiftStepSize = None,shiftAllDelay=None):
        self.Legs = [Leg(),Leg(),Leg(),Leg()]
        if servoIndexes!=None:
            self.setID(A,servoIndexes[0],servoIndexes[1],servoIndexes[2])
            self.setID(B,servoIndexes[3],servoIndexes[4],servoIndexes[5])
            self.setID(C,servoIndexes[6],servoIndexes[7],servoIndexes[8])
            self.setID(D,servoIndexes[9],servoIndexes[10],servoIndexes[11])

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


    def setID(self,Leg,ID1,ID2,ID3):
        self.Legs[Leg].setIDs(ID1,ID2,ID3)

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
    def __init__(self,ID1=None,ID2=None,ID3=None):
        self.servoTop    = servo.SmartServo()
        self.servoMiddle = servo.SmartServo()
        self.servoBottom = servo.SmartServo()

        if (ID1 != None and ID2 != None and ID3 != None):
            self.setIDs(ID1,ID2,ID3)
    
        self.Z_STEP_UP_HEIGHT = 0
        self.STEP_UP_DELAY = 0


    def setIDs(self,ID1,ID2,ID3):
        self.servoTop.setID(ID1)
        self.servoMiddle.setID(ID2)
        self.servoBottom.setID(ID3)

    def setLegPos(self,x,y,z):
        t1,t2,t3,isPossible = ik.getInverse(x,y,z)

        if isPossible:
            # Store the Current Value of X,Y,Z
            self.x = x
            self.y = y
            self.z = z

            self.servoTop.writeAngle(t1)
            self.servoMiddle.writeAngle(t2)
            self.servoBottom.writeAngle(t3)
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




