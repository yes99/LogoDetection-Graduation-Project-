import cv2

src = cv2.imread("kk.jpg", cv2.IMREAD_COLOR)
#src=cv2.resize(src, dsize=(int(src.shape[1]/2), int(src.shape[0]/2)), interpolation=cv2.INTER_AREA)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 3)
laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
canny = cv2.Canny(src, 100, 255)
"""
cv2.imshow("sobel", sobel)
cv2.imshow("laplacian", laplacian)
cv2.imshow("canny", canny)
"""
src2 = cv2.imread("kk1.jpg", cv2.IMREAD_COLOR)
#src2=cv2.resize(src2, dsize=(int(src2.shape[1]/2), int(src2.shape[0]/2)), interpolation=cv2.INTER_AREA)

gray2 = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

sobel2 = cv2.Sobel(gray2, cv2.CV_8U, 1, 0, 3)
laplacian2 = cv2.Laplacian(gray2, cv2.CV_8U, ksize=3)
canny2 = cv2.Canny(src2, 100, 255)

detector = cv2.ORB_create()
kp1, desc1 = detector.detectAndCompute(canny, None)
kp2, desc2 = detector.detectAndCompute(canny2, None)

# BF-Hamming 생성 ---②
matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
# knnMatch, k=2 ---③
matches = matcher.knnMatch(desc1, desc2, 2)

# 첫번재 이웃의 거리가 두 번째 이웃 거리의 75% 이내인 것만 추출---⑤
ratio = 0.75
good_matches = [first for first, second in matches \
                    if first.distance < second.distance * ratio]
print('matches:%d/%d' %(len(good_matches),len(matches)))

# 좋은 매칭만 그리기
res = cv2.drawMatches(canny, kp1, canny2, kp2, good_matches, None, \
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
# 결과 출력
cv2.imshow('Matching', res)
cv2.waitKey()
cv2.destroyAllWindows()
