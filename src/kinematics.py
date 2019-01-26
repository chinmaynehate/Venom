import numpy as np
import constants as k
import math

def getInverse(x,y,z):
    l1 = k.linkLength[0]
    l01= k.linkLength[1]
    l2 = k.linkLength[2]
    l3 = k.linkLength[3]

    r1 = l01
    r2 = l2 
    r3 = l3

    z+=l1   #Shift of Origin 
    
    #print(2**2)

    try:
        th1 = math.atan2(y,x)

        A = -z
        B = r1 -(x*np.cos(th1) + y*np.sin(th1))
        D = (2*r1*(x*np.cos(th1) + y*np.sin(th1)) + (r3**2) - (r2**2) - (r1**2) -(z**2) - ((x*np.cos(th1)+y*np.sin(th1))**2) )/(2*r2)

        phi = math.atan2(B,A)

        # print(A,B,D)

        th02 = -phi + math.atan2(D , + math.pow(((A**2)+(B**2) - (D**2)),0.5)  )
        th12 = -phi + math.atan2(D , - math.pow(((A**2)+(B**2) - (D**2)),0.5)  )
        
        th03 = np.arctan2( z-r2*np.sin(th02) , x*np.cos(th1) + y*np.sin(th1) - r2*np.cos(th02) -r1 ) -th02 ;
        th13 = np.arctan2( z-r2*np.sin(th12) , x*np.cos(th1) + y*np.sin(th1) - r2*np.cos(th12) -r1 ) -th12 ;

        th1 *=180/np.pi
        th02*=180/np.pi
        th12*=180/np.pi
        th03*=180/np.pi
        th13*=180/np.pi

        th03+=90;
        th13+=90;    
    except:
        return 0,0,0,False  #Return Not Possible
    
    return th1,th02,th03,True


if __name__ == "__main__":


    print(getInverse(13.9,0,-19.1))
