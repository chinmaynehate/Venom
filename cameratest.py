import cv2 as cv
import numpy as np 
import IP as m
cap = cv.VideoCapture(3)
n_slices=4
Images=[]
while True:
    ret,image= cap.read()
    gray_still= cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    bilateral_filter_gray=cv.bilateralFilter(gray_still,3,60,60)
    ret,thresh=cv.threshold(bilateral_filter_gray,150,255,cv.THRESH_BINARY)
    dilate_still=cv.dilate(thresh,np.ones((5,5),np.uint8),9)
    closed = m.segment_img(dilate_still,Images,n_slices)  
    
    restored_img = m.restore_img(closed)
    cv.imshow("masked",restored_img)


    if cv.waitKey(1)  & 0xFF == ord('q'):
        break

cap.release()

cv.destroyAllWindows()

