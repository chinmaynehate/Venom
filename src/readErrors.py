import ImageProcessing as ip
import cv2
from helpers import calculateYs

if __name__=="__main__":
    while True:
        angle,transLation,x1,x2,y1,y2  = ip.getSlopeError()
        print("Angle:",angle,"Lateral Error:",transLation)

        ymax,ymin = calculateYs(angle,transLation)
        print("Ymax : ",ymax," , ymin: ",ymin)
        # print("x1:",x1," , x2:",x2," , y1:",y1," , y2:",y2)
