"""
    This program is the Version 2 of the Line following, Here we use Video of arena instead of images of arena

    Points to be noted :
    - First the arena must be placed in front of the camera module before the program executes
    - This program is made with the assumption that the arena is for Robocon 2017
"""

import numpy as np
import cv2

n_slices=4
Images = [] 

def segment_img(feed_image0,img_array,slices):
	global error_array
	global part_height  
	global centers_list  									#Declared global for use in ifilter
	height,width = feed_image0.shape[:2]
	part_height = int(height/slices)
	masked = []
	morph = []
	
	for i in range (slices):
		filename= "images/file_%d.jpg"%i
		part= part_height*i
		crop_image= feed_image0[part:part+part_height,0:width]
		img_array.append(crop_image)
	
		error_array = ContoursAndBoundaries(img_array[i],empty_array)				#COMMENTED
		# cv.imshow('morph_%d'%i, morph[i])                     #Show each slice

	ifilter(lambda x: x%2, range(8))
	# print(centers_list)

	# return(morph)
	return(img_array)

def createLineIterator(P1, P2, img):
    """
        Produces an array that consists of the coordinates and intensities of each pixel in a line between 2 points

        Parameters :
            -P1 : array with first point(x, y)
            -P2 : array with second point(x, y)
            -img: image
    """

#define Local Variables
    imageH = img.shape[0]  #Stores the width of the image (frame)
    imageW = img.shape[1]  #Stores the height of the image (frame)
    P1X = P1[0]
    P2X = P2[0]
    P1Y = P1[1]
    P2Y = P2[1]

#difference between local and absolute difference between points

    dX = P2X - P1X
    dY = P2Y - P1Y

    dXa = abs(dX)
    dYa = abs(dY)

#Predefine numpy array for output based on the distance between points

    itBuffer = np.empty(shape = (np.maximum(dYa, dXa), 3), dtype=np.float32)
    itBuffer.fill(np.nan)

#Obtain coordinates along the line using a form of Bresenham's algo
# To test DDA algo, midpoint algo, Gupta sproull algo, xiaolin wu algo

    negY = P1Y > P2Y
    negX = P1X > P2Y

    if P1Y == P2Y: #Horizontal line segment
        itBuffer[:,1] = P1Y
        if negX:
            itBuffer[:,0] = np.arange(P1X-1, P1X-dXa-1, -1)
        else:
            itBuffer[:,0] = np.arange(P1X+1, P1X+dXa+1)

#Remove points outside image

    colX = itBuffer[:,0]
    colY = itBuffer[:,1]

    itBuffer = itBuffer[ (colX >= 0) & (colY >= 0 ) & (colX < imageW) & (colY < imageH) ]

#Get intensities from img ndarray
    itBuffer[:, 2] = img[itBuffer[:,1].astype(np.uint), itBuffer[:,0].astype(np.uint)]
    return itBuffer            

"""
	Main function begins now 
"""

#If not used each and every value of output won't be shown
np.set_printoptions(threshold='nan')

import constants as k
cap = cv2.VideoCapture(k.CAMERA_ID)
cap.set(3, 288)
cap.set(4, 352)
afterJunctionFlag = 1

while True:
    #Capture frame by frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (800, 600))

    #Our Operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Blurring the image
    gray = cv2.GaussianBlur(gray, (5,5) ,0)

    #Converts the image to binary image. thresh1 is the binary image
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # ret, thresh1 = cv2.threshold(gray, 143, 255, cv2.THRESH_BINARY)
    cv2.imshow('thresh', thresh1)
    thresh1 = cv2.bitwise_not(thresh1)


    #p1 and p2 are the points on the line segment whose distance must be 
    p1 = [0,300]
    p2 = [800, 300]

    p3 = [0,500]
    p4 = [800,500]

    #The return value from the function is the array consisting of [x, y, intensity]
    intensityBuf = np.array(createLineIterator(p1, p2, thresh1))
    intensityBuf1 = np.array(createLineIterator(p3, p4, thresh1))

    #Only intensities are extracted from the intensityBuf array
    onlyIntensity = intensityBuf[:,2].tolist()
    onlyIntensity1 = intensityBuf1[:,2].tolist()

    #Gets the index of the first pixel consisting of white pixel
    try:
      firstWhiteIndex = onlyIntensity.index(255)
    except:
      firstWhiteIndex = 20	

    try:
      firstWhiteIndex1 = onlyIntensity1.index(255)
    except:
      firstWhiteIndex1 = 20

    
    #Searches the first black pixel after finding first white pixel
    for coord in range(firstWhiteIndex, len(onlyIntensity), 1):
        if onlyIntensity[coord] == 0:
                firstBlackIndex = coord-1
                break 
        else:
	        firstBlackIndex = 780
    
    for coord in range(firstWhiteIndex1, len(onlyIntensity1), 1):
        if onlyIntensity1[coord] == 0:
                firstBlackIndex1 = coord-1
                break 
        else:
	        firstBlackIndex1 = 780

    # for coord in range(firstWhiteIndex1, len(onlyIntensity1), 1):
	#     if onlyIntensity1[coord] == 0:
    #     	    firstBlackIndex1 = coord-1
    #             break
        
    #     else:
	#         firstBlackIndex1 = 780

    #Finds the coordinates of the first white Pixel 
    p1Cir = intensityBuf[firstWhiteIndex].tolist()
    #Finds the coordinates of the first black Pixel 
    p2Cir = intensityBuf[firstBlackIndex].tolist()
   
    #Finds the coordinates of the first white Pixel 
    p3Cir = intensityBuf1[firstWhiteIndex1].tolist()
    #Finds the coordinates of the first black Pixel 
    p4Cir = intensityBuf1[firstBlackIndex1].tolist()

    #For Detecting the Junction
    if p1Cir[0] < 40 and p2Cir[0] > 600 and afterJunctionFlag == 1:
        print ("Junction Detected") 
        afterJunctionFlag = 0
        
	 
    
    if p1Cir[0] > 40 and p2Cir[0] < 600 and afterJunctionFlag == 0:
	    print ("Junction Crossed")
	    afterJunctionFlag = 1	
	
    d1 = 403 - p1Cir[0] 
    d2 = p2Cir[0] - 403 

    # if d1 > d2 or d2 < 0 :
    #     print ("Bot should move towards left now")
    # if d2 > d1 or d1 < 0 :
    #     print ("Bot should move towards right now")

    #Draw the first circle at the first white pixel
    gray = cv2.circle(gray, (int(p1Cir[0]), int(p1Cir[1])), 5, (0, 0, 255), -1)
    #Draw the second circle at the first black pixel after the array of white pixel
    gray = cv2.circle(gray, (int(p2Cir[0]), int(p2Cir[1])), 5, (255, 0, 255), -1)

    #Draw the first circle at the first white pixel
    gray = cv2.circle(gray, (int(p3Cir[0]), int(p3Cir[1])), 5, (0,0, 255), -1)
    #Draw the second circle at the first black pixel after the array of white pixel
    gray = cv2.circle(gray, (int(p4Cir[0]), int(p4Cir[1])), 5, (255, 0, 255), -1)

    import math
    dy = p4Cir[1]-p2Cir[1]
    dx = p4Cir[0]-p2Cir[0]
    print("Error Angle:" ,180/math.pi*math.atan2(dy,dx))

    #Drawing a line to divide the frame to two halfs 
    gray = cv2.line(gray, (400, 0), (400, 600), (0, 0, 0), 3)

    #Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#When everything is done 
cap.release()
cv2.destroyAllWindows()
