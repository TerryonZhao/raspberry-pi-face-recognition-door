import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3,640) #设置宽
cap.set(4,480) #设置高

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) #反转摄像头
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)#BGR模式
    cv2.imshow('gray', gray)#灰色窗口
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # 摁下ESC关闭窗口（ESC的ascll码为27）
        break
    
cap.release()
cv2.destroyAllWindows()
