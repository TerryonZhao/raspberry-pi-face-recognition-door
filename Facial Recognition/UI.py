# ui.pyw
import tkinter as tk
import cv2,os,time
from PIL import ImageTk,Image
import getdata,train,recognise,door

#Initial wide = 800， height = 500；all muti 3/5
class Display():
    def __init__(self,wide=800, height=500):
        self.W, self.H = wide, height
        self.button_w, self.button_h = 100, 30
        #button stretch
        self.button_hstretch= 10
        self.button_wstretch = 10

        self.samlpe_path="/home/pi/facial_recog/dataset"
        #self.cv_model='cv_model'
        self.recognition_model_path='/home/pi/facial_recog/trainer'

        self.show_state=False
        self.video_source=None

        self._init_root()

    def run(self):
        self.root.mainloop()

    def _init_root(self):
        #creat window
        self.root=tk.Tk()
        self.root.title("Face Detector System")
        self.root.config(background="white")
        self.root.geometry(str(self.W) + "x" + str(self.H) + "+100+60")
        self.root.resizable(0, 0)
        #self.root.iconbitmap("./image/icon.ico")
        self.root.attributes("-alpha", 0.95)

        """left area"""
        # creat video area
        self.video_w, self.video_h= int(3 / 4 * self.W) - 1, int(self.H) - 2
        self.video = tk.Label(self.root, bg="black", fg="green",cursor="cross")
        self.video.place(x=1, y=1, w=self.video_w, h=self.video_h-35)

        #state area
        self.text = tk.Label(self.root, text="----------------")
        self.text.place(x=1, y=self.video_h-32, w=self.video_w, h=30)

        """right area"""
        right_x, right_y = 7 / 8 * self.W - 1 / 2 * self.button_w, 3 / 11 * self.H
        #entry
        tk.Label(self.root, text="name:",bg="white",justify="left")\
            .place(x=right_x, y= right_y-70, w=40, h=20)
        self.name_input=tk.Entry(self.root,bd=5, relief="groove")
        self.name_input.place(x=right_x, y= right_y-50, w=self.button_w, h=self.button_h)

        #button
        tk.Button(self.root, text="信息采集", relief="groove", command=self._sample_collect)\
            .place(x=right_x, y= right_y-20, w=self.button_w, h=self.button_h)
        tk.Button(self.root, text="模型训练", relief="groove", command=self._train)\
            .place(x=right_x, y= right_y+2*self.button_h+self.button_hstretch, w=self.button_w, h=self.button_h)
        tk.Button(self.root, text="识别", relief="groove", command=self._detect_start)\
            .place(x=right_x, y= right_y+4*(self.button_h+self.button_hstretch), w=1/2*self.button_w, h=self.button_h)
        tk.Button(self.root, text="结束", relief="groove", command=self._detect_end)\
            .place(x=right_x+1/2*self.button_w, y= right_y+4*(self.button_h+self.button_hstretch), w=1/2*self.button_w, h=self.button_h)
        tk.Button(self.root, text="门禁识别", relief="groove", command=self._door) \
            .place(x=right_x, y=right_y + 6 * (self.button_h + self.button_hstretch),w=self.button_w, h=self.button_h)

    def _sample_collect(self):
        self.text.config(text='Collect Object: '+"")
        self.text.update()

        face_id = len(self._load_labels())
        # 生成器
        self.video_source = getdata.getdata(face_id,self.video_w)
        for img in self.video_source:
            self.video.config(image=img)
            self.video.update()

        # names save all name,and face_id is id of the name
        self._save_labels()

    def _train(self):
        self.text.config(text="training...")
        self.text.update()
        info=train.train(datapath = self.samlpe_path)
        self.text.config(text=info)
        self.text.update()

    def _detect_start(self):
        # 生成器
        self.video_source=recognise.recognise( names =self._load_labels(),video_w=self.video_w)
        for img,id,confidence in self.video_source:
            self.video.config(image=img)
            self.video.update()
            self.text.config(text='Object: '+id+" confidence:"+confidence)
            self.text.update()

    def _detect_end(self):
        if self.video_source is not None:
            self.video_source.close()

    def _door(self):
        self.video_source=door.door( names =self._load_labels(),video_w=self.video_w)
        for img,id,confidence,prumpt in self.video_source:
            self.video.config(image=img)
            self.video.update()
            self.text.config(text='Object: '+id+" confidence:"+confidence+'---'+prumpt)
            self.text.update()

    #save name
    def _save_labels(self):
        new_label=self.name_input.get()
        import labels
        names=labels.names
        if new_label not in names and new_label!="":
            names.append(new_label)
        with open("labels.py","w",encoding="utf-8") as f:
            f.write("#coding=utf-8\n")
            f.write("names="+str(names))

    def _load_labels(self):
        import labels
        return labels.names


if __name__=="__main__":
    ds=Display()
    ds.run()
