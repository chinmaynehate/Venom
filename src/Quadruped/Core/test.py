import board
import busio
# import adafruit_pca9685

i2c = busio.I2C(board.SCL,board.SDA)
# hat = adafruit_pca9685.PCA9685(i2c)

# channel = hat.channel[0]

from adafruit_servokit import ServoKit

print("Connecting to the I2C Bus......")
kit1 = ServoKit(channels=16,i2c=i2c,address=0x40)
kit2= ServoKit(channels=16,i2c=i2c,address=0x41)

print("Kit Complete !!!")

while True:
    index = int(input("Enter the Servo Index:"))
    angle = int(input("Enter the Servo Angle:"))
    kit2.servo[index].angle=angle

