import numpy as np
import cv2 as cv
import imutils
import time
import networking
from shapeRecognition import ShapeDetector as sr

shapeOutput = ""
count = 0
xPrevious = None
yPrevious = None

def shapeNameConverter(shapeName, shapeOutput):
    if shapeName == "circle":
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
        
        circles = cv.HoughCircles(grayScale, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=50, minRadius=3, maxRadius=200)
        
        if circles is not None:
            # Convert circle data into ints
            circles = np.round(circles[0, :].astype("int"))

            x = 0.0
            y = 0.0

            # Draw circle around each circle
            for (x, y, r) in circles:
                print('Found a circle!')
                if r > 3:
                    cv.circle(frame, (x, y), r, (0, 255, 0), 4)
                    
                    shape = "circle"
                    
                    if ((xPrevious and yPrevious) and 
                        ((yPrevious * 0.9 > y or y > yPrevious * 1.1) or 
                        (xPrevious * 0.9 > x or x > xPrevious * 1.1))):
                        count += 1
                        shapeOutput = shapeNameConverter(shape, shapeOutput)
                        print('Count: ' + str(count))

            xPrevious = float(x)
            yPrevious = float(y)
        else:
            contours = cv.findContours(threshold.copy(), #Find contours of grayscale frame
                cv.RETR_TREE, #List of hierarchy from parents to children
                cv.CHAIN_APPROX_SIMPLE) #Only take vertices, not edges
            contours = imutils.grab_contours(contours) #Converts contours into a usable array
            
            # If no contours found, try again
            if not contours: continue

            shapeObject = sr()
            
            c = contours[-1]
            shape = shapeObject.detect(c)

            # If no shape found, try again
            # if shape is None: continue
            if shape is not None:
                M = cv.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                if ((xPrevious and yPrevious) and 
                    ((yPrevious * 0.95 > cY or cY > yPrevious * 1.05) or
                    (xPrevious * 0.95 > cX or cX > xPrevious * 1.05))):
                    count += 1 
                    shapeOutput = shapeNameConverter(shape, shapeOutput)
                    print('Count: ' + str(count))
                
                xPrevious = float(cX)
                yPrevious = float(cY)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv.drawContours(frame, [c], -1, (0, 255, 0), 2)

        # show the output image
        cv.imshow("Image", frame)
        

        # Quit using 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

print('Shape output: ', str(shapeOutput))

sender = networking.Sender('127.0.0.1', 42069)
sender.send(shapeOutput)

capture.release()
cv.destroyAllWindows()
