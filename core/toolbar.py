from pymt import *
from pyglet.gl import *

class toolbar(MTGridLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault('width', 500)
        kwargs.setdefault('height', 70)
        kwargs.setdefault('rows', 1)
        kwargs.setdefault('cols', 10)
        kwargs.setdefault('spacing', 10)
        super(toolbar, self).__init__(**kwargs)
        self.bgcolor = (0.3,0.3,0.3,1)
        self.border_radius = 8
        self.size = (self.width,self.height)
        self.pos=(int(1440/2-self.width/2),-5) #make this indepeneted of the window size
        
    def draw(self):
        #x, y, w, h = self.x, self.y, self.width, self.height
        #print "x:",self.x
        set_color(*self.bgcolor)
        with gx_matrix:
            glTranslatef(self.pos[0], self.pos[1], 0)
            drawRoundedRectangle(size=self.size, radius=self.border_radius)
            drawRoundedRectangle(size=self.size, radius=self.border_radius, style=GL_LINE_LOOP)
            drawRoundedRectangleAlpha(size=self.size, radius=self.border_radius, alpha=(1,1,.5,.5))

            