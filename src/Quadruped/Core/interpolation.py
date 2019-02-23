import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import time 


# x,y,z,yaw,pitch,roll
Intitial_config = np.array([8,7,-16])
Final_config = np.array([8,-4,-16])



# Velocities dx,ty,dz,....
Initial_veclocity = np.array([0,0,0])
Final_veclotiy = np.array([0,3,0])


# Time of Path 
Iniital_time = 0.0
Final_time = 1

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
    pass
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # input = range(0,11,0.1)
    # pos = []
    # vel = []
    # acc = []

    # sctx = []
    # scty = []

    # start = time.time()
    # current = time.time()
    # while (time.time()-start <=(Final_time-Iniital_time)):
    #     config = getConfigAt(time.time()-start)
    #     # ax.scatter(config[0],config[1],config[2])
    #     time.sleep(1)
    #     print("Calculating at time:",time.time()-start)
    
    # print(res)
    # plt.plot(input,pos)
    # plt.plot(input,vel)
    # plt.plot(input,acc)
    # plt.plot(sctx,scty)
    # plt.xlabel("X")
    # plt.xlabel("Y")

    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")
    # # plt.ylabel("Time")
    # plt.show()



