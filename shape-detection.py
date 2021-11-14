import numpy as np
import cv2 as cv

capture = cv.VideoCapture(1)

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = capture.read()
  
    # Display the resulting frame
    if ret:
        cv.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
capture.release()
# Destroy all the windows
cv.destroyAllWindows()
