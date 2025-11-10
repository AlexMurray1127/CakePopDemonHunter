# This file will be minimal opencv file for mirroring the webcam

import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

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
    # Calculate change in gray
    delta = cv.absdiff(gray, prev_gray).sum()

    # Display Text
    cv.putText(frame, str(delta), (50,300),
                cv.FONT_HERSHEY_SIMPLEX,
                2,              # font_scale
                (255,255,255),    # color
                4)              # thickness

    cv.putText(frame, "Hello", (50,100),
                cv.FONT_HERSHEY_SIMPLEX,
                2,              # font_scale
                (150,0,150),    # color
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

