from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.app.observer import *

class toolbarHolder(MTGridLayout):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (75,70))
        kwargs.setdefault('rows', 1)
        kwargs.setdefault('cols', 10)
        kwargs.setdefault('spacing', 10)
        kwargs.setdefault('pos', (0,0))
        super(toolbarHolder, self).__init__(**kwargs)        
        self.bgcolor = (0.3,0.3,0.3,1)
        self.border_radius = 8
        self.spacing = kwargs.get('spacing')
        self.size = kwargs.get('size')
        self.pos=kwargs.get('pos') #make this indepeneted of the window size
        
        
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
        self.canvas = Observer.get('canvas')
        self.parent_win = Observer.get('window')
        tb = toolbarHolder(size=(430,70))
        tb.pos = (int(self.parent_win.width/2-tb.width/2),-5)
        brush_icon = MTImageButton(filename='gfx/icons/brush white txt.png')
        #select_icon = MTImageButton(filename='gfx/icons/select white txt.png')
        zoom_icon = MTImageButton(filename='gfx/icons/zoom white txt.png')
        filter_icon = MTImageButton(filename='gfx/icons/filter white txt.png')
        smudge_icon = MTImageButton(filename='gfx/icons/smudge.png')
        #flickr_icon = MTImageButton(filename='gfx/icons/flickr white txt.png')
        eraser_icon = MTImageButton(filename='gfx/icons/eraser.png')
        tb.add_widget(brush_icon)
        #tb.add_widget(select_icon)
        tb.add_widget(zoom_icon)
        tb.add_widget(filter_icon)
        tb.add_widget(smudge_icon)
        tb.add_widget(eraser_icon)
        #tb.add_widget(flickr_icon)
        self.add_widget(tb)
        
        @zoom_icon.event
        def on_press(touch):
            Observer.get('canvas').set_mode("zoom")
            
        @brush_icon.event
        def on_press(touch):
            Observer.get('canvas').set_mode("draw")
            
        @filter_icon.event
        def on_press(touch):
            filterbox = Observer.get('filter_box')
            filterbox.show()
            
        @filter_icon.event
        def on_release(touch):
            filterbox = Observer.get('filter_box')
            filterbox.hide()
            
        @eraser_icon.event
        def on_press(touch):
            Observer.get('canvas').set_mode("erase")

        @smudge_icon.event
        def on_press(touch):
            Observer.get('canvas').set_mode("smudge")
        
        
        
            