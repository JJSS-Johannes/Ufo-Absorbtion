
#Collision Planes:
#Vertikal: von YStart - Y Ende auf X
#Horizonal: von XStart - X Ende auf Y
class collision_plane_vertical():
    def __init__(self, yStart, yEnd, x):
        self.ay = yStart
        self.ey = yEnd
        self.x = x
    def check_collision(self, hor):
        if hor.y >= self.ay and hor.y <= self.ey and self.x >= hor.ax and self.x <= hor.ex:
            return True
        else:
            return False
    def place (self, yStart, yEnd, x):
        self.ay = yStart
        self.ey = yEnd
        self.x = x
class collision_plane_horizontal():
    def __init__(self, xStart, xEnd, y):
        self.ax = xStart
        self.ex = xEnd
        self.y = y
    def check_collision(self, ver):
        if ver.x >= self.ax and ver.x <= self.ex and self.y >= ver.ay and self.y <= ver.ey:
            return True
        else:
            return False
    def place(self, xStart, xEnd, y):
        self.ax = xStart
        self.ex = xEnd
        self.y = y
#Collision box
#von oben links bis unten rechts
#kann mit anderer box rechts, links, bottom, top collision checks machen
#kann alles glecihzeitig überprüfen
class collision_box():
    def __init__(self, start, finish):
        self.tlX, self.tlY = start
        self.brX, self.brY = finish
        self.width = self.brX - self.tlX
        self.height = self.brY -self.tlY
        self.top = collision_plane_horizontal(self.tlX, self.brX, self.tlY)
        self.bottom = collision_plane_horizontal(self.tlX, self.brX, self.brY)
        self.left  = collision_plane_vertical(self.tlY, self.brY, self.tlX)
        self.right = collision_plane_vertical(self.tlY, self.brY, self.brX)
    def check_collision_bottom(self, cb):
        if self.bottom.check_collision(cb.left) or self.bottom.check_collision(cb.right):
            return True
        else:
            return False
    def check_collision_top(self, cb):
        if self.top.check_collision(cb.left) or self.bottom.check_collision(cb.right):
            return True
        else:
            return False
    def check_collision_left(self, cb):
        if self.left.check_collision(cb.top) or self.left.check_collision(cb.bottom):
            return True
        else:
            return False
    def check_collision_right(self, cb):
        if self.right.check_collision(cb.top) or self.left.check_collision(cb.bottom):
            return True
        else:
            return False
    def check_collision(self, cb):
        if self.check_collision_right(cb) or self.check_collision_left(cb) or self.check_collision_top(cb) or self.check_collision_bottom(cb):
            return True
        else:
            return False
    def place(self, start, finish):
        self.tlX, self.tlY = start
        self.brX, self.brY = finish
        self.width = self.brX - self.tlX
        self.height = self.brY -self.tlY
        self.top.place(self.tlX, self.brX, self.tlY)
        self.bottom.place(self.tlX, self.brX, self.brY)
        self.left.place(self.tlY, self.brY, self.tlX)
        self.right.place(self.tlY, self.brY, self.brX)
