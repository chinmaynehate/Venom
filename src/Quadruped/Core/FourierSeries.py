from sympy import fourier_series,symbols,Piecewise,lambdify
import matplotlib.pyplot as plt
import numpy as np

def constructTrajectory_FourierSeriesX():
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

    print("Calculating Piecewise Func for X")
    FourierX = Piecewise( (fx1,t_current<=dc+dt) ,  (fx2 ,t_current<=T-dt ) , (fx3 , t_current<=1)   )

    print("\n")
    print("Piecewise func for X is    ",FourierX)
    print("\n")
   
    FourierXSeries = fourier_series( FourierX , (t_current,0,1)  )
    p = FourierXSeries.truncate(100)
    print("FourierX Series Calculated: ", p)

    lp = np.array(range( 0 , 100))
    for i in lp:

        currentX = p.subs(t_current,i/100)
        plt.scatter( i/100 , currentX )

    plt.show()


    
   
def constructTrajectory_FourierSeriesY():
    dc = 0.8
    ht = 3.5
    T = 1.0

    t_current = symbols('t_current')
    fy1 = -18
    fy2 = -18 + 0 + 16*ht/(T-dc)**2*(t_current-dc)**2 - 32*ht/(T-dc)**3*(t_current-dc)**3 + 16*ht/(T-dc)**4*(t_current-dc)**4 
    
    print("Calculating Piecewise func for Y")
    FourierY = Piecewise((fy1,t_current <= dc),(fy2, t_current<=1))
    print("\n")
    print("Piecewise func for Y is",FourierY)
    FourierYSeries = fourier_series(FourierY,(t_current,0,1))
    q = FourierYSeries.truncate(100)
    print("FourierY Series calculated:  ",q)
   
    lq = np.array(range( 0 , 100))
    for i in lq:

        currentY = q.subs(t_current,i/100)
        plt.scatter( i/100 , currentY )

    plt.show()

def constructTrajectory_FourierSeriesXY():
    # Constants
    TRUNCATEX = 10
    TRUNCATEY = 10
    dc = 0.8
    dt = 0.025
    T = 1.0
    stroke = 12.0
    ht = 3.5
    a3 = (-4.0*(stroke/2.0+stroke/dc*dt)-2.0*stroke/dc*(T-dc-2.0*dt))/(T-dc-2.0*dt)**3.0;
    a2 = -3.0/2.0*a3*(T-dc-2.0*dt);
    a1 = -stroke/dc;
    a0 = -(stroke/2.0+stroke/dc*dt);
 
    # Create a symbol t_current 
    t_current = symbols('t_current')

    # Functions for computing X(t_current)
    fx1 = (stroke/2.0 + stroke/dc*(-1* t_current))
    fx2 = a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0; #stride 
    fx3 = (stroke/2.0 + stroke/dc*(-1* t_current))

    # Functions for computing Y(t_current)
    fy1 = -18
    fy2 = -18 + 0 + 16*ht/(T-dc)**2*(t_current-dc)**2 - 32*ht/(T-dc)**3*(t_current-dc)**3 + 16*ht/(T-dc)**4*(t_current-dc)**4 
    
    # Finding the piecewise function for X i.e assimilating fx1, fx2 and fx3 together
    print("Calculating Piecewise Func for X")
    FourierX = Piecewise( (fx1,t_current<=dc+dt) ,  (fx2 ,t_current<=T-dt ) , (fx3 , t_current<=1)   )
    print("\n")
    print("Piecewise func for X is    ",FourierX)
    print("\n")
    
    # Calculating Fourier Series for X(t)
    FourierXSeries = fourier_series( FourierX , (t_current,0,1)  )
    p = FourierXSeries.truncate(TRUNCATEX)
    print("FourierX Series Calculated: ", p)



    # Finding the piecewise function for Y i.e assimilating fy1, fy2 and fy3 together
    print("Calculating Piecewise func for Y")
    FourierY = Piecewise((fy1,t_current <= dc),(fy2, t_current<=1))
    print("\n")
    print("Piecewise func for Y is",FourierY)

    # Calculating Fourier Series for Y(t)
    FourierYSeries = fourier_series(FourierY,(t_current,0,1))
    q = FourierYSeries.truncate(TRUNCATEY)
    print("FourierY Series calculated:  ",q)


    # Plotting X and Y
    lxy = np.array(range( 0 , 100))
    for i in lxy:

        currentX = p.subs(t_current,i/100)
        currentY = q.subs(t_current,i/100)
        plt.scatter( currentX, currentY)
        print("Progress = ",i)

    plt.show()

   



if __name__=="__main__":
    constructTrajectory_FourierSeriesXY()
    # constructTrajectory_FourierSeriesX()
    #constructTrajectory_FourierSeriesY()sudo apt-get install python3-tk 
