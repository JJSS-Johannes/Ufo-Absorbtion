from PIL import Image as im
from tkinter import *
import time
import threading
import os
import io
from PIL import Image, ImageTk

class tkgif():
    def __init__(self, file, tk, canvas, pos):
        self.file = file
        self.image = im.open(self.file)
        self.images = []
        self.duration = []
        self.tk = tk
        self.canvas = canvas
        self.width = self.image.width
        self.height = self.image.height
        self.fil = None
        self.pos = pos
        self.obj = None
        self.cha = 0
        self.fname = None
        for i in range(self.image.n_frames):
            self.image.seek(i)
            self.duration.append(self.image.info["duration"]/1000)
            with io.BytesIO() as f:
                self.image.convert(mode="RGBA").save(f, format='png')
                ima_png = Image.open(f)
                self.images.append(ImageTk.PhotoImage(ima_png))
        self.obj = self.canvas.create_image((self.pos), image = self.images[self.cha])
    def change_frame(self):
        if self.cha == len(self.images)-1:
            self.cha = 0
        else:
            self.cha += 1
        self.canvas.itemconfig(self.obj, image = self.images[self.cha])
        time.sleep(self.duration[self.cha])
    def update(self):
        x = threading.Thread(target=self.change_frame)
        x.start()
    def move(self, x, y):
        self.canvas.move(self.obj,x,y)
        self.pos = self.canvas.coords(self.obj)
    def destroy(self):
        self.canvas.delete(self.obj)
"""
main = Tk()
w = Canvas(main)
w.pack()

test = tkgif("../pictures/enemyleft.gif", main, w,(100,200))

def update():
    while True:
        test.update()
        
thd_1 = threading.Thread(target=update)
thd_1.start()
main.mainloop()
"""


