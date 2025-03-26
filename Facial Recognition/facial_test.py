import numpy as np
import cv2

faceCascade = cv2.CascadeClassifier('/home/pi/facial_recog/haarcascades/haarcascade_frontalface_default.xml')#加载分类器路径和文件
cap = cv2.VideoCapture(0)

cap.set(3,640) # set Width
cap.set(4,480) # set Height

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.1,#表示每次图像尺寸减小的比例
        minNeighbors=10,   #表示一个目标至少要被检测5次才会被认定为人脸  
        minSize=(80,80), #目标最小尺寸
        maxSize=(400,400)
    )
    for (x,y,w,h) in faces:#如果检测到人脸返回方框
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)#更改此函数数据可改变方框的大小其实位置颜色
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
    cv2.imshow('Gray',img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    
cap.release()
cv2.destroyAllWindows()
