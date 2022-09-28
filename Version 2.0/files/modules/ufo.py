from tkinter import *
from modules.collision import *
import time
import threading

class ufo():
    def __init__(self, pos, vel, w):
        self.x, self.y = pos
        self.vel = vel
        self.w = w
        self.image = PhotoImage(file="pictures/ufo.png")
        self.image_s = PhotoImage(file="pictures/beam.png")
        self.obj = self.w.create_image(self.x+(self.image.width()/2), self.y+(self.image.height()/2), image = self.image)
        self.strahl = w.create_image(self.x+(self.image.width()/2), self.y+(self.image_s.height()/1.3), image = self.image_s, state = "hidden")
        self.w.lift(self.strahl)
        self.beam_vis = False
        self.col_ufo = collision_box((self.w.coords(self.obj)[0]-(self.image.width()/2), self.w.coords(self.obj)[1]-(self.image.height()/2)),(self.w.coords(self.obj)[0]+(self.image.width()/2), self.w.coords(self.obj)[1]+(self.image.height()/2)))
        self.col_beam = collision_box((self.w.coords(self.strahl)[0]-(self.image_s.width()/2), self.w.coords(self.strahl)[1]-(self.image_s.height()/2)),(self.w.coords(self.strahl)[0]+(self.image_s.width()/2), self.w.coords(self.strahl)[1]+(self.image_s.height()/2)))
        self.cooldown = False
    def move(self, v):
        if ((self.x <= -10 and v != 1) or (self.x >= 610 and v != -1)) or (self.beam_vis == True):
            return
        else:
            self.x += v*self.vel
            self.w.move(self.obj, v * self.vel, 0)
            self.w.move(self.strahl, v * self.vel, 0)
            self.col_ufo.place((self.w.coords(self.obj)[0]-(self.image.width()/2), self.w.coords(self.obj)[1]-(self.image.height()/2)),(self.w.coords(self.obj)[0]+(self.image.width()/2), self.w.coords(self.obj)[1]+(self.image.height()/2)))
            self.col_beam.place((self.w.coords(self.strahl)[0]-(self.image_s.width()/2), self.w.coords(self.strahl)[1]-(self.image_s.height()/2)),(self.w.coords(self.strahl)[0]+(self.image_s.width()/2), self.w.coords(self.strahl)[1]+(self.image_s.height()/2)))
    def shoot(self, manager, enemys, friendly, damage, health, text):
        if self.cooldown:
            return [None, None]
        self.w.itemconfig(self.strahl, state="normal")
        self.beam_vis = True
        enemy_delete = []
        friend_delete = []
        for enem in enemys:
            if self.col_beam.check_collision(enem.col_box):
                enem.destroy()
                enemy_delete.append(enem)
        for friend in friendly:
            if self.col_beam.check_collision(friend.col_box):
                friend.destroy()
                friend_delete.append(friend)
                self.hit(damage, health, text)
        x = threading.Thread(target=self.stop_shoot, args=(lambda : manager.stop_threads,))
        x.start()
        return [enemy_delete, friend_delete]
    def stop_shoot(self, stop):
        time.sleep(0.5)
        if stop():
            return
        self.w.itemconfig(self.strahl, state="hidden")
        self.beam_vis = False
        self.cooldown = True
        time.sleep(2)
        self.cooldown = False
    def get_coords(self):
        return self.w.coords(self.obj)
    def hit(self, damage, health, text):
        pr = (damage*100)/500
        lo = (pr*300)/100
        wert1 = self.w.coords(health)[2]
        self.w.coords(health, 100, 442,wert1-lo,471)
        wert = int(self.w.itemcget(text, 'text'))
        self.w.itemconfig(text, text=int(wert)-damage)
        wert = int(self.w.itemcget(text, 'text'))

