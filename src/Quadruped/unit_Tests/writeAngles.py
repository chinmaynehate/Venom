import board
import busio
from adafruit_servokit import ServoKit

i2c = busio.I2C(board.SCL_1,board.SDA_1)

print("Connecting to the I2C Bus......")
kit1 = ServoKit(channels=16,i2c=i2c,address=0x40)
kit2= ServoKit(channels=16,i2c=i2c,address=0x41)

print("Kit Complete !!!")

kit = int(input("Enter the Servo Kit:"))

def run():
    while True:
        if kit==1:
            index =  int(input("Enter Servo Index:"))
            if(index!=-1):
                angle = int(input("Enter the Servo Angle:"))
                kit1.servo[index].set_pulse_width_range(500,2500)
                kit1.servo[index].angle=angle
            else:
                break
        elif kit==2:
            index =  int(input("Enter Servo Index:"))
            if(index!=-1):
                angle = int(input("Enter the Servo Angle:"))
                kit2.servo[index].set_pulse_width_range(500,2500)
                kit2.servo[index].angle=angle
            else:
                break;
        else:
            print("Invalid Kit!!!")

if __name__=="__main__":
    while True:
        run()
