# door.py
import cv2, os
from PIL import ImageTk, Image
import time,mail
from bluetooth_test import bt_open,servo_init,bt_close


def door(names, video_w):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "/home/pi/facial_recog/haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cam = cv2.VideoCapture(0)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    mail_flag = 0
    servo_init() #舵机初始化，一次即可，不放入循环

    while True:
        door_sta = ['识别失败，关门', '识别成功，开门，请在3秒内通过','正在确认中，请稍后']
        ret, img = cam.read()
        img = cv2.flip(img, 1)  # 反转摄像头
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        idnum = 0
        confidence = "0%"
        flag = 0

        for (x, y, w, h) in faces:
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # 捕获人脸返回所在位置
            # 检查匹配度是否小于它们 ，100 ==>“0”的匹配度
            if (confidence < 100):
                idnum = names[idnum]
                confidence = "  {0}%".format(round(100 - confidence))  # 显示百分比匹配度
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 显示绿色方框
                flag = 2
                mail_flag += 1
                if (mail_flag == 3):
                    flag = 1
                    mail_flag = 0
                    mail.mail()
                    bt_open()
                    time.sleep(3)
                    bt_close()
                time.sleep(3)
            elif (confidence >= 100):
                idnum = "unknown"  # 否则输出不认识
                confidence = "  {0}%".format(round(100 - confidence))  # 显示百分比匹配度
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 显示红色方框
                flag = 0
                #bt_close()

            cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (255, 255, 255), 2)  # 显示id名
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)  # 显示匹配度


        h, w, _ = img.shape
        wc, hc = video_w, int(h * (video_w / w))
        current_image = Image.fromarray(img, "RGB").resize((wc, hc), Image.LANCZOS)
        img = ImageTk.PhotoImage(image=current_image)

        prumpt = door_sta[flag]


        yield img, str(idnum), str(confidence),str(prumpt)


        #cv2.imshow('camera', img)
        #print(str(door_sta[flag]))

    #    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    #    if k == 27:
    #        break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    door(names=['unknow', 'Tinky'],video_w=800)

