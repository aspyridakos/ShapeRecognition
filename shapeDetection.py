import numpy as np
import cv2 as cv

# Use video capture index 1 (0 = internal webcam, 1 = external webcam)
capture = cv.VideoCapture(1, cv.CAP_DSHOW)

while(True):
      
    # Capture the video frame
    ret, frame = capture.read()
  
    # Display the resulting frame
    if ret:
        cv.imshow('frame', frame)
      
    # Quit using 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
capture.release()
cv.destroyAllWindows()
