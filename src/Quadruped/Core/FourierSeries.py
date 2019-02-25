from sympy import *

def constructTrajectory_FourierSeries():
    dc = 0.8
    dt = 0.025
    T = 1.0
    stroke = 12.0



    a3 = (-4.0*(stroke/2.0+stroke/dc*dt)-2.0*stroke/dc*(T-dc-2.0*dt))/(T-dc-2.0*dt)**3.0;
    a2 = -3.0/2.0*a3*(T-dc-2.0*dt);
    a1 = -stroke/dc;
    a0 = -(stroke/2.0+stroke/dc*dt);

    t_current = fourier()

    if t_current<=(dc+dt):
        x = stroke/2.0 + stroke/dc*(-t_current)
    elif t_current<=(T-dt):
        x = a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0; #stride 
    else:
        x= stroke/2.0 + stroke/dc*(T-t_current);          #velocity extension for 'dt'seconds before stride 
        

    
    # plt.plot(Ys,Xs)

    return Xs



