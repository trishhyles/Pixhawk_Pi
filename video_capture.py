import cv2
import cv2.cv as cv
import numpy as np

count = 0

# Set the size of the video to 320x240 so rpi can process faster
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)

def nothing(x):
	pass
'''
def Trackbar_crate():	
	cv2.createTrackbar('H_upper', 'image', 30, 179, nothing)
	cv2.createTrackbar('H_lower', 'image', 0, 179, nothing)
	cv2.createTrackbar('S_upper', 'image', 255, 255, nothing)
	cv2.createTrackbar('S_lower', 'image', 135, 255, nothing)
	cv2.createTrackbar('V_upper', 'image', 255, 255, nothing)
	cv2.createTrackbar('V_lower', 'image', 181, 255, nothing)
'''
#img = np.zeros((200, 300, 3), np.uint8)
#cv2.namedWindow('image')
#cv2.namedWindow('closing')
#Trackbar_crate()

kernel = np.ones((5,5),np.uint8)

while (1):
	ret, frame = cap.read()
	#cv2.imshow('image', img)

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	H_upper = 30#cv2.getTrackbarPos('H_upper', 'image')
	H_lower = 0#cv2.getTrackbarPos('H_lower', 'image')
	S_upper = 255#cv2.getTrackbarPos('S_upper', 'image')
	S_lower = 135#cv2.getTrackbarPos('S_lower', 'image')
	V_upper = 255#cv2.getTrackbarPos('V_upper', 'image')
	V_lower = 181#cv2.getTrackbarPos('V_lower', 'image')

	lower_blue = np.array([H_lower, S_lower, V_lower])
	upper_blue = np.array([H_upper, S_upper, V_upper])
	#print lower_blue
	#print upper_blue

	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	dilation = cv2.dilate(mask, kernel, iterations = 1)
	closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
	closing = cv2.GaussianBlur(closing, (5,5), 0)

	# Detect circles using HoughCircles
	circles = cv2.HoughCircles(closing, cv.CV_HOUGH_GRADIENT, 2, 120, 
		param1=120, param2=50, minRadius=10, maxRadius=0)
	# circles = np.uint16(np.around(circles))

	#Draw Circles
	if circles is not None:
			for i in circles[0,:]:
				# If the ball radius is small, draw it in green
				if int(round(i[2])) < 30:
					cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,255,0),5)
					cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,255,0),10)
					print 'x=', int(round(i[0])), ' '
					print 'y=', int(round(i[1])), ' ' 
					count = count + 1
				# If the ball radius is big, draw it in red
				elif int(round(i[2])) > 35:
					cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),int(round(i[2])),(0,0,255),5)
					cv2.circle(frame,(int(round(i[0])),int(round(i[1]))),2,(0,0,255),10)
					print 'x=', int(round(i[0])), ' '
					print 'y=', int(round(i[1])), '\n'
					count = count + 1
#	cv2.imshow('frame', frame)
	#cv2.imshow('mask', mask)
#	cv2.imshow('closing', closing)
	print count
	k = cv2.waitKey(5)&0XFF
	if k == 27:
		break

cap.ralease()
cv2.destoryAllWindows()
