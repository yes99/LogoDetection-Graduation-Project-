import cv2
import numpy as np
filename = 'k.png'
img = cv2.imread(filename)
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
surf = cv2.xfeatures2d.SURF_create(50000)
kp, des = surf.detectAndCompute(gray, None)
print(len(kp))
img2 = cv2.drawKeypoints(gray,kp,None,(0,0,255),4)
cv2.imshow('img2', img2)
cv2.waitKey()
cv2.destroyAllWindows()