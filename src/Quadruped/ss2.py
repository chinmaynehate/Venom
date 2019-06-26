import numpy as np
import time
import math
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)
delay = 0.4



kit.servo[0].set_pulse_width_range(500,2500)
kit.servo[0].angle=50                                          
