import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)



while True:
    _,frame = cap.read()
    gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    sift = cv2.SIFT_create()
    kp = sift.detect(gray,None)

    img=cv2.drawKeypoints(gray,kp,  None, color=(255,0,0))

    cv2.imwrite('sift_keypoints.jpg',frame)
    img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,color=(255,0,0) )
    cv2.imwrite('sift_keypoints.jpg',img)

    sift = cv2.SIFT_create()
    kp, des = sift.detectAndCompute(gray,None)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()