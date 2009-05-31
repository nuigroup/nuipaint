from pymt import *
from pyglet.gl import *

class toolbarHolder(MTGridLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault('width', 500)
        kwargs.setdefault('height', 70)
        kwargs.setdefault('rows', 1)
        kwargs.setdefault('cols', 10)
        kwargs.setdefault('spacing', 10)
        super(toolbarHolder, self).__init__(**kwargs)
        self.bgcolor = (0.3,0.3,0.3,1)
        self.border_radius = 8
        self.size = (self.width,self.height)
        self.parent_win = kwargs.get('parent_win')
        self.pos=(int(self.parent_win.width/2-self.width/2),-5) #make this indepeneted of the window size
        
    def draw(self):
        set_color(*self.bgcolor)
        with gx_matrix:
            glTranslatef(self.pos[0], self.pos[1], 0)
            drawRoundedRectangle(size=self.size, radius=self.border_radius)
            drawRoundedRectangle(size=self.size, radius=self.border_radius, style=GL_LINE_LOOP)
            drawRoundedRectangleAlpha(size=self.size, radius=self.border_radius, alpha=(1,1,.5,.5))
            
 
class toolbar(MTWidget):
    def __init__(self, **kwargs):
        super(toolbar, self).__init__(**kwargs)
        tb = toolbarHolder(parent_win=kwargs.get('win'))
        icon1 = MTImageButton(filename='gfx/icons/color white txt.png')
        icon2 = MTImageButton(filename='gfx/icons/brush white txt.png')
        icon3 = MTImageButton(filename='gfx/icons/select white txt.png')
        icon4 = MTImageButton(filename='gfx/icons/zoom white txt.png')
        icon5 = MTImageButton(filename='gfx/icons/filter white txt.png')
        icon6 = MTImageButton(filename='gfx/icons/polygon white txt.png')
        icon7 = MTImageButton(filename='gfx/icons/flickr white txt.png')
        tb.add_widget(icon1)
        tb.add_widget(icon2)
        tb.add_widget(icon3)
        tb.add_widget(icon4)
        tb.add_widget(icon5)
        tb.add_widget(icon6)
        tb.add_widget(icon7)
        self.add_widget(tb)
            