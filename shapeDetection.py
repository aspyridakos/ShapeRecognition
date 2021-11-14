import numpy as np
import cv2 as cv
import imutils
import time
from shapeRecognition import ShapeDetector as sr

shapeOutput = ""
count = 0
xPrevious = None
yPrevious = None

def shapeNameConverter(shapeName, shapeOutput):
    if shapeName == "cirle":
        print("O")
        shapeOutput += "O"
    else:
        print(shapeName[0].upper())
        shapeOutput += shapeName[0].upper()
    return shapeOutput

# Use video capture index 1 (0 = internal webcam, 1 = external webcam)
capture = cv.VideoCapture(1, cv.CAP_DSHOW)

frame_rate = 10
prev = 0

while(count < 5):
      
    time_elapsed = time.time() - prev
    # Capture the video frame
    ret, frame = capture.read()
    if time_elapsed > 1./frame_rate:
        prev = time.time()
  
        # If video not ready, try again
        if not ret: continue
    
        # Convert frame to gray scale
        #resized = cv.resize(frame, 300)
        ratio = frame.shape[0] / float(frame.shape[0])

        grayScale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.blur(grayScale, (10, 10))
        #blur = cv.GaussianBlur(grayScale, (5, 5), 0)
        threshold = cv.threshold(blur, 127, 255, cv.THRESH_BINARY)[1]
        
        circles = cv.HoughCircles(grayScale, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=50, minRadius=1, maxRadius=200)
        
        if circles is not None:
            # Convert circle data into ints
            circles = np.round(circles[0, :].astype("int"))
            # Draw circle around each circle
            for (x, y, r) in circles:
                print('Found a circle!')
                if r > 1:
                    cv.circle(frame, (x, y), r, (0, 255, 0), 4)
                    shape = "circle"



                    if ((xPrevious and yPrevious) and 
                        ((yPrevious * 0.99 < y < yPrevious * 1.01) or 
                        (xPrevious * 0.99 < x < xPrevious * 1.01))):
                        count += 1
                        print('Count: ' + str(count))

            xPrevious = float(x)
            yPrevious = float(y)
        else:
            # Find contours of grayscale frame
                # RETR_TREE: List of hierarchy from parents to children
                # CHAIN_APPROX_SIMPLE: Only take vertices, not edges
            contours = cv.findContours(threshold.copy(), 
                cv.RETR_TREE, 
                cv.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            
            # If no contours found, try again
            if not contours: continue

            shapeObject = sr()
            
            c = contours[-1]
            shape = shapeObject.detect(c)

            # If no shape found, try again
            if shape is None: continue
        
            M = cv.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if ((xPrevious and yPrevious) and 
                ((yPrevious * 0.99 < cY < yPrevious * 1.01) or 
                (xPrevious * 0.99 < cX < xPrevious * 1.01))):
                count += 1 
                print('Count: ' + str(count))
            
            xPrevious = cX
            yPrevious = cY

            # loop over the contours
            #for c in contours:

            #shape = shapeObject.detect(c)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv.drawContours(frame, [c], -1, (0, 255, 0), 2)

        # show the output image
        cv.imshow("Image", frame)
        shapeOutput = shapeNameConverter(shape, shapeOutput)
        # print(shapeNameConverter(shape))

        # CHANGE THIS AFTER
        # cv.waitKey(0)

        # Quit using 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

capture.release()
cv.destroyAllWindows()
