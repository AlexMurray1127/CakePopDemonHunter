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

motion_threshold = 1600000  # motion detection for corner demons

# Define falling and corner demons
last_demon_time = 0
demon_interval = 3  # seconds between corner demons
corner_demon = None

falling_demon = None
fall_speed = 7

fall_delay = random.uniform(1.0,6.0)
fall_start_time = time.time()

# Helper functions
def spawn_corner_demon(w, h):
    """Spawn demon at one of the four screen corners."""
    return random.choice([
        (20, 20),
        (w - 60, 20),
        (20, h - 60),
        (w - 60, h - 60)
    ])

def spawn_falling_demon(w):
    return [w // 2, 0]
    
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
    
    h, w = gray.shape

    if first:
        prev_gray = gray
        first = False
        
    # Face Detection Box
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_rect = None
    
    for (x, y, fw, fh) in faces:
        face_rect = (x, y, fw, fh)
        cv.rectangle(frame,(x, y), (x + fw, y + fh), (0, 255, 0), 2)
        break
    
    
    # Calculate change in gray
    delta = cv.absdiff(gray[0:100], 
                       prev_gray[0:100]).sum()
    #cv.rectangle(frame, (0,0), (100,100), (100,100,100), 2)

    motion = cv.absdiff(gray, prev_gray).sum()
    prev_gray = gray

    # Corner Demon System
    now = time.time()

    # Spawn a new corner demon every 3 seconds
    if corner_demon is None and now - last_demon_time > demon_interval:
        corner_demon = spawn_corner_demon(w, h)
        last_demon_time = now

    # Draw corner demon & check for motion hit
    if corner_demon is not None:
        cx, cy = corner_demon
        cv.rectangle(frame, (cx, cy), (cx + 40, cy + 40), (0, 0, 255), -1)

        if motion > motion_threshold:
            score += 1
            corner_demon = None

    # Falling Demon with randomized timer

    try:
        fall_delay
    except NameError:
        fall_delay = random.uniform(1.0,6.0)
        fall_start_time = time.time()
        
    if falling_demon is None:
        if time.time() - fall_start_time > fall_delay:
            falling_demon = spawn_falling_demon(w)
            fall_delay = random.uniform(1.0,6.0)
    else:
        fx, fy = falling_demon
        cv.rectangle(frame, (fx, fy), (fx + 40, fy + 40), (255, 0 , 0), -1)
        falling_demon[1] += fall_speed
            
        # Falling Demon collision
        if face_rect is not None:
            x, y, fw, fh = face_rect
            if (fx < x + fw and fx + 40 > x and
                fy < y + fh and fy + 40 > y):
                game_over = True
                
        # Off Screen timer reset
        if falling_demon[1] > h:
            score += 5
            falling_demon = None
            fall_start_time = time.time()
            
    # Display frame detection Text
    cv.putText(frame, str(delta), (10,300),
                cv.FONT_HERSHEY_SIMPLEX,
                1,              # font_scale
                (255,255,255),    # color
                4)              # thickness


    # Save prev frame 
    prev_gray = gray 


    if game_over:
            cv.putText(frame, "GAME OVER!", (w // 3, h // 2),
                        cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            cv.imshow("Game", frame)
            cv.waitKey(3000)
            break

    # Show "Game Over" / Quit


    cv.imshow("CakePopGame", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    # See if user wants to quit
    #if cv.waitKey(1) == ord('q'):
     #   break
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows() 

