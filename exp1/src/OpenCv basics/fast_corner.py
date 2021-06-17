import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)



while True:
    _,frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = cv2.Laplacian(frame, cv2.CV_64F)
    # find and draw the keypoints

    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector_create()
    kp = fast.detect(frame,None)
    img2 = cv2.drawKeypoints(frame, kp, None, color=(255,0,0))

    # Print all default params
    print("Threshold: ", fast.getThreshold())
    print("nonmaxSuppression: ", fast.getNonmaxSuppression())
    print("neighborhood: ", fast.getType())
    print("Total Keypoints with nonmaxSuppression: ", len(kp))

    cv2.imwrite('fast_true.png',img2)

    # Disable nonmaxSuppression
    fast.setNonmaxSuppression(False)
    kp = fast.detect(frame,None)

    print ("Total Keypoints without nonmaxSuppression: ", len(kp))

    img3 = cv2.drawKeypoints(frame, kp, None , color=(255,0,0))

    cv2.imwrite('fast_false.png',img3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()