from fishtools import get_movement
from tkinter import *
import time
import functools
import random
from collision import *
import os

sel = Tk()
sel.geometry("250x100")
sel.title("Selection")
sel.resizable(width = 0, height = 0)

schw = Label(sel, justify = "center", text="Difficulty", font="15")
schw.place(x=0, y=15, width = 250)
schwe = Button(sel, text="Easy", font="10", command=lambda:submit(25))
schwe.place(x=20, y=50)
schwm = Button(sel, text="Medium", font="10", command=lambda:submit(50))
schwm.place(x=90, y=50)
schwh = Button(sel, text="Hard",font="10", command=lambda:submit(100))
schwh.place(x=180, y=50)
                    
sel.bind("f", lambda event: submit())
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

t = PhotoImage(file="ufo.png")
k = PhotoImage(file="starhl.png")
bg = PhotoImage(file="bg.png")
player2 = PhotoImage(file="play3.png")
bulle = PhotoImage(file="bullet.png")
drl = []
dll = []
for i in range(0, 6):
    drl.append(PhotoImage(file="ducks/duck_right" + str(i+1) + ".png"))
    dll.append(PhotoImage(file="ducks/duck_left" + str(i+1) + ".png"))
    
w = Canvas(master, width = 800, height = 500)
w.pack()


mbg = w.create_image(400,250,image=bg)
g = w.create_rectangle(0,413, 1000, 500, fill="#933205")
hbb = w.create_rectangle(100, 442, 400, 471, fill="black")
hb = w.create_rectangle(100, 442, 400, 471, fill="lime green")
hbt = w.create_text(75,455, text=500, font="10")

class ufo():
    def __init__(self, pos, vel):
        self.x, self.y = pos
        self.vel = vel
        self.obj = w.create_image(self.x+(t.width()/2), self.y+(t.height()/2), image = t)
        self.col_1 = collision_box((w.coords(self.obj)[0]-(t.width()/2), w.coords(self.obj)[1]-(t.height()/2)),(w.coords(self.obj)[0]+(t.width()/2), w.coords(self.obj)[1]+(t.height()/2)))
    def move(self, v):
        if ((self.x <= -10 and v != 1) or (self.x >= 610 and v != -1)) or (s.vis == True):
            return
        else:
            self.x += v*self.vel
            w.move(self.obj, v * self.vel, 0)
            self.col_1.place((w.coords(self.obj)[0]-(t.width()/2), w.coords(self.obj)[1]-(t.height()/2)),(w.coords(self.obj)[0]+(t.width()/2), w.coords(self.obj)[1]+(t.height()/2)))
            s.move(v*1)
            
def hit(damage):
    pr = (damage*100)/500
    lo = (pr*300)/100
    wert1 = w.coords(hb)[2]
    w.coords(hb, 100, 442,wert1-lo,471)
    wert = int(w.itemcget(hbt, 'text'))
    w.itemconfig(hbt, text=int(wert)-damage)
    wert = int(w.itemcget(hbt, 'text'))
    if wert <= 0:
        lose()
class strahl():
    def __init__(self, ufo):
        self.x = ufo.x
        self.y = ufo.y
        self.vel = ufo.vel
        self.obj = w.create_image(self.x+(t.width()/2), self.y+(k.height()/1.3), image = k, state = "hidden")
        self.live = 25
        self.vis = False
        self.cooldown = 0
        self.ul = 0
        self.ur = 0
        
        self.col_box = collision_box((w.coords(self.obj)[0]-(k.width()/2), w.coords(self.obj)[1]-(k.height()/2)),(w.coords(self.obj)[0]+(k.width()/2), w.coords(self.obj)[1]+(k.height()/2)))
    def move(self, v):
        if self.x <= -10 and v != 1 or self.x >= 610 and v != -1:
            return
        else:
            self.x += v*self.vel
            w.move(self.obj, v * self.vel, 0)
            self.col_box.place((w.coords(self.obj)[0]-(k.width()/2), w.coords(self.obj)[1]-(k.height()/2)),(w.coords(self.obj)[0]+(k.width()/2), w.coords(self.obj)[1]+(k.height()/2)))
    def ch_st(self, mode):
        if mode:
            w.itemconfig(self.obj, state = "hidden")
            self.vis = False
        elif not mode and self.cooldown <= 0:
            self.live = 12
            self.cooldown = 50
            w.itemconfig(self.obj, state = "normal")
            self.vis = True
            for enem in enemys:
                if self.col_box.check_collision(enem.col_box):
                    enem.destroy()
                    enemys.remove(enem)
                    update_text()
            self.ul = self.x
            self.ur = self.x + k.width()
