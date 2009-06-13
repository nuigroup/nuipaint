from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import sin,cos,radians

       
def drawPartialCircle(pos=(0,0), radius=100):
    with gx_begin(GL_TRIANGLE_FAN):
        glColor3f(0,0,1)
        glVertex2f(0,0)        
        for angle in range (90,195,5):        
            glColor3f(sin(radians(angle-90)),cos(radians(angle-90)),0)
            glVertex2f(int(cos(radians(angle))*radius),int(sin(radians(angle))*radius))  
            
        

class MTColorSelector(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        kwargs.setdefault('canvas', None)
        super(MTColorSelector, self).__init__(**kwargs)
        self.parent_win = kwargs.get('win')
        self.canvas = kwargs.get('canvas')
        self.point_angle = 0.0
        self.point_distance = 0.0
        self.back_color = (0.0,0.0,0.0)
        
    def collide_point(self, x, y):
        return Vector((self.pos[0]+self.width,0)).distance((x, y)) <= self.size[0]

    def draw(self):
        set_color(*self.back_color)
        drawCSSRectangle(pos=self.pos, size=self.size, style=self.style)
        with gx_matrix_identity:
            glTranslated(self.pos[0]+self.size[0], self.pos[1], 0)
            set_color(*self.style.get('bg-color'))
            drawPartialCircle(pos=self.pos,radius=200)

    
    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y):
            self.point_angle = Vector((0,self.height)).angle((self.parent_win.width-x,y))
            self.point_distance = Vector((self.pos[0]+self.width,0)).distance((x, y))
            self.calculate_color()
            return True
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            self.point_angle = Vector((0,self.height)).angle((self.parent_win.width-x,y))
            self.point_distance = Vector((self.pos[0]+self.width,0)).distance((x, y))
            self.calculate_color()
            
    def calculate_color(self):
        #print self.point_angle
        #print "r,g,b:",sin(radians(self.point_angle)),cos(radians(self.point_angle)),1-self.point_distance/self.size[0]
        self.back_color = (sin(radians(self.point_angle)),cos(radians(self.point_angle)),1-self.point_distance/self.size[0])
        if(self.canvas):
            self.canvas.set_brush_color((sin(radians(self.point_angle)),cos(radians(self.point_angle)),1-self.point_distance/self.size[0]))
        

if __name__ == '__main__':
    w = MTWindow()
    cm = MTColorSelector(pos=(w.width-200,0),size=(200,200),win=w)
    w.add_widget(cm)    
    runTouchApp()