import cv2 as cv
class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, contours):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv.arcLength(contours, True)

		# Minimum perimeter
		if peri < 10:
			return
		vertices = cv.approxPolyDP(contours, 0.04 * peri, True)

		if len(vertices) == 4:
			(x,y, width, height) = cv.boundingRect(vertices)
			ar = width / float(height)
			shapeArea = cv.contourArea(contours)
			squareArea = width * height
			print('Square area: {}'.format(squareArea))
			print('Shape area: {}'.format(shapeArea))
			if 0.6 <= squareArea / shapeArea <= 2 :
				shape = "square"
			else:
				shape = "plus"

		elif len(vertices) == 7:
			shape = "arrow"
		elif len(vertices) == 12:
			shape = "plus"
		else:
			print('No shape found.')
			return
		
		print(len(vertices))
		print(shape)
		return shape

