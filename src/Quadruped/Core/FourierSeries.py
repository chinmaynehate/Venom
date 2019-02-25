from sympy import fourier_series,symbols

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

    fx1 = lambda t_current:(stroke/2.0 + stroke/dc*(-t_current))
    fx2 = lambda t_current:a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0; #stride 
    fx3 = lambda t_current:(stroke/2.0 + stroke/dc*(-t_current))

    print("calculating Fourier1")
    Fourier1 = fourier_series( fx1(t_current) , (t_current,0,dc+dt)   )
    print("calculating Fourier2")
    Fourier2 = fourier_series( fx2(t_current) , (t_current,dc+dt,T-dt )    )
    print("calculating Fourier3")
    Fourier3 = fourier_series( fx3(t_current) , (t_current,T-dt,1)    )
    # f2 = fourier_series( (a0 + a1*(t_current-(dc+dt)) + a2*(t_current-(dc+dt))**2.0 + a3*(t_current-(dc+dt))**3.0) )
    print("Fourier1 = ",Fourier1.truncate())
    print("\n\n\n")
    print("Fourier2 = ",Fourier2.truncate())
    print("\n\n\n")
    print("Fourier3 = ",Fourier3.truncate())


    FourierTotal = Fourier1+Fourier2+Fourier3
    print(FourierTotal)



if __name__=="__main__":
    constructTrajectory_FourierSeries()