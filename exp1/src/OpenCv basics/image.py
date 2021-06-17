import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('out.avi',fourcc, 20.0, (640,480))

while True:
    #ret returns true if it reads something and frame is the frame
    ret, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out.write(grey)

    cv2.imshow('grey',grey)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.imwrite('demo.png',frame)
cv2.imwrite('demo_grey.jpg',grey)

cap.release()
out.release()
cv2.destroyAllWindows()