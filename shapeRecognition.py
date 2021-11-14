import cv2
class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		vertices = cv2.approxPolyDP(c, 0.04 * peri, True)

		if len(vertices) == 4:
			x, y, width, height = cv2.boundingRect(vertices)
			aspectRatio = float(width) / height

			if aspectRatio >= 0.95 and aspectRatio <= 1.05:
				shape = "square"

		else:
			shape = "circle"
		return shape

