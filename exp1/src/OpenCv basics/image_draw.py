import numpy as np 
import cv2

img = cv2.imread('demo.png', cv2.IMREAD_REDUCED_COLOR_2)
exp = cv2.imread('demo.png', cv2.IMREAD_UNCHANGED)

cv2.line(exp, (0,0), (150,150), (255,255,255), 5)
cv2.rectangle(exp, (150,150), (200,200), (0,0,0), -1)
font=cv2.FONT_HERSHEY_COMPLEX
cv2.putText(exp, 'Bruh!', (0,150), font,1, (200,255,255), 2, cv2.LINE_AA)


cv2.imshow('demo_exp', exp)
cv2.imshow('demo',img)
cv2.waitKey(0)
cv2.imwrite('exp_image.png',exp)
cv2.destroyAllWindows()
