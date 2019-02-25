import matplotlib.pyplot as plt
from sympy import fourier_series,Piecewise,symbols,lambdify,log
import numpy as np

if __name__ == "__main__":
    x = symbols('x')
    f = x**2
    g = log(x)
    p = Piecewise( (0,x<-1) , (f,x<1),(100,True) )

    # p = lambdify((x),p)
    
    lp = np.array(range( -20 , 20))
    for i in lp:
        ix = float( p.subs(x,i/1.0) )
        plt.scatter(ix,i)
        print(ix,",Iteration:",i )
    # print(p(2))
    plt.show()