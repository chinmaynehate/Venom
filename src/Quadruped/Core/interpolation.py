import numpy as np
import time 
import kinematics as ik
import constants as k
from numpy.linalg import inv

# x,y,z,yaw,pitch,roll
Intitial_config = np.array([8,7,-16])
Final_config = np.array([8,-4,-16])

Intitial_config = np.array([0,0,0,0,0,0])
Final_config = np.array([10,0,0,0,0,0])

# Intitial_config = np.array([-np.pi,0,0,0,0,0])
# Final_config = np.array([np.pi,0,0,0,0,0])

# Velocities dx,ty,dz,....
Initial_veclocity = np.array([0,0,0,0,0,0])
Final_veclotiy = np.array([0,0,0,0,0,0])

# Time of Path 
Iniital_time = 0.0
Final_time = 1


def setInterpolate1d(position,velocities,time):
    global Intitial_config,Final_config,Initial_veclocity,Final_veclotiy,Iniital_time,Final_time,A,B,C,D

    Intitial_config = np.array([position[0],0,0])
    Final_config = np.array([position[1],0,0])

        # Velocities dx,dy,dz,....
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
    return res*0.001

def getAcc(t):
    res = 6 * A*t + 2*B
    return res

def CalculateJInv(x,y,z):

    t1,t2,t3,isPossible = ik.getInverse(x,y,z)
    a1 = k.linkLength[1]
    a2 = k.linkLength[2]
    a3 = k.linkLength[3]
    s1 = np.sin(t1)
    c1 = np.cos(t1)
    s2 = np.sin(t2)
    c2 = np.cos(t2)
    s23 = np.sin(t2+t3)
    c23 = np.cos(t2+t3)

    J = np.matrix([ [ (-s1*(a3*c23 + a2*c2 + a1)) , (-c1*(a3*s23 + a2*s2)) , (-a3*c1*s23)],
                    [ (c1*(a3*c23 + a2*c2 + a1)) ,  (-s1*(a3*s23 + a2*s2)) , (-a3*s1*s23)],
                    [ 0 ,                           (a3*c23 + a2*c2) ,       (a3*c23)],
                    [ (-s1*c23) ,                   (-c1*s23) ,              (-c1*s23)],
                    [ (c1*c23) ,                    (-s1*s23) ,              (-s1*s23)],
                    [ 0,                            c23 ,                    c23]])

    # print("\nJ = \n", J)

    JT = np.transpose(J)
    # print("\nJT = \n", JT)
    JTJ = JT*J
    # print("\nJT*J = \n", JTJ)
    JI = inv(JTJ) * JT
    # print("\nJI = \n", JI)
    return JI

def CalculateJSV(x,y,z,t):
    JI = CalculateJInv(x,y,z)
    # print("\nJT = \n", JI)
    ToolVelocity = np.transpose(np.matrix(getVelocity(t)))
    # print("\nToolVelocity = \n", ToolVelocity)
    JointSpaceVelocities = JI * ToolVelocity
    print("\nJointSpaceVelocities = \n",JointSpaceVelocities)
    # return JointSpaceVelocities


if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

    
    # pos = []

    times = [0,2]
    position = [0,10]
    velocities = [0,0]

    # setInterpolate1d(position,velocities,times)

    Xs = []
    Ys=[]

    def pathFun(theta):
        stepLength = 10.0
        Amplitude = 5.0
        return ( np.sin(np.pi * theta / stepLength) * Amplitude)

    start = time.time()
    current = time.time()
    
    while (time.time()-start <= ( Final_time-Iniital_time)):
        # config = getInterpolate1d( time.time()-start)
        # Xs.append(config)
        # Ys.append(patFun(config))
        # ax.scatter(1,1,1)
        config= getConfigAt(time.time()-start)
        x,y,z=config
        time.sleep(0.1)
        print("Calculating at time:",time.time()-start)
        print("\nconfig = \n", config)
        CalculateJSV(x,y,z,time.time()-start)
    
    # fig = plt.figure()
    
    # plt.scatter(Xs,Ys)
    # ax = fig.add_subplot(111, projection='3d')
    # # plt.ylabel("Time")
    # plt.show()



