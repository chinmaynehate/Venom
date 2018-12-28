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
    def __init__(self,servoIndexes=None):
        servo.init()                                #Open Port and Set Baud Rate
        self.Legs = [Leg(),Leg(),Leg(),Leg()]
        if servoIndexes!=None:
            self.setID(servoIndexes)
            
        self.DEFAULT_X = 5
        self.DEFAULT_Z = -15
        self.Y_MAX = 9
        self.Y_MIN = -0.5
        self.Y_MEAN = (self.Y_MIN+self.Y_MAX)/2  

        self.totalShiftSize = (self.Y_MAX-self.Y_MEAN)
        self.stanceIncrements = 0.5

        # Delays
        self.shiftAllInterDelay = 0.1


    def setID(self,ID):
        for i in range(0,4):
                self.Legs[i].setIDs(ID[i*3:i*3+3])

    def setParams(self,dirParams,fixedPtsParams):
        for i in range(0,4):
                self.Legs[i].setParams(dirParams[i*3:i*3+3],fixedPtsParams[i*3:i*3+3])

    def stanceBackward(self,increments,totalShift):
        currentShift = 0

        while currentShift < self.totalShiftSize:
            currentShift += increments
            self.Legs[A].setLegPos(self.DEFAULT_X ,self.currentYa - currentShift ,self.DEFAULT_Z)
            self.Legs[B].setLegPos(self.DEFAULT_X ,self.currentYb - currentShift ,self.DEFAULT_Z)
            self.Legs[C].setLegPos(self.DEFAULT_X ,self.currentYc - currentShift ,self.DEFAULT_Z)
            self.Legs[D].setLegPos(self.DEFAULT_X ,self.currentYd - currentShift ,self.DEFAULT_Z)
            time.sleep(self.shiftAllInterDelay)

        self.currentYa = self.currentYa - currentShift + increments * 0
        self.currentYb = self.currentYb - currentShift + increments * 0
        self.currentYc = self.currentYc - currentShift + increments * 0
        self.currentYd = self.currentYd - currentShift + increments * 0

    def go2MotionStartPos(self):
        print("Going to Starting Position")
        self.Legs[A].setLegPos(self.DEFAULT_X, self.Y_MEAN,self.DEFAULT_Z)
        self.Legs[B].setLegPos(self.DEFAULT_X, self.Y_MIN,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MEAN,self.DEFAULT_Z)

        self.currentYa =  self.Y_MEAN
        self.currentYb =  self.Y_MIN
        self.currentYc = -self.Y_MIN
        self.currentYd = -self.Y_MEAN

    def Creep(self):

        # Step 1 - Step Leg B Forward
        self.Legs[B].StepInY(self.Y_MIN,self.Y_MAX)

        input("Press Any Key to Push")
        # Step 1.2 - Push Forward
        self.stanceBackward(self.stanceIncrements,self.totalShiftSize)


        # Step 2 - Step Leg D Forward
        self.Legs[D].StepInY(-self.Y_MAX,-self.Y_MIN)

        # Step 2.1 - Step Leg A Forward
        self.Legs[A].StepInY(self.Y_MIN,self.Y_MAX)

        input("Press Any Key to Push")
        # Step 2.2 - Push Forward
        self.stanceBackward(self.stanceIncrements,self.totalShiftSize)

        # Step 3 - Step Leg C Forward
        self.Legs[C].StepInY(-self.Y_MAX,-self.Y_MIN)


    def walk(self):
        self.go2MotionStartPos()
        while True:
            self.Creep()
    

class Leg:
    def __init__(self,ID = None):
        self.joints = [servo.SmartServo(),servo.SmartServo(),servo.SmartServo()]

        if (ID != None):
            self.setIDs(ID)
    
        self.Z_STEP_UP_HEIGHT = -10
        self.STEP_UP_DELAY = 1
        self.x = 5


    def setIDs(self,ID):
        self.joints[TOP].setID(ID[TOP])
        self.joints[MIDDLE].setID(ID[MIDDLE])
        self.joints[BOTTOM].setID(ID[BOTTOM])

    
    def setParams(self,dirParams,fixedPointParams):
        self.joints[TOP].setParams(dirParams[TOP],fixedPointParams[TOP])
        self.joints[MIDDLE].setParams(dirParams[MIDDLE],fixedPointParams[MIDDLE])
        self.joints[BOTTOM].setParams(dirParams[BOTTOM],fixedPointParams[BOTTOM])

        self.joints[BOTTOM].setSpeed(400)
        
        

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
        input("Press Any Key")
        # Pickup the Leg
        self.setLegPos(5,from_y,self.Z_STEP_UP_HEIGHT)
        # self.setLegPos(self.x,from_y,-4.5)
        time.sleep(self.STEP_UP_DELAY)
        input("Press Any Key")
        # Rotate Top
        self.setLegPos(5,to_y,self.Z_STEP_UP_HEIGHT)
        # self.setLegPos(self.x,to_y,-4.5)
        self.y = to_y 
        time.sleep(self.STEP_UP_DELAY)
        input("Press Any Key")
        # Drop Down the Leg
        self.setLegPos(5,to_y,-15)
        # self.setLegPos(self.x,to_y,-11.5)
        # time.sleep(self.STEP_UP_DELAY)




if __name__=="__main__":
    venom = Venom(k.servoId)
    venom.setParams(k.dirVector,k.FixedPoints)
    venom.walk()
