# This file will be minimal opencv file for mirroring the webcam

import numpy as np
import cv2 as cv
import time
import random
 
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")

# Score
score = 0
game_over = False

first = True
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    frame = cv.flip(frame, 1)

    # Operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    if first:
        prev_gray = gray
        first = False
        
    # Face Detection Box
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    face_rect = None
    for (x, y, w, h) in faces:
        face_rect = (x, y, w, h)
        cv.rectangle(frame,(x, y), (x + w, y + h), (0, 255, 0), 2)
        break
    
    
    # Calculate change in gray
    delta = cv.absdiff(gray[0:100], 
                       prev_gray[0:100]).sum()
    cv.rectangle(frame, (0,0), (100,100), (100,100,100), 2)


    # Display Text
    cv.putText(frame, str(delta), (50,300),
                cv.FONT_HERSHEY_SIMPLEX,
                2,              # font_scale
                (255,255,255),    # color
                4)              # thickness


    # Display the resulting frame
    cv.imshow('frame', frame)

    # Save prev frame 
    prev_gray = gray 


    # See if user wants to quit
    if cv.waitKey(1) == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows() 

