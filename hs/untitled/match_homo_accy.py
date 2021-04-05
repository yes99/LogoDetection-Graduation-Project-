# RANSAC 원근 변환 근사 계산으로 나쁜 매칭 제거 (match_homography_accuracy.py)

import cv2, numpy as np

img1 = cv2.imread('ka3.JPG')
img2 = cv2.imread('ka4.jpg')

#img1=cv2.resize(img1, dsize=(int(img1.shape[1]/6), int(img1.shape[0]/6)), interpolation=cv2.INTER_AREA)
#img2=cv2.resize(img2, dsize=(int(img2.shape[1]*2), int(img2.shape[0]*2)), interpolation=cv2.INTER_AREA)

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
sobel1 = cv2.Sobel(gray1, cv2.CV_8U, 1, 0, 3)
laplacian1 = cv2.Laplacian(gray1, cv2.CV_8U, ksize=3)
canny1 = cv2.Canny(img1, 100, 255)

gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
sobel2 = cv2.Sobel(gray2, cv2.CV_8U, 1, 0, 3)
laplacian2 = cv2.Laplacian(gray2, cv2.CV_8U, ksize=3)
canny2 = cv2.Canny(img2, 100, 255)

down1 = cv2.pyrDown(img1)
down1 = cv2.resize(down1, dsize=(int(down1.shape[1] * 2), int(down1.shape[0] * 2)), interpolation=cv2.INTER_AREA)

for i in range(10):
    down1 = cv2.pyrDown(down1)
    down1=cv2.resize(down1, dsize=(int(down1.shape[1]*2), int(down1.shape[0]*2)), interpolation=cv2.INTER_AREA)

#cv2.imshow('down', down1)

down2 = cv2.pyrDown(img2)
down2 = cv2.resize(down2, dsize=(int(down2.shape[1] * 2), int(down2.shape[0] * 2)), interpolation=cv2.INTER_AREA)

for i in range(10):
    down2 = cv2.pyrDown(down2)
    down2=cv2.resize(down2, dsize=(int(down2.shape[1]*2), int(down2.shape[0]*2)), interpolation=cv2.INTER_AREA)
#cv2.imshow('down2', down2)

#down1 = cv2.resize(down1, dsize=(int(down1.shape[1] /2), int(down1.shape[0] /2)), interpolation=cv2.INTER_AREA)

"""
cv2.imshow('sobel', sobel1)
cv2.imshow('laplacian', laplacian1)
cv2.imshow('canny', canny1)
cv2.waitKey()

cv2.imshow('sobel', sobel2)
cv2.imshow('laplacian', laplacian2)
cv2.imshow('canny', canny2)
cv2.waitKey()
"""


# ORB, BF-Hamming 로 knnMatch  ---①
#detector = cv2.xfeatures2d.SURF_create(100,10,True,True)   #700개 까지는 멀쩡함, 800개 부터 엇나감 #300개 쓸만함
detector = cv2.xfeatures2d.SURF_create()

#키포인트랑 디스크립터 한번에 계산해버림
kp1, desc1 = detector.detectAndCompute(canny1, None)
print("키포인트")
print(kp1)
print("디스크립터")
print(desc1)
kp2, desc2 = detector.detectAndCompute(canny2, None)

#매쳐는 BF매쳐 사용
matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = matcher.match(desc1, desc2)


# 매칭 결과를 거리기준 오름차순으로 정렬 ---③
matches = sorted(matches, key=lambda x:x.distance)
print(matches)
# 모든 매칭점 그리기 ---④
res1 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, \
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS) #한쪽만 있는 매칭 결과 그리기 제외

# 매칭점으로 원근 변환 및 영역 표시 ---⑤
src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ])
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ])

# RANSAC으로 변환 행렬 근사 계산 ---⑥
mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
h,w = img1.shape[:2]
pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
print("이게 네모인가")
print(pts)

dst = cv2.perspectiveTransform(pts,mtrx)
img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

# 정상치 매칭만 그리기 ---⑦
matchesMask = mask.ravel().tolist()
res2 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None, \
                    matchesMask = matchesMask,
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
# 모든 매칭점과 정상치 비율 ---⑧
accuracy=float(mask.sum()) / mask.size
print("accuracy: %d/%d(%.2f%%)"% (mask.sum(), mask.size, accuracy))

# 결과 출력
#cv2.imshow('Matching-All', res1)
cv2.imshow('Matching-Inlier ', res2)
cv2.waitKey()
cv2.destroyAllWindows()
