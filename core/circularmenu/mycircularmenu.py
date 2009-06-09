from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import degrees,sqrt,acos



class MTCircularMenu(MTWidget): 
    def __init__(self, **kwargs):
        kwargs.setdefault('radius', 200)
        super(MTCircularMenu, self).__init__(**kwargs)
        self.radius = kwargs.get('radius')
        self.A = self.pos #first vertex of the triangle
        self.B = (self.pos[0]+self.radius,self.pos[1]) #second vertex of the triangle
        self.C = (0,0) #third vertex of the triangle
        self.angle = 0.0
        self.rotation = 0.0
        self.begin_rotation = False
        self.begin_rot_angle = 0.0        

    def collide_point(self, x, y):
        return Vector(self.pos).distance((x, y)) <= self.radius

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            return True
    
    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            #self.rotation += self.angle
            #print self.rotation
            self.begin_rotation = False
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.C = (x, y)
            self.calculate_angle()
            if self.begin_rotation == False:
                self.begin_rot_angle = self.angle
                self.begin_rotation = True
            print self.begin_rot_angle-self.angle
            self.rotation += self.begin_rot_angle-self.angle
            return True
            
    def calculate_angle(self):
        c = sqrt((self.B[0]-self.A[0])**2+(self.B[1]-self.A[1])**2)
        a = sqrt((self.C[0]-self.B[0])**2+(self.C[1]-self.B[1])**2)
        b = sqrt((self.A[0]-self.C[0])**2+(self.A[1]-self.C[1])**2)
        self.angle = degrees(acos((b**2+c**2-a**2)/(2*b*c)))
        
        vector = self.C[0]-self.A[0],self.C[1]-self.A[1]

        if (vector[1] < 0):
            self.angle = 360 - self.angle

        
    def draw(self):
        # Background
        set_color((1,1,1,1))
        drawCSSRectangle(pos=(self.pos[0]-self.radius,self.pos[1]-self.radius), size=(self.radius*2,self.radius*2), style=self.style)
        set_color(*self.style.get('bg-color'))
        with gx_matrix:
            glTranslated(self.pos[0],self.pos[1], 0)
            glRotatef(self.rotation, 0, 0, 1)
            glTranslated(-self.pos[0],-self.pos[1], 0)
            drawCircle(self.pos, self.radius)
            drawCSSRectangle(pos=self.pos, size=(40,40), style=self.style)

            