bulletlist = []            
class entity():
    def __init__(self,x, vel, typ):
        self.x = x
        self.y = 413
        self.vel = vel
        self.curim = 0
        self.itemchange = 4
        if typ == 0:
            self.typ = "unfriendly"
            self.obj = w.create_image(self.x+(drl[1].width()/2), self.y-(drl[0].height()/2), image = drl[self.curim])
            #self.curim = 0
        elif typ == 1:
            self.typ = "friendly"
            self.obj = w.create_image(self.x+(player2.width()/2), self.y-(player2.height()/2), image = player2)
        self.col_box = collision_box((w.coords(self.obj)[0]-(player2.width()/2), w.coords(self.obj)[1]-(player2.height()/2)),(w.coords(self.obj)[0]+(player2.width()/2), w.coords(self.obj)[1]+(player2.height()/2)))
        self.target = random.randint(50, 714)
        self.dead = False
        self.shoot_cooldown = random.randint(200, 500)
        if self.target % 2 != 0:
            self.target += 1
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
            if self.itemchange <= 0:
                if self.typ == "unfriendly":
                    if self.curim == 5:
                        self.curim = 0
                    else:
                        self.curim += 1
                    if v == 1:
                        w.itemconfig(self.obj, image = drl[self.curim])
                    elif v == -1:
                        w.itemconfig(self.obj, image = dll[self.curim])
                self.itemchange = 4

            w.move(self.obj, v*self.vel, 0)
            self.x += v*self.vel
            if self.dead != True:
                self.col_box.place((w.coords(self.obj)[0]-(player2.width()/2), w.coords(self.obj)[1]-(player2.height()/2)),(w.coords(self.obj)[0]+(player2.width()/2), w.coords(self.obj)[1]+(player2.height()/2)))
    def destroy(self):
        self.dead = True
        w.delete(self.obj)
        if self.typ == "friendly":
            hit(player_damage)
        else:
            return
    def shoot(self):
        if self.typ == "unfriendly":
            bulletlist.append(bullet(w.coords(self.obj)[0], w.coords(self.obj)[1]))
            self.shoot_cooldown = random.randint(200, 500)
        else:
            return
class bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.obj = w.create_image(self.x, self.y, image=bulle)
        self.target = None
        self.cobox = collision_box((w.coords(self.obj)[0]-(bulle.width()/2), w.coords(self.obj)[1]-(bulle.height()/2)),(w.coords(self.obj)[0]+(bulle.width()/2), w.coords(self.obj)[1]+(bulle.height()/2)))
        self.live = True
    def move(self):
        if self.target == None:
            self.target = w.coords(u.obj)[0], w.coords(u.obj)[1]
        self.ax, self.ay = get_movement((self.x, self.y), self.target, 10)

        self.ax = round(self.ax)
        self.ay = round(self.ay)
        
        self.x = self.ax
        self.y = self.ay
        w.moveto(self.obj, x=self.ax, y=self.ay)
        if self.live:
            self.cobox.place((w.coords(self.obj)[0]-(bulle.width()/2), w.coords(self.obj)[1]-(bulle.height()/2)),(w.coords(self.obj)[0]+(bulle.width()/2), w.coords(self.obj)[1]+(bulle.height()/2)))
        if u.col_1.check_collision(self.cobox):
            hit(player_damage)
            w.delete(self.obj)
            bulletlist.remove(self)
            self.live = False
        elif self.y <= 72:
            w.delete(self.obj)
            bulletlist.remove(self)
            self.live = False


def update():
    s.live -= 1
    s.cooldown -= 1
    for i in range(len(enemys)):
        enemys[i].shoot_cooldown -= 1
        enemys[i].itemchange -= 1
        if enemys[i].shoot_cooldown <= 0:
            enemys[i].shoot()
    if s.live <= 0:
        s.ch_st(True)
    
    
enemys = []
friendly = []
u = ufo((100, 30), 10)
s = strahl(u)
for i in range(0,random.randint(1,3)):
    friendly.append(entity(i*50+50, 2, 1))
for i in range(0,random.randint(5,15)):
    enemys.append(entity(i*50+50, 2, 0))
et = w.create_text(600, 455, text=str(len(enemys))+" Enemys left", font="Calibri 20")
def update_text():
    w.itemconfig(et, text = str(len(enemys))+" Enemys left")
w.lift(s.obj)
def on_close():
    os._exit(0)
master.bind('a', lambda event: u.move(-1))
master.bind('d', lambda event: u.move(1))
master.bind('<space>', lambda event: s.ch_st(False))
master.protocol("WM_DELETE_WINDOW", on_close)
test = False

def win():
    global game_loop
    master.withdraw()
    game_loop = False
    master2 = Tk()
    master2.geometry("100x50")
    master2.resizable(width=0, height=0)
    l = Label(master2, text="WIN!", justify="center", fg="green", font="Calibri 30")
    l.place(x=0, y=0, width=100)
def lose():
    global game_loop
    master.withdraw()
    game_loop = False
    master2 = Tk()
    master2.geometry("125x50")
    master2.resizable(width=0, height=0)
    l = Label(master2, text="LOOSE!", justify="center", fg="red", font="Calibri 30")
    l.place(x=0, y=0, width=125)


while game_loop:
    if len(bulletlist) > 0:
        for i in bulletlist:
            i.move()
    master.update()
    master.update_idletasks()
    update()
    for i in range(len(enemys)):
        enemys[i].random_move()
    for i in range(len(friendly)):
        friendly[i].random_move()
    if len(enemys) <= 0:
        win()
    time.sleep(0.02)




