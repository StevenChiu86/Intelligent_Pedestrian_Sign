# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 19:58:38 2020

@author: user
"""

#%%
import cv2
import numpy as np
import imutils 
from imutils.object_detection import non_max_suppression
import os
import time 
alert_signal=False

def add_greenseconds(postion):
    global alert_signal
    if postion>400 and postion<450 and alert_signal==False:
        with open ('film.txt','w') as f:
                f.write('YES')
                alert_signal=True
    if postion>350 and postion<400 and alert_signal==True:
        with open ('film.txt','w') as f:
                f.write('No')
                alert_signal=False    
os.popen('python ./GUI.py')
kernel_Ero = np.ones((3, 1), np.uint8)
kernel_Dia = np.ones((3, 5), np.uint8)

crossmark=[]
caps = cv2.VideoCapture("Person_crossroad_film.mp4")
caps.set(cv2.CAP_PROP_POS_FRAMES,10)
a,b=caps.read()  #read方法返回一个布尔值和一个视频帧。若帧读取成功，则返回True

b1 = imutils.resize(b,width=min(400, b.shape[1])) 
     # 轉成灰階
b2 = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
    # 高斯模糊:最後一個參數值越大意味著越遠的的像素會有較大的權值，使得模糊效果更明顯
b3 = cv2.GaussianBlur(b2, (9, 9), 10)
    # 變成黑白兩值
ret, b4 = cv2.threshold(b3, 200, 255, cv2.THRESH_BINARY)
    # 侵蝕: 移除影像中的小白雜點、細化影像
b5 = cv2.erode(b4, kernel_Ero, iterations=0)  # 3
    # 膨脹: 連接兩個很靠近但分開的物體
b6 = cv2.dilate(b5, kernel_Dia, iterations=4)  # 1
    # 描繪輪廓, cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），所以读取的图像要先转成灰度的，再转成二值图
  
    
  
    
_,contouts, hie = cv2.findContours(b6, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = contouts
# print(cnt)
for i in cnt:
    # 坐标赋值
    x, y, w, h = cv2.boundingRect(i)
    # roi位置判断
    # print(x, y, w, h)
    # if (5 < x and x < 30) or(340 < x and x < 380)or(x==162):
    if ((0<x<400)&(120<y<225)&(10<w<70)&(0<h<40)):
        LRzero = i
        crossmark.append([x,y])

    # 画出轮廓 第三參數-1表示會出所有輪廓 最後參數表示輪廓線寬度
        # cv2.drawContours(b1, LRzero, -1, (0, 255, 0), 2)
Xmax=400
# for i in range (len(crossmark)):
#     if Xmax<crossmark[i][0]:
#         Xmax=crossmark[i][0]
Xmin=1000
for i in range (len(crossmark)):
    
    if Xmin>crossmark[i][0]:
        Xmin=crossmark[i][0]
 
Xlong = abs(Xmax-Xmin)    
# cv2.imshow('b', b1)

  



#%%


cap = cv2.VideoCapture('Person_crossroad_film.mp4')


fps = cap.get(cv2.CAP_PROP_FPS)
frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# 定义HOG对象，采用默认参数，或者按照下面的格式自己设置
defaultHog = cv2.HOGDescriptor()
# 设置SVM分类器，用默认分类器
defaultHog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())




index = 1

pedestrianmark=[]



while cap.isOpened():
    ret, frame = cap.read() 
    
    # 我是第幾禎
    
     
    # 第一個值為T/F 判斷是否有讀到; 第二個值為照片list
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = imutils.resize(frame,width=min(400, frame.shape[1])) 
     # 轉成灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 高斯模糊:最後一個參數值越大意味著越遠的的像素會有較大的權值，使得模糊效果更明顯
    imgBlur = cv2.GaussianBlur(gray, (9, 9), 10)
    # 變成黑白兩值
    ret, thresh = cv2.threshold(imgBlur, 200, 255, cv2.THRESH_BINARY)
    # 侵蝕: 移除影像中的小白雜點、細化影像
    imgEro = cv2.erode(thresh, kernel_Ero, iterations=0)  # 3
    # 膨脹: 連接兩個很靠近但分開的物體
    imgDia = cv2.dilate(imgEro, kernel_Dia, iterations=4)  # 1
    # 描繪輪廓, cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），所以读取的图像要先转成灰度的，再转成二值图
    
    
    
    
    # --------------行人偵測--------------
    
    (rects, weights) = defaultHog.detectMultiScale(frame, winStride=(4, 4),padding=(4, 4), scale=1.05)
    for (x, y, w, h) in rects:
        if ((0<x<400)&(130<y<160)):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (xA, yA, xB, yB) in pick:
        if ((0<xA+xB<750)&(180<yB<5000)):
            print(xA+xB)
            add_greenseconds((xA+xB))
        # if True:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 255), 2)
            pedestrianmark.append( [(xA+xB)/2,index/fps,((index/fps)*abs(((xA+xB)/2)-Xmin))/abs(Xmax-(xA+xB)/2)])
            if ((index/fps)*abs(((xA+xB)/2)-Xmin))/abs(Xmax-(xA+xB)/2) < 8 :    
                cv2.putText(frame, 'time: ' + str(round(((index/fps)*abs(((xA+xB)/2)-Xmin))/abs(Xmax-(xA+xB)/2), 2)) + 's' , (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            
   
        
            
    # ------------斑馬線偵測-----------------

   
    _,contouts, hie = cv2.findContours(
        imgDia, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = contouts
    # print(cnt)
    for i in cnt:
        # 坐标赋值
        x, y, w, h = cv2.boundingRect(i)
        # roi位置判断
        # print(x, y, w, h)
        # if (5 < x and x < 30) or(340 < x and x < 380)or(x==162):
        if ((0<x<400)&(120<y<225)&(10<w<70)&(0<h<40)):
            LRzero = i
        
        # if w>50 and h>10:
        # if x>10 and w>50 and h>10:

        # 画出轮廓 第三參數-1表示會出所有輪廓 最後參數表示輪廓線寬度
            cv2.drawContours(frame, LRzero, -1, (0, 255, 0), 2)
    
    # cv2.putText(frame, 'fps: ' + str(round(int(fps), 2)), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
    # cv2.putText(frame, 'count: ' + str(frameCount), (0, 100), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,255), 2)
    # cv2.putText(frame, 'frame: ' + str(index), (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
    # cv2.putText(frame, 'time: ' + str(round(index / int(fps), 2)) + 's' , (0,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2)
    
    
    cv2.imshow('frame', frame)
    index += 1
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()