from math import *
import random
def get_movement (pos, fin, dist):
    sx, sy = pos
    fx, fy = fin
    distance = sqrt((fx-sx) ** 2 + (fy-sy)**2)
    if (fy-sy) < 0: #Q 2+3
        if (fx-sx) <0: # Q 2
            c = 3
        else:
            c = 2
    else:  #Q 1+4
        if (fx-sx) < 0: # Q4
            c = 4
        else:
            c = 1
    if distance == 0:
        return pos
    if c % 2 != 0:
        w = acos(abs((fy-sy))/distance)
    else:
        w = acos(abs((fx-sx))/distance)
    if dist >= distance:
        return (fx,fy)
    if dist <= 0:
        return (sx,sy)
    distance -= dist
    if c % 2 != 0:
        vy = cos(w) * distance
        vx = sin(w) * distance
    else:
        vy = sin(w) * distance
        vx = cos(w) * distance
    if fx-sx <0:
        nx = fx + vx
    else:
        nx = fx - vx
    if fy-sy <0:
        ny = fy + vy
    else:
        ny = fy - vy
    return (nx, ny)
def get_distance (pos, fin):
    sx, sy = pos
    fx, fy = fin
    distance = sqrt((fx-sx) ** 2 + (fy-sy)**2)
    return distance
def get_closest (pos, fins):
    u = []
    for i in range (0, len(fins)):
        u.append(get_distance(pos, fins[i]))
    if len(u) == 0:
        return pos
    mi = min(u)
    for i in range (0, len(u)):
        if u[i] == mi:
            return fins[i]
class food():
    def __init__(self,parent,idx, canvas, x,y):
        self.parent = parent
        self.idx = idx
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.display = canvas.create_rectangle(self.x-2,self.y-2,self.x+2,self.y+2,fill="green",outline="green")
    def collect(self, canvas, fish):
        fish.eat()
        canvas.delete(self.display)
        self.parent.remove(self.idx)
class foodSpawner():
    def __init__(self,canvas, maxAmount, Intervall):
        self.c = canvas
        self.foods = [None]*maxAmount
        self.MaxLife = Intervall
        self.life = self.MaxLife
    def generate_new(self):
        for i in range (0, len(self.foods)):
            if self.foods[i] == None:
                self.foods[i] = food(self, i, self.c, random.randint(0,1000),random.randint(0,500))
                return
    def remove(self, foodIdx):
        self.foods[foodIdx] = None
    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.life = self.MaxLife
            self.generate_new()
