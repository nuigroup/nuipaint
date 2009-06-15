from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import degrees,sqrt,acos,pi,cos,sin,radians

def drawSemiCircle(pos=(0,0), inner_radius=100,outer_radius=100,slices=32,loops=1,start_angle=0,sweep_angle=0):
    gluPartialDisk(gluNewQuadric(), inner_radius, outer_radius, slices, loops, start_angle,sweep_angle )

class MTCircularScroller(MTWidget): 
    def __init__(self, **kwargs):
        kwargs.setdefault('radius', 200)
        super(MTCircularScroller, self).__init__(**kwargs)
        self.radius = kwargs.get('radius')        
        self.last_touch = (0, 0)
        self.angle = 0.0
        self.rotation = -40.0
        self.radius_line = (int(self.radius*sin(radians(self.rotation))),int(self.radius*cos(radians(self.rotation))))

    def collide_point(self, x, y):
        return Vector(self.pos).distance((x, y)) <= self.radius

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()
            return True
    
    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            pass            
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()
            return True
            
    def calculate_angle(self):
        self.angle = Vector(self.radius_line).angle(self.last_touch)
 
    def on_draw(self):
        with gx_matrix_identity:
            set_color(*self.style.get('bg-color'))
            glTranslated(self.pos[0], self.pos[1], 0)
            glRotatef(-self.rotation, 0, 0, 1)
            drawSemiCircle((0,0),self.radius-32,self.radius,32,1,0,360)
            set_color(1,1,0,0.5)
            drawSemiCircle((0,0),self.radius-24,self.radius-8,32,1,0,(360+self.angle) if self.angle<0 else self.angle)
            drawTriangle(pos=(0, 0), w=40, h=100)


if __name__ == '__main__':
    w = MTWindow()
    cm = MTCircularScroller(pos=(w.width/2,w.height/2),radius=150)
    w.add_widget(cm)

    runTouchApp()


