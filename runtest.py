import cv2
import time

mjpg_PATH = "http://localhost:9090/?action=stream"

video = cv2.VideoCapture(mjpg_PATH)

prev_time = 0
FPS = 10

while True:

    ret, frame = video.read()
    
    current_time = time.time() - prev_time

    if (ret is True) and (current_time > 1./ FPS) :
    	
        prev_time = time.time()
        
        cv2.imshow('VideoCapture', frame)
    	
        if cv2.waitKey(1) > 0 :
            
            break
video.release()
