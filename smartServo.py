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

def readRawAngle(ID):
    return servos.read_pos(ID,0)

if __name__=="__main__":
    pass
