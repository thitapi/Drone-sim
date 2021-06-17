import cv2
import numpy as np

cap=cv2.VideoCapture(0)

while True:
    _, frame =cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, greyMask = cv2.threshold(gray, 7, 255, cv2.THRESH_BINARY)
    gaussMask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)        
    _,threshold2 = cv2.threshold(gray,125,255,cv2.THRESH_OTSU)

    cv2.imshow('frame',frame)
    cv2.imshow('grey mask',greyMask)
    cv2.imshow('gauss mask', gaussMask)
    cv2.imshow('thresh2',threshold2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()