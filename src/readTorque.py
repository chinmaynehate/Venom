import smartServo as servo

if __name__=="__main__":
    servo.init()
    ID=9
    print(servo.readTorque(ID))