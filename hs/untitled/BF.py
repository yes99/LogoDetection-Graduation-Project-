import numpy as np
import cv2

imageA = cv2.imread('nn1.jpg')  # 왼쪽 사진
imageB = cv2.imread('nn2.jpg')  # 오른쪽 사진
imageA=cv2.resize(imageA, dsize=(int(imageA.shape[1]/2), int(imageA.shape[0]/2)), interpolation=cv2.INTER_AREA)
imageB=cv2.resize(imageB, dsize=(int(imageB.shape[1]/2), int(imageB.shape[0]/2)), interpolation=cv2.INTER_AREA)

grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
kpA, desA = sift.detectAndCompute(grayA, None)
kpB, desB = sift.detectAndCompute(grayB, None)

bf = cv2.BFMatcher()
matches = bf.match(desA, desB)

sorted_matches = sorted(matches, key=lambda x: x.distance)
res = cv2.drawMatches(imageA, kpA, imageB, kpB, sorted_matches[:30], None, flags=2)

cv2.imshow('res', res)
cv2.waitKey()
cv2.destroyAllWindows()