import cv2
import numpy as np
import math
#psnr을 구하는 것을 딱히 미련을 갖지 말자, 대충 [수치를 따져서 앞이랑 전이랑 차이가 크게 나면] 멈춰! 가 나오는 거 정도로 알면된다. 
#발표할 상황이 생기면 내가 알아가서 교수님 앞에서 말하겠다. 
#이거랑 SSIM 이라는 기법이 있다.
def psnr(img1, img2):
    mse = np.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 10 * math.log10(PIXEL_MAX / math.sqrt(mse))


video_file = "av2.mp4" # 동영상 파일 경로   #동영상을 뽑아와야겠지
cnt1 = 0
cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①

#동영상 크기 설정이다, 나중에 정말로 필요하더라.
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)    
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


print ("width = %d  height = %d" %(width, height)) #디버깅 한번 해주고
blank_img = cv2.imread('a.png') #흰색 종이를 읽어왔다. # psnr을 앞뒤를 비교하는 거라서 처음에 초기화 할 거리가 필요함. 

blank_img=cv2.resize(blank_img, dsize=(int(width ), int(height)), interpolation=cv2.INTER_AREA) #크기 안맞으면, 나중에 psnr 비교할때 뱉어내서 지금 흰종이 크기를, 맞춰준거임.

timg = blank_img
t =0    #psnr 값 비교를 위한 초기화
fc= 0   #flag change의 약자임, 플래그로 두번 멈추는거 컨트롤 하려고 만들었음

if cap.isOpened():                 # 캡쳐 객체 초기화 확인
    while True:

        ret, img = cap.read()      # 다음 프레임 읽기      --- ②
        psnrV = psnr(timg , img)  #psnr 함수 위에 나온거 쓰는거, 사실 psnr수치 자체가 , 파라미터로 들어간 두 이미지 사이 비교해서 보여주는 거긴 하다.  
                                  #일단 img는 비디오 프레임 읽어오는거고 t(emp)img 는 맨처음에 흰 종이. 
        st = t - psnrV            #standard, 두가지 비교하려고 넣은 값임
        cnt1 = cnt1 + 1           #cnt1은 이미지 저장해서 나올때 이름 비교하려고 만들었음.
        print("abs1")             
        st = abs(st)              #터미널 상에서 차이가 몇이나 나오나 확인하려고 만들었음.
        text = "F: %d, psnr: %f" %(cnt1, psnrV)  #화면에 해당 이미지의 프레임 넘버    psnr수치, 
        cv2.putText(img, text, (50, 100),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
        text0 = "t : %f abs:%f" %(t, st)   #해당 화면의 t 이전 프레임의 psnr 그리고 st는 앞과 뒤의 차이
        cv2.putText(img, text0, (50, 200),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
    
        print(st)
        if ret:                     # 프레임 읽기 정상일 경우
            cv2.imshow(video_file, img) # 화면에 표시  --- ③
            if( st> 1 and fc ==0):      #해당 psnr 값의 앞 뒤 차이가 1보다 크고 플래그가 0일경우에는
                text3 = "stop here"     #멈추게 한다.
                cv2.putText(img, text3, (50, 400),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
                cv2.imshow(video_file, img) # 화면에 표시  --- ③
                fc = 1                   #한번 멈추면 분명 그 다음에 또 같은 이유로 멈춰서 플래그를 세워준다
                cv2.waitKey()
            elif (st>1 and fc ==1):      #st가 1보다 크지만, 이전에 바로 멈춘 상태여서 fc가 1일경우에는 그냥 패스하게 해준다
                fc = 0                   #그리고 fc를 0으로 바꿔라
                text4 = "pass pass"
                cv2.putText(img, text4, (50, 400),  cv2.FONT_HERSHEY_DUPLEX, 3, (0, 200, 0), 10)
                cv2.imshow(video_file, img) # 화면에 표시  --- ③
            else:                         # 그 외에는 그냥 넘겨
                cv2.waitKey(25)            # 25ms 지연(40fps로 가정)   --- ④
        else:                       # 다음 프레임 읽을 수 없슴,
            break# 재생 완료
        timg = img                  #timg 는 일단 이제 그 다음 프레임의 이미지로 바꿔주고
        t = psnrV                   #psnrV를 비교하기 위한 t는 현제 psnr 값으로 바꿔준다.
    
else:
    print("can't open video.")      # 캡쳐 객체 초기화 실패
cap.release()                       # 캡쳐 자원 반납
cv2.destroyAllWindows()