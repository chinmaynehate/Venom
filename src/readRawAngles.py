import smartServo as servo
import time

if __name__ == '__main__':
    
    # Open port
    print("Opening Port!")
    if servo.init():
    	
        botId = int(input("Enter The Bot ID:"))
        print("disabling Torque on the Servo Id [%d]",botId)
        servo.disable(botId)
        
        try:
            while True:
                # print("Angle:",sep="")
                print(servo.readRawAngle(botId))
        except KeyboardInterrupt:
            pass
        
        print("\n[+] Disabling")





