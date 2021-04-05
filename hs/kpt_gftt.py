# GFTTDetector로 특징점 검출 (kpt_gftt.py)

import cv2
import numpy as np
 
img = cv2.imread("k.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Good feature to trac 검출기 생성 ---①
gftt = cv2.GFTTDetector_create() 
# 특징점 검출 ---②
keypoints = gftt.detect(gray, None)
# 특징점 그리기 ---③
img_draw = cv2.drawKeypoints(img, keypoints, None)

# 결과 출력 ---④
cv2.imshow('GFTTDectector', img_draw)
cv2.waitKey(0)
cv2.destrolyAllWindows()