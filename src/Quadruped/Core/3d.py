import sys
sys.path.insert(0, "..")	
import numpy as np	
# import constants as k	


def Transform3D(x,y,z,Pitch,Roll):
    home = np.matrix([x,0,0,0],[0,y,0,0],[0,0,z,0],[0,0,0,1])

    xAngle = Yaw
    rotX = np.matrix([1 ,0              ,0              ,0],
                    [0  ,np.cos(xAngle) ,-np.sin(xAngle),0],
                    [0  ,np.sin(xAngle) ,np.cos(xAngle),0],
                    [0 ,0              ,0              ,1])
    yAngle=Roll
    rotY = np.matrix([np.cos(yAngle) ,np.sin(yAngle),0  ],
                    [0 ,1              ,0              ,0],
                    [-np.sin(yAngle),0 ,np.cos(yAngle),0 ],
                    [0 ,0              ,0              ,1])

    zAngle=0
    rotZ = np.matrix([np.cos(zAngle) ,-np.sin(zAngle),0,0],
                    [np.sin(zAngle) ,np.cos(zAngle)  ,0,0],
                    [0 ,0              ,1              ,0],
                    [0 ,0              ,0              ,1])


    tfx = home.dot(rotX)
    tfxy = tfx.dot(rotY)
    tfxyz = tfxy.dot(rotZ)

    x = tfxyz[0][0]
    y = tfxyz[1][1]
    z = tfxyz[2][2]

    return x,y,z





if __name__ == "__main__":
    pass   

