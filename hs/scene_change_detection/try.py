import cv2
import numpy as np
import math

def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 10 * math.log10(PIXEL_MAX / math.sqrt(mse))

"""
def psnr11(img1, img2):
    abs = cv2.absdiff(img1, img2)
    print("abs")
    print(abs)    
    abs1 = abs**2
    print("abs1")
    print(abs1)   
    b,g,r = cv2.split(abs1)
    print("bgr")
    sse = sum(b)+sum(g)+sum(r)
    print("sse sum")
    print(sse)
    mse = float(sse/(3 * img.shape[1] * img.shape[0]))
    print("mse")
    print(mse)
   # psnr = 10.0 * math.log10((255 * 255)/mse)
    print("psnr")
    return 10.0 * math.log10((255 * 255)/mse)
"""

video_file = "av2.mp4" # 동영상 파일 경로
cnt1 = 0
cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print ("width = %d  height = %d" %(width, height))
blank_img = cv2.imread('a.png')
blank_img=cv2.resize(blank_img, dsize=(int(width ), int(height)), interpolation=cv2.INTER_AREA)

#tpsnrV = psnr(blank_img, blank_img)
cv2.imshow("blannk", blank_img)
timg = blank_img
t =0
fc= 0
if cap.isOpened():                 # 캡쳐 객체 초기화 확인
    while True:

     
        ret, img = cap.read()      # 다음 프레임 읽기      --- ②
        psnrV = psnr(timg , img)
        #abs1 = tpsnrV
        st = t - psnrV
        

        #print(cnt)
        cnt1 = cnt1 + 1
        #print(psnrV)
        #print("t")
        #print(t)
        print("abs1")
        st = abs(st)
        cnt = "F: %d, psnr: %f" %(cnt1, psnrV)
        cv2.putText(img, cnt, (50, 100),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
        cnt0 = "t : %f abs:%f" %(t, st)
        cv2.putText(img, cnt0, (50, 200),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
    
        #cv2.imwrite("./a/frame%d.png" % cnt1, img)
        print(st)
        if ret:                     # 프레임 읽기 정상
            cv2.imshow(video_file, img) # 화면에 표시  --- ③
            if( st> 1 and fc ==0):
                cnt3 = "stop here"
                cv2.putText(img, cnt3, (50, 400),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
                cv2.imshow(video_file, img) # 화면에 표시  --- ③
                #cv2.imwrite("./a/frame%d stopstopstop.png" % cnt1, img)
                fc = 1
                cv2.waitKey()
            elif (st>1 and fc ==1):
                fc = 0
                cnt4 = "pass pass"
                cv2.putText(img, cnt4, (50, 400),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
                cv2.imshow(video_file, img) # 화면에 표시  --- ③
                #cv2.imwrite("./a/frame%d passpasspass.png" % cnt1, img)
            else:
                #cv2.imwrite("./a/frame%d.png" % cnt1, img)
                cv2.waitKey(25)            # 25ms 지연(40fps로 가정)   --- ④
        else:                       # 다음 프레임 읽을 수 없슴,
            break# 재생 완료
        timg = img
        t = psnrV
    
else:
    print("can't open video.")      # 캡쳐 객체 초기화 실패
cap.release()                       # 캡쳐 자원 반납
cv2.destroyAllWindows()