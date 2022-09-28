from modules.tkgif import *
from modules.collision import *
from modules.bullet import * 
import random
from PIL import Image, ImageTk
import sys

class entity():
    def __init__(self, x, vel, typ, master, canvas):
        self.x = x
        self.y = 413
        self.vel = vel
        self.master = master
        self.canvas = canvas
        self.height = None
        self.width = None
        self.cooldown = True
        self.cooldown_time = random.randint(5, 15)
        self.dead = False
        if typ == 0:
            self.typ = "unfriendly"
            im = Image.open("pictures/enemyleft.gif")
            self.height = im.width/2
            self.width = im.height/2
            self.x = self.x + self.height
            if self.x % 2 != 0:
                self.x += 1
            self.y = self.y - self.width
            self.obj = tkgif("pictures/enemyleft.gif", self.master, self.canvas, (self.x, self.y))
        elif typ == 1:
            self.typ = "friendly"
            im = Image.open("pictures/friendly.gif")
            self.height = im.width/2
            self.width = im.height/2
            self.x = self.x + self.height
            if self.x % 2 != 0:
                self.x += 1
            self.y = self.y - self.width
            self.obj = tkgif("pictures/friendly.gif", self.master, self.canvas, (self.x, self.y))
        self.col_box = collision_box((self.obj.pos[0]-self.width, self.obj.pos[1]-self.height),(self.obj.pos[0]+self.width, self.obj.pos[1]+self.height))
        self.target = random.randint(50, 714)
        self.dead = False
        self.shoot_cooldown = random.randint(200, 500)
        if self.target % 2 != 0:
            self.target += 1
    def get_game(self):
        sys.path.append("../Ufo_Absorbtion")
        print("1")
        from Ufo_Absorbtion import testvar
        print("2")
        print(testvar)
        print("3")
    def update(self, stop):
        while True:
            self.obj.change_frame()
            if stop():
                break
    def random_move(self):
        if self.target < self.x:
            v = -1
        elif self.target > self.x:
            v = 1
        if self.target == self.x:
            self.target = random.randint(50,715)
            if self.target % 2 != 0:
                self.target += 1
            v = 0
        self.move(v)
    def move(self, v):
        if self.x <= 50 and v != 1 or self.x >= 715 and v != -1:
            return
        else:
            self.obj.move(v*self.vel, 0)
            self.x += v*self.vel
            if self.typ == "unfriendly":
                if v == -1 and self.obj.file == "pictures/enemyright.gif":
                    self.obj.destroy()
                    self.obj = tkgif("pictures/enemyleft.gif", self.master, self.canvas, (self.x, self.y))
                elif v == 1 and self.obj.file == "pictures/enemyleft.gif":
                    self.obj.destroy()
                    self.obj = tkgif("pictures/enemyright.gif", self.master, self.canvas, (self.x, self.y))
            if self.dead != True:
                self.col_box.place((self.obj.pos[0]-self.width, self.obj.pos[1]-self.height),(self.obj.pos[0]+self.width, self.obj.pos[1]+self.height))
    def destroy(self):
        self.dead = True
        self.obj.destroy()
    def shoot(self):
        while True:
            time.sleep(self.cooldown_time)
            if (self.typ == "unfriendly") and (self.dead == False):
                self.cooldown_time = random.randint(5,15)
                return self.obj.pos
            else:
                break

