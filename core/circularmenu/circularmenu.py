from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import degrees,sqrt,acos


class MTCircularMenu(MTWidget): 
    def __init__(self, **kwargs):
        kwargs.setdefault('radius', 200)
        super(MTCircularMenu, self).__init__(**kwargs)
        self.radius = kwargs.get('radius')        
        self.first_touch = (0, 0)
        self.last_touch = (0, 0)
        self.angle = 0.0
        self.rotation = 0.0

    def collide_point(self, x, y):
        return Vector(self.pos).distance((x, y)) <= self.radius

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.first_touch = (x - self.pos[0], y - self.pos[1])
            return True
    
    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            print self.angle
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()
            return True
            
    def calculate_angle(self):
        self.angle = Vector(self.last_touch).angle(self.first_touch)
        #if self.angle < 0:
        #    self.angle = 360 + self.angle
    def draw(self):
        # Background
        set_color((1,1,1,1))
        drawCSSRectangle(pos=(self.pos[0]-self.radius,self.pos[1]-self.radius), size=(self.radius*2,self.radius*2), style=self.style)
        #set_color(*self.style.get('bg-color'))
        #print self.angle
        with gx_matrix:
            set_color(*self.style.get('bg-color'))
            glTranslated(self.pos[0],self.pos[1], 0)
            glRotatef(self.angle, 0, 0, 1)
            glTranslated(-self.pos[0],-self.pos[1], 0)
            drawCircle(self.pos, self.radius)
            drawTriangle(pos=self.pos,w=40,h=50)
            #drawCSSRectangle(pos=self.pos, size=(40,40), style=self.style)

if __name__ == '__main__':
    w = MTWindow()
    cm = MTCircularMenu(pos=(300,300),radius=300)
    w.add_widget(cm)
    runTouchApp()
            

