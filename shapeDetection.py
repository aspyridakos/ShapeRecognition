import numpy as np
import cv2 as cv
from shapeRecognition import ShapeDetector as sr

# Use video capture index 1 (0 = internal webcam, 1 = external webcam)
capture = cv.VideoCapture(1, cv.CAP_DSHOW)

while(True):
      
    # Capture the video frame
    ret, frame = capture.read()
  
    # Display the resulting frame
    if ret:
        # Convert frame to gray scale
        grayScale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        # Find contours of grayscale frame
            # RETR_EXTERNAL: Take most outer contours
            # CHAIN_APPROX_SIMPLE: Only take vertices, not edges
        contours = cv.findContours(grayScale.copy(), 
            cv.RETR_EXTERNAL, 
            cv.CHAIN_APPROX_SIMPLE)
        
        shape = sr()
        cv.imshow('frame', frame)
      

#     # loop over the contours
# for c in contours:
# 	# compute the center of the contour, then detect the name of the
# 	# shape using only the contour
# 	M = cv2.moments(c)
# 	cX = int((M["m10"] / M["m00"]) * ratio)
# 	cY = int((M["m01"] / M["m00"]) * ratio)
# 	shape = sd.detect(c)
# 	# multiply the contour (x, y)-coordinates by the resize ratio,
# 	# then draw the contours and the name of the shape on the image
# 	c = c.astype("float")
# 	c *= ratio
# 	c = c.astype("int")
# 	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
# 	cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
# 		0.5, (255, 255, 255), 2)
# 	# show the output image
# 	cv2.imshow("Image", image)
# 	cv2.waitKey(0)

    # Quit using 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
capture.release()
cv.destroyAllWindows()
