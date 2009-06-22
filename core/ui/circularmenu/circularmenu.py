from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import degrees,sqrt,acos,pi,cos,sin


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
            self.rotation += self.angle            
            self.angle = 0.0            
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()
            return True
            
    def calculate_angle(self):
        self.angle = Vector(self.last_touch).angle(self.first_touch)
 
    def on_draw(self):
        #set_color((1,1,1,1))
        #drawCSSRectangle(pos=(self.pos[0]-self.radius,self.pos[1]-self.radius), size=(self.radius*2,self.radius*2), style=self.style)
        with gx_matrix_identity:
            set_color(*self.style.get('bg-color'))
            glTranslated(self.pos[0], self.pos[1], 0)
            glRotatef(self.angle+self.rotation, 0, 0, 1)
            drawCircle((0, 0), self.radius)
            drawTriangle(pos=(0, 0), w=40, h=100)
            for w in self.children:
                with gx_matrix:
                    angle = Vector(w.pos).angle((0,self.radius))
                    glTranslatef(w.x, w.y, 0)
                    glRotatef(angle, 0, 0, 1)
                    glTranslatef(-w.x, -w.y, 0)
                    w.dispatch_event('on_draw')

if __name__ == '__main__':
    w = MTWindow()
    cm = MTCircularMenu(pos=(w.width/2,w.height/2),radius=150)
    w.add_widget(cm)
    for i in range (12):
        teta = float((360/12)*i*(pi/180))
        x =  int(90*cos(teta))
        y =  int(90*sin(teta))
        im = MTImageButton(filename="../../../gfx/icons/flickr.png",pos=(x,y))
        cm.add_widget(im) 

    runTouchApp()

