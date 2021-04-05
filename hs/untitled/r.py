import cv2
import numpy as np
import math

mode, drawing=True,False
xi, yi=-1,-1
#주황색
B=255
G=94
R=0
img=cv2.imread('small.jpg',cv2.IMREAD_COLOR)
newimg=img.copy()
def onMouse(event, x, y, flags, frame):
    global xi, yi, drawing, mode, B, G, R

    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        xi, yi=x, y

    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        if mode:
            cv2.rectangle(frame, (xi, yi), (x, y), (B, G, R), 3)
        else:
            r = (xi - x) ** 2 + (yi - y) ** 2
            r = int(math.sqrt(r))
            cv2.circle(frame, (xi, yi), r, (B, G, R), 3)

def mouse_callback(event, x, y, flags, param):
    print("마우스 이벤트 발생, x:", x, "y:", y)

#256*256 에다가 brg
#img=np.zeros((256,256,3), np.uint8)
#newimg.copyTo(img)

cv2.namedWindow('image')

cv2.setMouseCallback('image',onMouse,param=img)

while(True):
    cv2.imshow('image',img)

    k=cv2.waitKey(1)&0xFF
    #비트연산자 & 로 둘다 1인것만 1 운영체제가 64비트라 이런 과정을 해줘야된대
    if k==27:
        #print("ESC키 눌러짐")
        break
    elif k==ord('m'):
        mode=not mode
    elif k==ord('r'):
        img=newimg


cv2.destroyAllWindows()

'''
        elif event==cv2.EVENT_MOUSEMOVE:
            if drawing:
                if mode:
                    cv2.rectangle(frame, (xi,yi),(x,y),(B, G, R),3)
                else:
                    r=(xi-x)**2+(yi-y)**2
                    r=int(math.sqrt(r))
                    cv2.circle(frame,(xi, yi),r,(B, G, R),3)
        '''