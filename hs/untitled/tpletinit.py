import cv2 as cv
import numpy as np

img_rgb = cv.imread('nn3.jpg')
img_rgb=cv.resize(img_rgb, dsize=(int(img_rgb.shape[1]*2), int(img_rgb.shape[0]*2)), interpolation=cv.INTER_AREA)

img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('nn1.jpg', 0)
w, h = template.shape[::-1]

res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

threshold = 0.8
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv.imshow('result', img_rgb)
cv.waitKey(0)