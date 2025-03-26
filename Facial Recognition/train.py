# train.py
import numpy as np
from PIL import Image
import os
import cv2

def train(datapath = '/home/pi/facial_recog/dataset'):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("/home/pi/facial_recog/haarcascades/haarcascade_frontalface_default.xml")
    faces, ids = getImagesAndLabels(datapath,detector)

    #train recogn model
    recognizer.train(faces, np.array(ids))
    #save model
    recognizer.write('trainer/trainer.yml')

    return "{0} faces trained.".format(len(np.unique(ids)))

def getImagesAndLabels(path,detector=None):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')   # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids

if __name__=="__main__":
    info=train()
    print(info)
