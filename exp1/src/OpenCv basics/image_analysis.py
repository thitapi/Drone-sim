import cv2
import numpy as np

cv2.destroyAllWindows()

img1 = cv2.imread('/home/thitapi/Desktop/images.jpeg', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread('/home/thitapi/Desktop/index.jpeg', cv2.IMREAD_UNCHANGED)
img3 = cv2.imread('/home/thitapi/Desktop/base.jpeg', cv2.IMREAD_UNCHANGED)
img4 = cv2.imread('/home/thitapi/Desktop/dank memeer.png', cv2.IMREAD_UNCHANGED)
img1 = cv2.resize(img1, (225,225), interpolation = cv2.INTER_CUBIC)
img3 = cv2.resize(img3, (224,224), interpolation = cv2.INTER_CUBIC)

add = img2 + img4
addcv = cv2.add(img2,img4)
#wtadd = cv2.addWeighted(img2, 0.5 , img3, 0.5, 0)

rows, col, chan = img3.shape
roi = img2[0:rows, 0:col]
#creating masks using thresholding
img2grey = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2grey, 128, 255, cv2.THRESH_BINARY)
#logical operations
mask_inv = cv2.bitwise_not(mask)
img3_bg = cv2.bitwise_and(roi, roi, mask= mask)
img3_fg = cv2.bitwise_and(img3, img3, mask=mask_inv)

dat= cv2.add(img3_bg, img3_fg)
img2[0:rows, 0:col]=dat

cv2.imshow('mask', mask)
cv2.imshow('mask_inv', mask_inv)
cv2.imshow('img3_bg', img3_bg)
cv2.imshow('img3_fg', img3_fg)
cv2.imshow('dat', dat)
cv2.imshow('addcv', addcv)
#cv2.imshow('add',add)
#cv2.imshow('wtadd', wtadd)
#cv2.imshow('images',img1)
#cv2.imshow('index',img2)
#cv2.imshow('base',img3)
#cv2.imshow('dank memeer',img4)

cv2.imwrite('meme_sticker1.png', addcv)
cv2.waitKey(0)
cv2.destroyAllWindows()