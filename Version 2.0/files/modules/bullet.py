from modules.fishtools import get_movement
from modules.collision import *
from modules.relabs import *
from tkinter import *

class bullet():
    def __init__(self, x, y, w, damage, health, text):
        self.x = x
        self.y = y
        self.canvas = w
        self.damage = damage
        self.health = health
        self.text = text
        self.path = resource_path0("pictures/bullet.png")
        self.image = PhotoImage(file=self.path)
        self.imageheight = self.image.height()/2
        self.imagewidth = self.image.width()/2
        self.obj = self.canvas.create_image(self.x, self.y, image=self.image)
        self.canvas.lift(self.obj)
        self.target = None
        self.cord1 = self.canvas.coords(self.obj)[0]
        self.cord2 = self.canvas.coords(self.obj)[1]
        self.cobox = collision_box((self.cord1-self.imagewidth, self.cord2-self.imageheight),(self.cord1+self.imagewidth, self.cord2+self.imageheight))
        self.live = True
    def move(self, ucords, ufo):
        if self.target == None:
            self.target = ucords[0], ucords[1]
        self.ax, self.ay = get_movement((self.x, self.y), self.target, 10)

        self.ax = round(self.ax)
        self.ay = round(self.ay)
        
        self.x = self.ax
        self.y = self.ay
        self.canvas.moveto(self.obj, x=self.ax, y=self.ay)
        if self.live:
            self.cord1 = self.canvas.coords(self.obj)[0]
            self.cord2 = self.canvas.coords(self.obj)[1]
            self.cobox.place((self.cord1-self.imagewidth, self.cord2-self.imageheight),(self.cord1+self.imagewidth, self.cord2+self.imageheight))
        if ufo.col_ufo.check_collision(self.cobox):
            self.canvas.delete(self.obj)
            ufo.hit(self.damage, self.health, self.text)
            self.live = False
            return True
        elif self.y <= 72:
            self.canvas.delete(self.obj)
            self.live = False
            return True
        else:
            return False
