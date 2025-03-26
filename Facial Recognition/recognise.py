# recognise.py
import cv2, os
from PIL import ImageTk, Image


def recognise(names, video_w):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "/home/pi/facial_recog/haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cam = cv2.VideoCapture(0)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
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

        for (x, y, w, h) in faces:
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])  # 捕获人脸返回所在位置
            # 检查匹配度是否小于它们 ，100 ==>“0”的匹配度
            if (confidence < 100):
                idnum = names[idnum]
                confidence = "  {0}%".format(round(100 - confidence))  # 显示百分比匹配度
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 显示绿色方框
            elif (confidence >= 100):
                idnum = "unknown"  # 否则输出不认识
                confidence = "  {0}%".format(round(100 - confidence))  # 显示百分比匹配度
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 显示红色方框

            cv2.putText(img, str(idnum), (x + 5, y - 5), font, 1, (255, 255, 255), 2)  # 显示id名
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)  # 显示匹配度


        h, w, _ = img.shape
        wc, hc = video_w, int(h * (video_w / w))
        current_image = Image.fromarray(img, "RGB").resize((wc, hc), Image.LANCZOS)
        img = ImageTk.PhotoImage(image=current_image)

        yield img, str(idnum), str(confidence)

        cv2.waitKey(10)
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognise(names=['unknow', 'Tinky'])