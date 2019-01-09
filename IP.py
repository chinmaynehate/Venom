import cv2 as cv 
import numpy as np
from itertools import *
from math import *
import serial
import time
from time import sleep
vid = cv.VideoCapture(1)

from_centre=False
n_slices=4
error_array = []
empty_array = []

prev_slope = 0
slope = 0
prev_c = 0

 

def ifilter(predicate, iterable):
    #Example function call: ifilter(lambda x: x%2, range(10)) --> 1 3 5 7 9
    if predicate is None:
        predicate = bool
    for i in iterable:
        if predicate(i):
        	centers_list[i] += part_height*(i-1/2) 
            

def segment_img(feed_image0,img_array,slices,roi_array):
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
		roi = feed_image0[part:part+50,0:50]
		roi_array.append(roi)
	
		error_array = ContoursAndBoundaries(img_array[i],empty_array)				#COMMENTED
		# cv.imshow('morph_%d'%i, morph[i])                     #Show each slice

	ifilter(lambda x: x%2, range(8))
	# print(centers_list)

	# return(morph)
	return(img_array)

def restore_img(img_array):
	top= img_array[0]
	for i in range(len(img_array)):   										# 0 is a separate case because number of concatenations are 3 and length of array(i.e number of slices is 4)
		if (i==0):
			concatenated_img=np.concatenate((top,img_array[1]),axis=0)  #axis 0 for vertical, 1 for horizontal stacking (img1 is up and left)
		if (i>1):
			concatenated_img=np.concatenate((concatenated_img,img_array[i]),axis=0)


	return concatenated_img


def getContourCenter(contour):
    M = cv.moments(contour)

    if M["m00"] == 0:
        return 0,0

    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    return x, y

def ContoursAndBoundaries(feed_image, empty_array):
    global centers_list
    global prev_c
    _,contours,hierarchy=cv.findContours(feed_image.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)   # no 'img' as first argument necessary for findContours argument. Otherwise it will trigger ValueError: Too many/less values to unpack.                                                                                                # contours,hierarchy=cv.findContours(thresh.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        c = max(contours,key=cv.contourArea)
        height,width = feed_image.shape[:2]
        middleX= int(width/2)      #X and Y coordinates of the middle point         
        middleY= int(height/2)
        cx = getContourCenter(c)[0]
        cy = getContourCenter(c)[1]
        cv.line(feed_image,(cx,0),(cx,720),(255,0,0),1)
        cv.line(feed_image,(0,cy),(1280,cy),(255,0,0),1)
        cv.circle(feed_image,(cx,cy),7,(238,130,238),-1)       #moving centre
        cv.circle(feed_image,(middleX,middleY),7,(0,255,0),-1)    #stationary centre
        cv.drawContours(feed_image, contours, -1, (0,255,0), 1)
        if (abs(middleX-cx)>7):
           error = (middleX-cx)
        else:
           error = 0 

        font = cv.FONT_HERSHEY_COMPLEX
        cv.putText(feed_image, str(middleX - cx),(cx+50 ,middleY),
                        font, 1, (200, 0, 200), 2)
        cv.drawContours(feed_image, contours, -1, (0,255,0), 1)
        empty_array.append(error)
        centers_list.extend([cx,cy])
        prev_c = c
    else:	
        height,width = feed_image.shape[:2]
        middleX= int(width/2)      #X and Y coordinates of the middle point         
        middleY= int(height/2)
        cx = getContourCenter(prev_c)[0]
        cy = getContourCenter(prev_c)[1]
        cv.line(feed_image,(cx,0),(cx,720),(255,0,0),1)
        cv.line(feed_image,(0,cy),(1280,cy),(255,0,0),1)
        cv.circle(feed_image,(cx,cy),7,(238,130,238),-1)       #moving centre
        cv.circle(feed_image,(middleX,middleY),7,(0,255,0),-1)    #stationary centre
        cv.drawContours(feed_image, contours, -1, (0,255,0), 1)
        if (abs(middleX-cx)>7):
           error = (middleX-cx)
        else:
           error = 0 

        font = cv.FONT_HERSHEY_COMPLEX
        cv.putText(feed_image, str(middleX - cx),(cx+50 ,middleY),
                        font, 1, (200, 0, 200), 2)
        cv.drawContours(feed_image, contours, -1, (0,255,0), 1)
        empty_array.append(error)
        centers_list.extend([cx,cy])

    	
    # print (centers_list)
    return empty_array

        
def map(x,in_min,in_max,out_min,out_max):

	return (x-in_min)*(out_max-out_min)/(in_max-in_min) + out_min


