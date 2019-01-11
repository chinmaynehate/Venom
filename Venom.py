import smartServo as servo
import kinematics as ik
import constants as k
from constants import TOP,MIDDLE,BOTTOM
import time 
import ImageProcessing as ip
import cv2
from helpers import calculateYs


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

        self.setDefaults()
        self.setControlSystemParams()
            
        

    def setDefaults(self):
        # Bot Motion Params (Cordinates)
        self.DEFAULT_X =5
        self.DEFAULT_Z = -17
        self.Y_MAX = 7
        self.Y_MIN = -2
        self.Y_MEAN = (self.Y_MIN+self.Y_MAX)/2  
        self.Z_STEP_UP_HEIGHT = -15


        self.totalShiftSize = (self.Y_MAX-self.Y_MIN)/2
        self.stanceIncrements = 2.5

        # Delays
        self.shiftAllInterDelay = 0.01
        self.trotDelay = 0.09

    def setControlSystemParams(self):
        self.Kp = 1

        self.Y_MAX_adjusted = 0
        self.Y_MIN_adjusted = 0




    def setID(self,ID):
        for i in range(0,4):
                self.Legs[i].setIDs(ID[i*3:i*3+3])

    def setParams(self,dirParams,fixedPtsParams):
        for i in range(0,4):
                self.Legs[i].setParams(dirParams[i*3:i*3+3],fixedPtsParams[i*3:i*3+3])

    def stanceBackward(self,increments,totalShift):
        currentShift = 0

        
        self.currentYa = self.currentYa - totalShift 
        self.currentYb = self.currentYb - totalShift 
        self.currentYc = self.currentYc - totalShift 
        self.currentYd = self.currentYd - totalShift


        # FOR Creep Differential
        # self.currentYa = self.currentYa - totalShift 
        # self.currentYb = self.currentYb - 2
        # self.currentYc = self.currentYc - 2 
        # self.currentYd = self.currentYd - totalShift 


        # self.currentYa = self.currentYa - 2 
        # self.currentYb = self.currentYb - totalShift
        # self.currentYc = self.currentYc - totalShift
        # self.currentYd = self.currentYd - 2 


        # For Normal Drive
        self.Legs[A].setLegPos(self.DEFAULT_X ,self.currentYa ,self.DEFAULT_Z)
        self.Legs[B].setLegPos(self.DEFAULT_X ,self.currentYb  ,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X ,self.currentYc ,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X ,self.currentYd  ,self.DEFAULT_Z)


        # For Sand Dune
        # self.Legs[A].setLegPos(self.Legs[A].x ,self.currentYa ,self.Legs[A].z)
        # self.Legs[B].setLegPos(self.Legs[B].x ,self.currentYb  ,self.Legs[B].z)
        # self.Legs[C].setLegPos(self.DEFAULT_X ,self.currentYc ,self.DEFAULT_Z)
        # self.Legs[D].setLegPos(self.DEFAULT_X ,self.currentYd  ,self.DEFAULT_Z)
        
        
        time.sleep(0.1)

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

        

    def Trot_followLine(self):
        global_angle, average_error,_,_,_,_ = ip.getSlopeError()

        print ("Errors:",global_angle,average_error)


        error=average_error
        if error >0:
            # self.TrotLeft()
            print("Going Left")
        elif error <0:
            # self.TrotRight()
            print("Going Right")

        self.Y_MAX_adjusted,self.Y_MIN_adjusted=calculateYs(global_angle,average_error)
        print("Ymax :",self.Y_MAX_adjusted," , Ymin :" , self.Y_MIN_adjusted)

        while True:
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('e'):
                break
            elif key == ord('q'):
                cv2.destroyAllWindows()
                quit()

        
        

        if error >0:
            self.TrotLeft(correction=True)
            print("Going Left")
        elif error <0:
            self.TrotRight(correction=True)
            print("Going Right")



    def Trot(self):
        global_angle, average_error,_,_,_,_ = IP.getSlopeError()
        
        print (global_angle,average_error)
        # input()
        # Step 1 - Step Leg B And D Forward and PushBack Leg A and C Back
        
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")


    def TrotStrafeLeft(self):
        self.X_MAX = 0
        self.X_MIN = 0
        self.DEFAULT_Y = 0
        
        # Step 1 - Step Leg B And D Left and PushBack Leg A and C Right    
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")

    def TrotStrafeRight(self):
        self.X_MAX = 0
        self.X_MIN = 0
        self.DEFAULT_Y = 0
        
        # Step 1 - Step Leg B And D Left and PushBack Leg A and C Right    
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.X_MIN,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.X_MAX,self.DEFAULT_Y,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.X_MIN,self.DEFAULT_Y,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.X_MAX,self.DEFAULT_Y,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")

    def TrotReverse(self):
        # Step 1 - Step Leg B And D Forward and PushBack Leg A and C Back
        
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")


    def TrotClimb(self):
        pass                #TODO



    def TrotLeft(self,correction=False):
        
        if correction:
            self.Y_MAX2 = self.Y_MAX_adjusted
            self.Y_MIN2 = self.Y_MIN_adjusted
        else:
            self.Y_MAX2 = 3
            self.Y_MIN2 = -1.5
        
        # Step 1 - Step Leg B And D Forward and PushBack Leg A and C Back
        
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX2,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN2,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN2,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN2,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN2,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX2,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX2,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX2,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")


    def TrotRight(self,correction=False):
        
        if correction:
            self.Y_MAX2 = self.Y_MAX_adjusted
            self.Y_MIN2 = self.Y_MIN_adjusted
        else:
            self.Y_MAX2 = 3
            self.Y_MIN2 = -1.5


        # Step 1 - Step Leg B And D Forward and PushBack Leg A and C Back
        
        # 1.Pickup the Leg

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN2,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")
        # 1.Rotate Top
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX2,self.Z_STEP_UP_HEIGHT)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.Z_STEP_UP_HEIGHT)

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX2,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed2")
        # 1.Drop Down the Leg
        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MAX2,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MIN,self.DEFAULT_Z)
        time.sleep(self.trotDelay)
        # input("Enter to Proceed")

        # Step 2 - Step Leg A And C Forward and PushBack Leg B and D Back
        
        # 1.Pickup the Leg

        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MIN,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MAX2,self.Z_STEP_UP_HEIGHT)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed3")
        # 1.Rotate Top
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.Z_STEP_UP_HEIGHT)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN2,self.Z_STEP_UP_HEIGHT)

        self.Legs[B].setLegPos(self.DEFAULT_X,self.Y_MIN2,self.DEFAULT_Z)
        self.Legs[D].setLegPos(self.DEFAULT_X,-self.Y_MAX,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed")
        # 1.Drop Down the Leg
        self.Legs[A].setLegPos(self.DEFAULT_X,self.Y_MAX,self.DEFAULT_Z)
        self.Legs[C].setLegPos(self.DEFAULT_X,-self.Y_MIN2,self.DEFAULT_Z)

        time.sleep(self.trotDelay)
        # input("Enter to Proceed1")


    def walk(self):
        self.go2MotionStartPos()
        input("Enter to Begin Motion")

        while True:
            self.Trot_followLine()



 
            
class Leg:
    def __init__(self,ID = None):
        self.joints = [servo.SmartServo(),servo.SmartServo(),servo.SmartServo()]

        if (ID != None):
            self.setIDs(ID)
    
        self.Z_STEP_UP_HEIGHT = -9
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


if __name__=="__main__":
    venom = Venom(k.servoId)
    venom.setParams(k.dirVector,k.FixedPoints)
    venom.walk()
