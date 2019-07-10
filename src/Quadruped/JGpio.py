import RPi.GPIO as GPIO
import time
from constants import *



def setInput(pin):
    try:
        GPIO.setup(pin, GPIO.IN)  # set pin as an input pin
    except:
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
        GPIO.setup(pin, GPIO.IN)  # set pin as an input pin


def readInput(pin):
    value = GPIO.input(pin)
    if value == GPIO.HIGH:
        return False
    else:
        return True


if __name__=="__main__":
    setInput(BUMPA)
    setInput(BUMPB)
    setInput(BUMPC)
    setInput(BUMPD)


    while True:
        print(readInput(BUMPA),readInput(BUMPB),readInput(BUMPC),readInput(BUMPD))
        # time.sleep(0.1)



