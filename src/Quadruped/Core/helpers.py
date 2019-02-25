from sympy import *

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


def fourier_series(f, frange, t, t_0):   
    k = symbols('k', integer=True, positive=True, zero=False)
    
    a_k = 2/t_0*(integrate(f * cos(2*pi/t_0*k*t), [t, frange[0], frange[1]]))
    a_k = [a_k.subs(k, i) for i in range(1, 10)]

    b_k = 2/t_0*(integrate(f * sin(2*pi/t_0*k*t), [t, -t_0/2, t_0/2]))
    b_k = [b_k.subs(k, i) for i in range(1, 10)]

    # Amplitude
    d_k = [sqrt(a**2 + b**2) for a, b in zip(a_k, b_k)]

    # Phase
    phi_k = [atan(b/a) for a, b in zip(a_k, b_k)]
    
    return a_k, b_k, d_k, phi_k