import cv2
import numpy as np

def nothing(x):
	pass

cap = cv2.VideoCapture(0)

img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('image')

cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

while (1):
	ret, frame = cap.read()
	cv2.imshow('image', img)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	r = cv2.getTrackbarPos('R', 'image')
	g = cv2.getTrackbarPos('G', 'image')
	b = cv2.getTrackbarPos('B', 'image')

	lower_blue = np.array([r, g, b])
	upper_blue = np.array([130, 255, 255])

	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	res = cv2.bitwise_and(frame, frame, mask=mask)

	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)

	k = cv2.waitKey(5)&0XFF
	if k == 81:
		break
	
cv2.destoryAllWindows()