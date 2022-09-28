from PIL import Image as im
from tkinter import *
import time
import threading
import os

class tkgif():
    def __init__(self, file, tk, pos):
        self.file = file
        self.image = im.open(self.file)
        self.images = []
        self.duration = []
        self.tk = tk
        self.fil = None
        self.pos = pos
        self.obj = None
        self.cha = 0
        self.w = None
        self.fname = None
        for i in range(self.image.n_frames):
            self.image.seek(i)
            self.duration.append(self.image.info["duration"]/1000)
            self.fname = self.file.split(".")
            self.fil = "temp/" + str(self.fname[0]) + str(i) + ".png"
            self.image.save(str(self.fil), "PNG")
            self.images.append(PhotoImage(file=self.fil))
    def load(self):
        self.w = Canvas(self.tk)
        self.w.pack()
        self.obj = self.w.create_image((self.pos), image = self.images[self.cha])
    def update(self):
        if self.cha == len(self.images)-1:
            self.cha = 0
        else:
            self.cha += 1
        self.w.itemconfig(self.obj, image = self.images[self.cha])
        time.sleep(self.duration[self.cha])
    def delete(self):
        for i in range(len(self.images)):
            os.remove("C:\\Users\\Johannes\\Downloads\\temp\\" + self.fname[0] + str(i) + ".png")
main = Tk()
test = tkgif("friendly.gif", main, (100,200))    
test.load()
def up():
    while True:
        test.update()
        
thd_1 = threading.Thread(target=up)
thd_1.start()
test.delete()
main.mainloop()


