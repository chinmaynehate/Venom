import Quadruped
import Server
from constants import *
import time



if __name__ == "__main__":
    venom = Quadruped.Quadruped(servoId)
    venom.setParams(dirVector,FixedPoints)
    venom.go2CreepStartPosition()
    server = Server.Server()
    server.setPort(21574)
    server.start()

    while True:
        ipt = server.getInput()
        angle,force = ipt[0],ipt[1]

        print("Received Input:",ipt)
        if force > 10:                      #Set Threshold for Processing
            if(angle>=0 and angle<=180):       
                # Map the Angle and get the Differential Factor
                diffFactor = -((angle-90.0)/90)
                if diffFactor <0:
                    diffFactor= -diffFactor**2
                else:
                    diffFactor=diffFactor**2

                
                print("Differential Factor:",diffFactor)
                # time.sleep(0.5)

                venom.walk(TROT,diffFactor=diffFactor)

            else:                           #Bot Backwards
                # Map the Angle and get the Differential Factor
                diffFactor = -((angle-270.0)/90)
                if diffFactor <0:
                    diffFactor= diffFactor**2
                else:
                    diffFactor=-diffFactor**2

                
                print("Differential Factor:",diffFactor)
                # time.sleep(0.5)

                venom.walk(TROT_BACK,diffFactor=diffFactor)
        else:
            print("Force Not Sufficient..")
            # time.sleep(0.4)
        time.sleep(0.4)

                
                




