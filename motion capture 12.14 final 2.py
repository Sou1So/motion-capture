
from asyncore import write
from importlib.resources import path
from textwrap import wrap
 
#from pysine import sine
import time
 
 
 
import math
import cv2
import numpy as np
import os.path
 
 
 
#def mouseClick(event, x, y, flags, params): #happens whene the left button is clicked
   # if event == cv2.EVENT_LBUTTONDOWN:
       # print("Mouse clikced at x=", x, "y= ", y)
        #hsv = frame_hsv[y, x] #pulls BGR data from frame
        #print("Hue =", hsv[0], "Saturation = ", hsv[1], "Value = ", hsv[2])

#####While loop that ask you the angle you are trying to reach and the angle that is to great
#    
FoundAngle_Check = False
FoundAngle = False
while FoundAngle_Check == False:
    readyStatus = input("are you ready? ")
    if readyStatus == "yes" or readyStatus == "Yes" or readyStatus == "y" or readyStatus == "Y":
        FoundAngle = True  
    else: #readyStatus == "No" or readyStatus == "no" or readyStatus == "N" or readyStatus == "n":
        FoundAngle = False
        #FoundAngle_Check = True
    if FoundAngle == True:
        FoundAngleInp = input("type the angle that you are trying to reach, and the press 'enter':")
        FoundAngleInt = int(FoundAngleInp)
        DangerAngle = input("type the angle that is to far to reach and SHOULD NOT BE REACHED, press 'enter' when complete:")
        DangerAngleInt = int(DangerAngle)
        #Danger_AngletOf = True
        #if Danger_AngletOf == True:
        #loadedAngle =np.load(FoundAngleInt)
        #Danger_loadedAngle =np.load(DangerAngleInt)
        GA = FoundAngleInt
        BA = DangerAngleInt
        FoundAngle_Check = True
    #else:
        #print("Please type in the desired angle to reach/")
        #print("Restart the program")
        #break
    """if FoundAngle == False:
        print("please prepare yourself and restart the program.")
        break"""
 

