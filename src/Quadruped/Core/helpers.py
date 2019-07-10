# from sympy import *

def cmap(value,inputLow,inputHigh,outputLow,outputHigh,constrain=False):
    mappedValue = (value - inputLow) * (outputHigh-outputLow)/(inputHigh-inputLow) + outputLow
    if constrain:
        if mappedValue<outputLow:
            mappedValue=outputLow
        elif mappedValue>outputHigh:
            mappedValue=outputHigh
    return mappedValue


def calculateYs(angleError,lateralError):
        absoluteError = abs(lateralError)
        YMax = 7 -  cmap(absoluteError,0,50,0,6,constrain=True)
        YMin = -2 + cmap(absoluteError,0,50,0,1.5,constrain=True)

        return YMax,YMin

