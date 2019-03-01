from sympy import fourier_series,symbols,Piecewise,lambdify
import matplotlib.pyplot as plt
import numpy as np

def constructTrajectory_FourierSeries():
    dc = 0.8
    dt = 0.025
    T = 1.0
    stroke = 12.0



    a3 = (-4.0*(stroke/2.0+stroke/dc*dt)-2.0*stroke/dc*(T-dc-2.0*dt))/(T-dc-2.0*dt)**3.0;
    a2 = -3.0/2.0*a3*(T-dc-2.0*dt);
    a1 = -stroke/dc;
    a0 = -(stroke/2.0+stroke/dc*dt);

    t_current = symbols('t_current')

    fx1 = (stroke/2.0 + stroke/dc*(-1* t_current))
    fx2 = a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0; #stride 
    fx3 = (stroke/2.0 + stroke/dc*(-1* t_current))

    print("Calculating Piecewise Fourier Series")
    FourierX = Piecewise( (fx1,t_current<=dc+dt) ,  (fx2 ,t_current<=T-dt ) , (fx3 , t_current<=1)   )

    print("\n")
    print("FOurier piecewise is    ",FourierX)
    print("\n")
   
    FourierXSeries = fourier_series( FourierX , (t_current,0,1)  )
    p = FourierXSeries.truncate(100)
    print("FourierX Series Calculated: ", p)

    lp = np.array(range( 0 , 100))
    for i in lp:

        current = p.subs(t_current,i/100)
           plt.scatter( i/100 , current )

    plt.show()

   


if __name__=="__main__":
    constructTrajectory_FourierSeries()