def constrain(x, lower,upper):
	if x<lower:
		x=lower
	if x>upper:
		x=upper 
	if x<upper and x>lower:
		x = x
	return x
 
def errorAverage(restored_img,error_array,bottomX,bottomY):
	font= cv.FONT_HERSHEY_SIMPLEX
	mapped_error=[]
	error_sum = 0  
	for i in range(len(error_array)):
		mapped_error.append(constrain(map(error_array[i],-200,200,0,100),0,100))
		error_sum += mapped_error[i]
	error_average = error_sum/n_slices
	cv.putText(restored_img,str(error_average),(bottomX-150,bottomY-50),font,1,(200,0,200),2)
	return error_average

def calculateSlope(centers_list):
	global slope
	global prev_slope

	x1= centers_list[0]
	y1 = centers_list[1]
	x2 = centers_list[6]
	y2= centers_list[7]
	print (x1,x2,y1,y2)
	if (x2-x1 !=0):
			diff_y = y2-y1
			diff_x = x2-x1
			slope = diff_y/diff_x
			print(slope)
	# angle = 45
	elif prev_slope<0 :
		slope = -5729.57789312
	elif prev_slope>0 :
		slope = 5729.57789312
	checkangle = 1
	if (checkangle==1):
		if slope >= 5729.57789312:    
			angle = 89.99
		elif slope <= -5729.57789312:
			angle = -89.99
		else :
			angle = degrees(atan(slope))    
		checkangle=0
	prev_slope = slope     			# If line is on right side , x2-x1 is negative. Opposite for other direction.
	return angle

def returnVal(global_angle,error_average):
	return global_angle,error_average



while True:
	ret,image= vid.read()
	# image= cv.imread("Line2.png")
	Images=[]
	ROI_Array = []
	error_array = []
	empty_array = []
	centers_list = []
	font= cv.FONT_HERSHEY_SIMPLEX
	# ok,frame= vid.read()
	hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

	# hsv= cv.cvtColor(frame,cv.COLOR_BGR2HSV)
	# gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	gray_still= cv.cvtColor(image,cv.COLOR_BGR2GRAY)	 #COMMENTED
	# g_blur=cv.GaussianBlur(hsv,(5,5),0)
	# bilateral_filter= cv.bilateralFilter(hsv,3,60,60)
	bilateral_filter_gray=cv.bilateralFilter(gray_still,3,60,60)

	#bilateral=cv.bilateralFilter(hsv_image,3,60,60)			#COMMENTED

	ret,thresh=cv.threshold(bilateral_filter_gray,150,255,cv.THRESH_BINARY)

	#ret,thresh=cv.threshold(bilateral_filter_gray_still,60,255,cv.THRESH_BINARY_INV)	  #COMMENTED

	dilate_still=cv.dilate(thresh,np.ones((5,5),np.uint8),9)	 #COMMENTED




	# dilate = cv.dilate(thresh,np.ones((5,5),np.uint8),9)
	# erode = cv.erode(bilateral_filter,np.ones((1,1),np.uint8),1)
	# mask_blur=cv.inRange(g_blur,lower_range,upper_range)
	# #mask_dilate= cv.inRange(dilate,lower_range,upper_range)
	# mask_erode = cv.inRange(erode,lower_range,upper_range)

	# mask_bilateral=cv.inRange(bilateral_filter,lower_range,upper_range)
	# cv.imshow('frame',frame)
	# cv.imshow('mask_blur',mask_blur)
	# cv.imshow('bilateral_filter',mask_bilateral)
	# cv.imshow('dilate',dilate)
	# cv.imshow('mask_erode',mask_erode)
	# cv.imshow('thresh',thresh)
	cv.imshow('original',image)

	# closed= segment_img(hsv_image,Images,n_slices, ROI_Array)              # Slice function called, with arguments either feeded through an image or through continuous loop,
	closed= segment_img(dilate_still,Images,n_slices, ROI_Array)  
	restored_img= restore_img(closed)
	full_height,full_width = restored_img.shape[:2]
	error_average =errorAverage(restored_img,error_array,full_width,full_height)
	global_angle = calculateSlope(centers_list)	
	cv.putText(restored_img,str(global_angle),(0,full_height-50),font,1,(200,0,200),2)
	error_average =int(error_average)

	returnVal(global_angle,error_average)

	cv.imshow('restored', restored_img)

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

# print([lower_range[0], lower_range[1], lower_range[2]])
# print([upper_range[0], upper_range[1], upper_range[2]])