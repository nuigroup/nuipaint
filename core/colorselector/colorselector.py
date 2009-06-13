from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import sin,cos,radians
       
def drawPartialCircle(pos=(0,0), radius=100):
    with gx_begin(GL_TRIANGLE_FAN):
        glColor3f(0,0,1)
        glVertex2f(pos[0], pos[1])        
        for angle in range (90,195,5):        
            glColor3f(sin(radians(angle-90)),cos(radians(angle-90)),0)
            glVertex2f(pos[0] + int(cos(radians(angle))*radius),pos[1] + int(sin(radians(angle))*radius))  
        

class MTColorSelector(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        super(MTColorSelector, self).__init__(**kwargs)

    def draw(self):
        with gx_matrix_identity:
            set_color(*self.style.get('bg-color'))
            drawPartialCircle(pos=self.pos,radius=250)

if __name__ == '__main__':
    w = MTWindow()
    cm = MTColorSelector(pos=(w.width,0),radius=100)
    w.add_widget(cm)    
    runTouchApp()