import numpy as np
import time 


# x,y,z,yaw,pitch,roll
Intitial_config = np.array([8,7,-16])
Final_config = np.array([8,-4,-16])


Intitial_config = np.array([-np.pi,0,0])
Final_config = np.array([np.pi,0,0])

# Velocities dx,ty,dz,....
Initial_veclocity = np.array([0,0,0])
Final_veclotiy = np.array([0,0,0])

# Time of Path 
Iniital_time = 0.0
Final_time = 1


def setInterpolate1d(position,velocities,time):
    global Intitial_config,Final_config,Initial_veclocity,Final_veclotiy,Iniital_time,Final_time,A,B,C,D

    Intitial_config = np.array([position[0],0,0])
    Final_config = np.array([position[1],0,0])

        # Velocities dx,ty,dz,....
    Initial_veclocity = np.array([velocities[0],0,0])
    Final_veclotiy = np.array([velocities[1],0,0])


    # Time of Path 
    Iniital_time = time[0]
    Final_time = time[1]

    A,B,C,D = getABCD()

def getInterpolate1d(time):
    return (getConfigAt(time))[0]
    # return 0
    pass





def getABCD():
    D = Intitial_config

    C = Initial_veclocity

    B = 3.0*(Final_config - Intitial_config - Initial_veclocity*Final_time)/(Final_time**2.0) - ( Final_veclotiy-Initial_veclocity )/(Final_time)

    A = (Final_veclotiy-Initial_veclocity)/(3.0*(Final_time**2.0)) - 2.0*(B)/(3.0*Final_time)

    return A,B,C,D

A,B,C,D = getABCD()


def getConfigAt(t):
    t=t*1.0
    res = A * (t**3) + B * (t**2) + C *(t) + D  
    return res[0:3]

def getVelocity(t):
    res = 3 * A * t**2 + 2 * B*t + C
    return res

def getAcc(t):
    res = 6 * A*t + 2*B
    return res

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

    
    # pos = []

    times = [0,2]
    position = [0,10]
    velocities = [0,0]

    setInterpolate1d(position,velocities,times)

    Xs = []
    Ys=[]

    def pathFun(theta):
        stepLength = 10.0
        Amplitude = 5.0
        return ( np.sin(np.pi * theta / stepLength) * Amplitude)

    start = time.time()
    current = time.time()
    while (time.time()-start <= ( Final_time-Iniital_time)):
        config = getInterpolate1d( time.time()-start)
        Xs.append(config)
        Ys.append(pathFun(config))

        # ax.scatter(1,1,1)
        time.sleep(0.1)
        print("Calculating at time:",time.time()-start)
    
    fig = plt.figure()
    
    plt.scatter(Xs,Ys)
    # ax = fig.add_subplot(111, projection='3d')
    # # plt.ylabel("Time")
    plt.show()



