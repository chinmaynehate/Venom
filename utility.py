
def cMap(value,inputLow,inputHigh,outputLow,outputHigh,constrain=False):
    mappedValue = (value - inputLow) * (outputHigh-outputLow)/(inputHigh-inputLow) + outputLow
    if constrain:
        if mappedValue<outputLow:
            mappedValue=outputLow
        elif mappedValue>outputHigh:
            mappedValue=outputHigh
    return mappedValue


