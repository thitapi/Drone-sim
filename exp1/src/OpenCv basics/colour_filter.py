import cv2
import numpy as np
from numpy.core.defchararray import upper

cap=cv2.VideoCapture(0)

while True:
    _, frame =cap.read()
    hsv= cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array([110,60,50])
    upper = np.array([123,255,255])

    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5), np.int8)
    erosion = cv2.erode(mask, kernel, iterations= 1)
    dilation = cv2.dilate(mask, kernel, iterations= 1)

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    color = cv2.bitwise_and(frame, frame, mask=opening)

    cv2.imshow('frame', frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('opening', opening)
    #cv2.imshow('closing', closing)
    cv2.imshow('result', color)
    #cv2.imshow('erode', erosion)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()