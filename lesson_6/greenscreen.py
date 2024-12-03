import cv2
import numpy as np
import time

video = cv2.VideoCapture("video.mp4")

time.sleep(1)
count = 0 
background = 0

for i in range(60):
    status, background = video.read() #read fonction used to read each frame in video 
    #status video.read fonction gives status of the frame 
    #background is a varaible in which we are storing the frame we recive
    if status == False:
        continue

#flipping the background image left right fliping
background = np.flip(background, axis = 1)
 
while video.isOpened():
    status, frame = video.read()
    if status == False:
        break
    frame = np.flip(frame, axis = 1)
    count += 1
    #converting frame to HSV color format
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #color range for masking (HSV) hue, saturation, value
    low_red1 = np.array([100,40,40])
    low_red2 = np.array([100,255,255])
    mask1 = cv2.inRange(hsv, low_red1, low_red2)
    upper_red1 = np.array([155,40,40])
    upper_red2 = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, upper_red1, upper_red2)
    mask1 = mask1 + mask2

    #refining the mask 
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)
    mask1 = cv2.dilate(mask1, np.ones((3,3), np.uint8), iterations = 1)
    mask2 = cv2.bitwise_not(mask1) #eveything which is not mask (the red area) #non red zone

    result1 = cv2.bitwise_and(background, background, mask = mask1)
    result2 = cv2.bitwise_and(frame,frame, mask = mask2)
    result = cv2.addWeighted(result1, 1, result2, 1, 0)
    cv2.imshow("Red screen", result)
    if cv2.waitKey(10) == 27:
        break


cv2.destroyAllWindows()