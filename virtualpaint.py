# Virtual paint app

import cv2 as cv
import numpy as np
from collections import deque

lower_red = np.array([100, 60, 60])
upper_red = np.array([140, 255, 255])


# Initialize deques to store different colors in different arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

# Initialize an index variable for each of the colors 
bindex = 0
gindex = 0
rindex = 0
yindex = 0

# Just a handy array and an index variable to get the color-of-interest on the go
# Blue, Green, Red, Yellow respectively
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] 
colorIndex = 0

# Create a blank white image
paintWindow = np.zeros((471,636,3)) + 255

# Draw buttons like colored rectangles on the white image
paintWindow = cv.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

# Label the rectanglular boxes drawn on the image
cv.putText(paintWindow, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)

# Create a window to display the above image (later)
cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)


capture = cv.VideoCapture(0) # 0 is for webcam
while True:
    _ , frame = capture.read() # Reading video frame by frame
    flipped = cv.flip(frame, 1) # Flipping the frame horizontally
    #cv.imshow('Webcam', flipped)
    blur = cv.medianBlur(flipped, 5)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV) # HSV is useful when we need to detect something based on its color
    #cv.imshow('HSV', hsv)
    
    kernel = np.ones((1, 1), np.uint8)
    mask = cv.inRange(hsv, lower_red, upper_red)
    
    # Morphological Image Processing (For removing noise)
    mask = cv.erode(mask, kernel, iterations=2)
    #cv.imshow('Erosion', mask)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    #cv.imshow('Morphologyex', mask)
    mask = cv.dilate(mask, kernel, iterations=1)
    #cv.imshow('Dilate', mask)
    
    # Contours detection in mask
    contours, heirarchies = cv.findContours(mask.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    center = 0
    
    # Creating a circle when it detects red color
    if len(contours) > 0:
           contours = sorted(contours, key = cv.contourArea, reverse = True)[0]
           (x,y), radius = cv.minEnclosingCircle(contours)
           cv.circle(flipped, (int(x),int(y)), int(radius), (0,255,255), 2)
           M = cv.moments(contours)
           if M['m00'] != 0:
               center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
           
           if center[1]<65:
               if 40 <= center[0] <= 140: # Clear All
                   bpoints = [deque(maxlen=512)]
                   gpoints = [deque(maxlen=512)]
                   rpoints = [deque(maxlen=512)]
                   ypoints = [deque(maxlen=512)]
                   bindex = 0
                   gindex = 0
                   rindex = 0
                   yindex = 0
                   paintWindow[67:,:,:] = 255
               elif 160 <= center[0] <= 255:
                   colorIndex = 0
               elif 275 <= center[0] <= 370:
                   colorIndex = 1
               elif 390 <= center[0] <= 485:
                   colorIndex = 2
               elif 505 <= center[0] <= 600:
                   colorIndex = 3
           else:
               if colorIndex == 0:
                   bpoints[0].appendleft(center)
               if colorIndex == 1:
                   gpoints[0].appendleft(center)
               if colorIndex == 2:
                   rpoints[0].appendleft(center)
               if colorIndex == 3:
                   ypoints[0].appendleft(center)
           
           points = [bpoints, gpoints, rpoints, ypoints]
           for i in range(len(points)):
               for j in range(len(points[i])):
                   for k in range(1, len(points[i][j])):
                       if points[i][j][k-1] is None or points[i][j][k] is None:
                           continue
                       cv.line(flipped, points[i][j][k-1], points[i][j][k], colors[i], 2)
                       cv.line(paintWindow, points[i][j][k-1], points[i][j][k], colors[i], 2)
                       
    flipped = cv.rectangle(flipped, (40,1), (140,65), (0,0,0), 2)
    flipped = cv.rectangle(flipped, (160,1), (255,65), colors[0], -1)
    flipped = cv.rectangle(flipped, (275,1), (370,65), colors[1], -1)
    flipped = cv.rectangle(flipped, (390,1), (485,65), colors[2], -1)
    flipped = cv.rectangle(flipped, (505,1), (600,65), colors[3], -1)
    cv.putText(flipped, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
    cv.putText(flipped, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(flipped, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(flipped, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(flipped, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)                 
    
    cv.imshow('With Circle', flipped)
    cv.imshow('Paint', paintWindow)
    
    if cv.waitKey(20) & 0xFF==ord('q'):
        break # Breaking out of infinite video playing loop
    
capture.release()
cv.destroyAllWindows()