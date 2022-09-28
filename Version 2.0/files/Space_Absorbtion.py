from modules.fishtools import get_movement
from modules.collision import *
from modules.tkgif import tkgif
from modules.ufo import ufo
from modules.entity import *
from modules.bullet import *
from modules.mythread import *
from tkinter import *
import threading
import time
import random
import pyautogui
import os

sel = Tk()
sel.geometry("250x100")
sel.title("Selection")
sel.resizable(width = 0, height = 0)

schw = Label(sel, justify = "center", text="Difficulty", font="15")
schw.place(x=0, y=15, width = 250)
schwe = Button(sel, text="Easy", font="Calibri1 15", command=lambda:submit(25))
schwe.place(x=20, y=50)
schwm = Button(sel, text="Medium", font="Calibri 15", command=lambda:submit(50))
schwm.place(x=90, y=50)
schwh = Button(sel, text="Hard",font="Calibri 15", command=lambda:submit(100))
schwh.place(x=180, y=50)
                    
player_damage = 0
def on_close():
    sel.quit()
    sel.destroy()
    os._exit(0)
def submit(dam):
    global game_sel, game_loop, player_damage
    sel.destroy()
    game_sel = False
    game_loop = True
    player_damage = dam
game_sel = True
game_loop = False
sel.protocol("WM_DELETE_WINDOW", on_close)
sel.mainloop()


master = Tk()
master.geometry("800x500")
master.title("UFO")
master.resizable(width = 0, height = 0)

bg = PhotoImage(file="pictures/bg.png")
  
w = Canvas(master, width = 800, height = 500)
w.pack()


mbg = w.create_image(400,250,image=bg)
g = w.create_rectangle(0,413, 1000, 500, fill="#933205")
hbb = w.create_rectangle(100, 442, 400, 471, fill="black")
hb = w.create_rectangle(100, 442, 400, 471, fill="lime green")
hbt = w.create_text(75,455, text=500, font="10")

bulletlist = []    
enemys = []
friendly = []
u = ufo((100, 30), 10, w)

for i in range(0,random.randint(1,3)):
    friendly.append(entity(i*50+50, 2, 1, master, w))
for i in range(0,random.randint(3,12)):
    enemys.append(entity(i*50+50, 2, 0, master, w))
et = w.create_text(600, 455, text=str(len(enemys))+" Enemys left", font="Calibri 20")
def on_close_wl():
    os._exit(0)
def win():
    master.withdraw()
    master2 = Tk()
    master2.geometry("100x50")
    master2.resizable(width=0, height=0)
    master2.protocol("WM_DELETE_WINDOW", on_close_wl)
    l = Label(master2, text="WIN!", justify="center", fg="green", font="Calibri 30")
    l.place(x=0, y=0, width=100)
    master2.mainloop()
def lose():
    master.withdraw()
    master2 = Tk()
    master2.geometry("125x50")
    master2.resizable(width=0, height=0)
    master2.protocol("WM_DELETE_WINDOW", on_close_wl)
    l = Label(master2, text="LOOSE!", justify="center", fg="red", font="Calibri 30")
    l.place(x=0, y=0, width=125)
    master2.mainloop()
class Manager():
    stop_threads = False
    def update_text():
        w.itemconfig(et, text = str(len(enemys))+" Enemys left")
    def end_all():
        Manager.stop_threads = True
    def ufo_shoot(damage, hb, hbt):
        global enemys, friendly
        deletion = u.shoot(Manager, enemys, friendly, damage, hb, hbt)
        if deletion[0] == None:
            return
        for enemy in deletion[0]:
            enemy.dead = True
            enemys.remove(enemy)
            del enemy
        for friend in deletion[1]:
            friendly.remove(friend)
    def enemy_shoot(enemy, stop):
        while True:
            check_shoot = enemy.shoot()
            if check_shoot == None:
                return
            if stop():
                break
            bulletlist.append(bullet(check_shoot[0], check_shoot[1], w, player_damage, hb, hbt))
    def game_update(stop):
        global bulletlist, game_loop
        Manager.entity_update()
        while game_loop:
            if stop():
                break
            Manager.update_text()
            if len(bulletlist) > 0:
                for i in bulletlist:
                    dele = i.move(u.get_coords(), u)
                    if dele == True:
                        bulletlist.remove(i)
            for enemy in enemys:
                try:
                    enemy.random_move()
                except:
                    pass
            for friend in friendly:
                friend.random_move()
            if len(enemys) == 0:
                Manager.end_all()
                win()
            if int(w.itemcget(hbt, "text")) <= 0:
                Manager.end_all()
                lose()
            time.sleep(0.025)
    def entity_update():
        for friend in friendly:
            x1 = MyThread(target=friend.update, args =(lambda : Manager.stop_threads, ))
            x1.start()
        for enemy in enemys:
            x2 = MyThread(target=enemy.update, args =(lambda : Manager.stop_threads, ))
            x2.start()
            x3 = MyThread(target=Manager.enemy_shoot, args=(enemy,lambda : Manager.stop_threads,))
            x3.start()
def on_close():
    Manager.end_all()
    master.quit()
    master.destroy()
    os._exit(0)
master.bind('a', lambda event: u.move(-1))
master.bind('d', lambda event: u.move(1))
master.protocol('WM_DELETE_WINDOW', on_close)
master.bind('<space>', lambda event: Manager.ufo_shoot(player_damage, hb, hbt))

x = MyThread(target=Manager.game_update, args =(lambda : Manager.stop_threads, ))
x.start()

master.mainloop()


