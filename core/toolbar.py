from __future__ import with_statement
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
        self.canvas = kwargs.get('canvas')
        tb = toolbarHolder(parent_win=kwargs.get('win'))
        color_icon = MTImageButton(filename='gfx/icons/color white txt.png')
        brush_icon = MTImageButton(filename='gfx/icons/brush white txt.png')
        select_icon = MTImageButton(filename='gfx/icons/select white txt.png')
        zoom_icon = MTImageButton(filename='gfx/icons/zoom white txt.png')
        filter_icon = MTImageButton(filename='gfx/icons/filter white txt.png')
        polygon_icon = MTImageButton(filename='gfx/icons/polygon white txt.png')
        flickr_icon = MTImageButton(filename='gfx/icons/flickr white txt.png')
        tb.add_widget(color_icon)
        tb.add_widget(brush_icon)
        tb.add_widget(select_icon)
        tb.add_widget(zoom_icon)
        tb.add_widget(filter_icon)
        tb.add_widget(polygon_icon)
        tb.add_widget(flickr_icon)
        self.add_widget(tb)
        
        @zoom_icon.event
        def on_press(touchID, x, y):
            self.canvas.set_mode("zoom")
            
        @brush_icon.event
        def on_press(touchID, x, y):
            self.canvas.set_mode("draw")
        
            