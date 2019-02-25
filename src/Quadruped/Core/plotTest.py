import matplotlib.pyplot as plt
import numpy as np


def plotX():
    dc = 0.8
    dt = 0.025
    T = 1.0
    stroke = 12.0

    Xs = []
    Ys = []

    SampleDensity = 1000
    t1 = np.array(range(0,SampleDensity))/(SampleDensity*1.0)

    a3 = (-4.0*(stroke/2.0+stroke/dc*dt)-2.0*stroke/dc*(T-dc-2.0*dt))/(T-dc-2.0*dt)**3.0;
    a2 = -3.0/2.0*a3*(T-dc-2.0*dt);
    a1 = -stroke/dc;
    a0 = -(stroke/2.0+stroke/dc*dt);

    for t_current in t1:
        t_current = t_current%1

        if t_current<=(dc+dt):
            x = stroke/2.0 + stroke/dc*(-t_current)
        elif t_current<=(T-dt):
            x = a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0; #stride 
        else:
            x= stroke/2.0 + stroke/dc*(T-t_current);          #velocity extension for 'dt'seconds before stride 
        
        Xs.append(x)
        Ys.append(t_current)

    
    # plt.plot(Ys,Xs)

    return Xs
    # plt.show()

def plotY():
    dc = 0.8
    dt = 0.025
    T = 1.0
    stroke = 12.0
    ht = 3.5;

    Xs = []
    Ys = []

    SampleDensity = 1000
    t1 = np.array(range(0,SampleDensity))/(SampleDensity*1.0)

    a3 = (-4.0*(stroke/2.0+stroke/dc*dt)-2.0*stroke/dc*(T-dc-2.0*dt))/(T-dc-2.0*dt)**3.0;
    a2 = -3.0/2.0*a3*(T-dc-2.0*dt);
    a1 = -stroke/dc;
    a0 = -(stroke/2.0+stroke/dc*dt);

    Amplitude=0

    for t_current in t1:
        t_current = t_current%1

        if t_current<=dc:
            x= -18.0 +Amplitude #stance
        else:
            x = -18.0 +Amplitude + 16.0*ht/(T-dc)**2.0*(t_current-dc)**2.0 - 32.0*ht/(T-dc)**3.0*(t_current-dc)**3.0 +16.0*ht/(T-dc)**4.0*(t_current-dc)**4.0;   #stride

        x*=1/8.0
        
        Xs.append(x)
        Ys.append(t_current)

    
    # plt.plot(Ys,Xs)

    # plt.show()
    return Xs



if __name__=="__main__":
    Xs,Ys = plotX(),plotY()
    plt.plot(Xs,Ys)
    plt.grid()
    plt.show()