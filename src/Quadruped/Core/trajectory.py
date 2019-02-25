import numpy as np


def sine(stepLength,stepHeight,theta):
    return ( np.sin(np.pi * theta / stepLength) * stepHeight)

# def complexSine(stepLength,stepHeight,time,TimeTaken):
    # return (stepHeight*(time/TimeTaken - (np.sin(2*np.pi*time/TimeTaken))/(np.pi*2) )  )
