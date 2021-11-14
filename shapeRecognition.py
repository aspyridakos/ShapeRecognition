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
		vertices = cv.approxPolyDP(contours, 0.01 * peri, True)

		if len(vertices) == 4:
			(x,y, width, height) = cv.boundingRect(vertices)
			ar = width / float(height)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			# shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

			shapeArea = cv.contourArea(contours)
			# if 0.95 < area/ar < 1.05:
				# shape = "square"
			# else:
			# 	shape = "plus"

			squareArea = width * height
			if squareArea > shapeArea:
				shape = "plus"
			else:
				shape = "square"

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