def distance(x1, y1, x2, y2):#function to caluclate distance between two points 
    """
    Calculate distance between two points
    """
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist
 
 
#function to find the first color and put a dot on the center 
def find_color1(frame):
        kernalOpen = np.ones((5,5), np.uint8)#keranl is for filtering the coler to make them look nicer
        kernalClose = np.ones((20,20), np.uint8)#keranl is for filtering the coler to make them look nicer      
    
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#converts color to HSV
        c1_lower = np.array([8, 110, 100]) #orange
        c1_upper = np.array([12, 250, 255])#orange
        c1_upper = np.array(c1_upper, dtype = "uint8")#sets HSV values in a array
        c1_lower = np.array(c1_lower, dtype = "uint8")#sets HSV values in a array
        c1_mask = cv2.inRange(frame_hsv, c1_lower, c1_upper)#mask the colers
        c1_maskOpen = cv2.morphologyEx(c1_mask,cv2.MORPH_OPEN, kernalOpen)
        c1_maskClosed = cv2.morphologyEx(c1_maskOpen, cv2.MORPH_CLOSE, kernalClose)#filters the colors
        c1_filter = cv2.bitwise_and(frame, frame, mask = c1_maskClosed)#the filter for the color
        cnts, hir = cv2.findContours(c1_maskClosed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#helps with detecting the color in the video
        if len(cnts) > 0:
            maxcontour = max(cnts, key=cv2.contourArea)
 
            #Find center of the contour(center of the circle)
            M = cv2.moments(maxcontour)
            if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                return (centroid_x, centroid_y), True
            else:
                return (700, 700), False #faraway point
        else:
            return (700, 700), False #faraway point
 
 
def find_color2(frame):#function to find the first color and put a dot on the center 
        kernalOpen = np.ones((5,5), np.uint8)#keranl is for filtering the coler to make them look nicer
        kernalClose = np.ones((20,20), np.uint8)#keranl is for filtering the coler to make them look nicer
    
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#converts color to HSV
        c2_lower =  np.array([45,55,30])#green
        c2_upper = np.array([120, 140, 135])#green
        c2_upper = np.array(c2_upper, dtype = "uint8")
        c2_lower = np.array(c2_lower, dtype = "uint8")
        c2_mask = cv2.inRange(frame_hsv, c2_lower, c2_upper)
        c2_maskOpen = cv2.morphologyEx(c2_mask,cv2.MORPH_OPEN, kernalOpen)
        c2_maskClosed = cv2.morphologyEx(c2_maskOpen, cv2.MORPH_CLOSE, kernalClose)
        c2_filter = cv2.bitwise_and(frame, frame, mask = c2_maskClosed)
        cnts, hir = cv2.findContours(c2_maskClosed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            maxcontour = max(cnts, key=cv2.contourArea)
 
            #Find center of the contour
            M = cv2.moments(maxcontour)
            if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                return (centroid_x, centroid_y), True #True
            else:
                return (700, 700), True #faraway point
        else:
            return (700, 700), True #faraway point
 
def find_color3(frame):
        kernalOpen = np.ones((5,5), np.uint8)
        kernalClose = np.ones((20,20), np.uint8)    
        """
        Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
        """
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        c3_lower =  np.array([90, 50, 50])#blue
        c3_upper = np.array([131, 120, 235])#blue
        c3_upper = np.array(c3_upper, dtype = "uint8")
        c3_lower = np.array(c3_lower, dtype = "uint8")
        c3_mask = cv2.inRange(frame_hsv, c3_lower, c3_upper)
        c3_maskOpen = cv2.morphologyEx(c3_mask,cv2.MORPH_OPEN, kernalOpen)
        c3_maskClosed = cv2.morphologyEx(c3_maskOpen, cv2.MORPH_CLOSE, kernalClose)
        c2_filter = cv2.bitwise_and(frame, frame, mask = c3_maskClosed)
        cnts, hir = cv2.findContours(c3_maskClosed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts) > 0:
            maxcontour = max(cnts, key=cv2.contourArea)
 
            #Find center of the contour
            M = cv2.moments(maxcontour)
            if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
                centroid_x = int(M['m10']/M['m00'])
                centroid_y = int(M['m01']/M['m00'])
                return (centroid_x, centroid_y), True #True
            else:
                return (700, 700), True #faraway point
        else:
            return (700, 700), True #faraway point
 
def Green_Out(GA, BA):
    if angle2_text <= GA:
        #cv2.circle(picture, (centroid1_x, centroid1_y), 50, (120, 0, 360), -1)
        #cv2.circle(picture, (centroid2_x, centroid2_y), 50, (120, 0, 360), -1)
        #cv2.circle(picture, (centroid3_x, centroid3_y), 50, (255, 0, 360), -1)
        sine(493,0.3)
        input("Stop there, Now lets go back down to your orignal position")
    elif angle2_text <= BA:
        #cv2.circle(picture, (centroid1_x, centroid1_y), 50, (23, 100, 82), -1)
        #cv2.circle(picture, (centroid2_x, centroid2_y), 50, (23, 100, 82), -1)
        #cv2.circle(picture, (centroid3_x, centroid3_y), 50, (23, 100, 82), -1)
        sine(560,0.3)
        input("GO BACK, you have went too far and need to decrease your angle")
    #else:
        #cv2.circle(picture, (centroid1_x, centroid1_y), 20, (255, 0, 0), -1)
        #cv2.circle(picture, (centroid2_x, centroid2_y), 20, (0, 128, 255), -1)
        #cv2.circle(picture, (centroid3_x, centroid3_y), 20, (255, 0, 255), -1)'''
 
 
 
cap = cv2.VideoCapture(1)
 
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('Therapy_Video', fourcc, 20.0, (640, 480))
 
 
keypressed = cv2.waitKey(100)
while keypressed != 27 and keypressed != ord("s"):
   
        #_, orig_frame = cap.read()
        ret, frame = cap.read()#could replace frame with "Orginal frame"
        #we'll be inplace modifying frames, so save a copy
        picture = frame.copy()
        (centroid1_x, centroid1_y), found_color1 = find_color1(picture)#relace the centroids with"color#_x/y
        (centroid2_x, centroid2_y), found_color2 = find_color2(picture)
        (centroid3_x, centroid3_y), found_color3 = find_color3(picture)
 
        #draw circles around these objects
        cv2.circle(picture, (centroid1_x, centroid1_y), 20, (255, 0, 0), -1)
        cv2.circle(picture, (centroid2_x, centroid2_y), 20, (0, 128, 255), -1)
        cv2.circle(picture, (centroid3_x, centroid3_y), 20, (255, 0, 255), -1)
        if found_color1 and found_color2 and found_color3:
            #trig stuff to get the line
            hypotenuse = distance(centroid1_x,centroid1_y, centroid2_x, centroid2_y)
            horizontal = distance(centroid1_x, centroid1_y, centroid2_x, centroid1_y)
            vertical = distance(centroid2_x, centroid2_y, centroid2_x, centroid1_y)
            angle = np.arcsin(vertical/hypotenuse)*180.0/math.pi
            round(angle)
 
            hypotenuse2= distance(centroid1_x,centroid1_y,centroid3_x, centroid3_y)
            horizontal2 = distance(centroid1_x,centroid1_y,centroid3_x,centroid1_y)
            vertical2 = distance(centroid3_x,centroid3_y,centroid3_x,centroid1_y)
            angle2 = np.arcsin(vertical2/horizontal2)*180.0/math.pi
            round(angle2)
 
            cv2.line(picture, (centroid1_x, centroid1_y), (centroid2_x, centroid2_y), (0, 0, 255), 2)
            cv2.line(picture, (centroid1_x, centroid1_y), (centroid2_x, centroid1_y), (0, 0, 255), 2)
            cv2.line(picture, (centroid2_x, centroid2_y), (centroid2_x, centroid1_y), (0, 0, 255), 2)
 
            cv2.line(picture, (centroid1_x, centroid1_y), (centroid3_x, centroid3_y), (255,127,0), 2)
            cv2.line(picture, (centroid1_x, centroid1_y), (centroid3_x, centroid1_y), (255,127,0), 2)
            cv2.line(picture, (centroid3_x, centroid3_y), (centroid3_x, centroid3_y), (255,127,0), 2)
       
            angle_text = ""
 
 
            if centroid2_y < centroid1_y and centroid2_x > centroid1_x:
                angle_text = str(angle)
            elif centroid2_y < centroid1_y and centroid2_x < centroid1_x:
                angle_text = str(180 - angle)
            elif centroid2_y > centroid1_y and centroid2_x < centroid1_x:
                angle_text = str(180 + angle)
            elif centroid2_y > centroid1_y and centroid2_x > centroid1_x:
                angle_text = str(360 - angle)
            cv2.putText(picture, angle_text, (centroid1_x-30, centroid1_y), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 128, 229), 2)
 
 
            angle2_text = ""
 
            if centroid3_y < centroid1_y and centroid3_x > centroid1_x:
                angle2_text = str(angle2)
            elif centroid3_y < centroid1_y and centroid3_x < centroid1_x:
                angle2_text = str(180 - angle2)
            elif centroid3_y > centroid1_y and centroid3_x < centroid1_x:
                angle2_text = str(180 + angle2)
            elif centroid3_y > centroid1_y and centroid3_x > centroid1_x:
                angle2_text = str(360 - angle2)
            cv2.putText(picture, angle2_text, (centroid3_x-30, centroid3_y), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 128, 229), 2)
 
 
            #Green_Out(BA, GA)
 
 
 
           
   
 
        #out.write(picture)
        img = cv2.flip(picture, 1)
        cv2.imshow('AngleCalc', img)
        cv2.waitKey(5)
keypressed = cv2.waitKey(30)
if keypressed == 27:
    cv2.destroyAllWindows() #press escape to close everything
elif keypressed == ord('s'): #press 's' to save
    cv2.destroyAllWindows()
 
#out.release()
cap.release()
 
 
 
 
 
 
