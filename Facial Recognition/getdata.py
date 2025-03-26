# getdata.py
import cv2,os
import numpy
from PIL import Image,ImageTk

def getdata(face_id,video_w):
    face_detector = cv2.CascadeClassifier("/home/pi/facial_recog/haarcascades/haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)
    count = 0

    minW = 0.2 * cap.get(3)
    minH = 0.2 * cap.get(4)

    while True:
        sucess, img = cap.read()
        if sucess:
            img = cv2.flip(img, 1)  # 反转摄像头
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(  # faces的值为人脸的坐标
                gray,
                scaleFactor=1.01,
                minNeighbors=10,
                minSize=(int(minW), int(minH)),
            )
            #faces为人脸的坐标

            #标注出正在采集的人脸
            if len(faces) != 0:
                x, y, w, h = faces[0]
                cv2.rectangle(img, (x, y), (x + w, y + w), (0, 255, 0),2)
                cv2.imwrite("/home/pi/facial_recog/dataset/" + str(face_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
                count += 1

            h, w, _ = img.shape
            wc ,hc= video_w,int(h * (video_w / w))
            current_image = Image.fromarray(img,"RGB").resize((wc,hc),Image.LANCZOS)
            img= ImageTk.PhotoImage(image=current_image)
            yield img

        cv2.waitKey(1)

        if count > 25:
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__=="__main__":
    images=getdata(face_id=0,video_w = 800)
    cv2.namedWindow("show",0)
    for i in range(100):
         cv2.imshow("show",images.__next__())
    for i in images:
         cv2.imshow("show",i)
