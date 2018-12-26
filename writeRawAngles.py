import smartServo as servo

if __name__ == '__main__':
    # Open port
    print("Opening Port!")
    if servo.init():
    	#take Id for the Servos as Input

        Id = int(input("Enter The Bot ID(Enter -1 to Quit):"))
        print("Enabling Torque on the Servo Id [%d]",Id)
        servo.enable(Id)
        while True:
            exAngle = int(input("Enter the Servo Angle(0-1023)"))
            servo.setSpeed(Id,50)
            servo.writeRawAngle(Id,exAngle)
            print("------------------------------------------------------------------")
        print("\n[+] Disabling")
