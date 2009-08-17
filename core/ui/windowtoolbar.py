from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.app.colorselector.tinycolorpicker import MTTinyColorPicker
from core.app.observer import *

class windowBar(MTWidget):
    def __init__(self, **kwargs):
        super(windowBar, self).__init__(**kwargs)
        self.canvas = Observer.get('canvas')
        self.handler = Observer.get("inner_window_handler")
        self.tb = MTBoxLayout(spacing=5)
        self.add_widget(self.tb)
        color = MTImageButton(filename='gfx/icons/color.png')
        self.tb.add_widget(color)
        brush = MTImageButton(filename='gfx/icons/brush.png')
        self.tb.add_widget(brush)
        save = MTImageButton(filename='gfx/icons/filesave_tiny.png')
        self.tb.add_widget(save)
        self.size = (self.tb.size[0]+40,self.tb.size[1]+25)
        self.pos = (int(self.handler.size[0]/2-(self.tb.size[0]+40)/2), -10)
        self.tb.pos = (int(self.handler.size[0]/2-self.tb.size[0]/2), 10)
        
        self.tinycolor = MTTinyColorPicker(pos=(color.pos[0]-45,color.pos[1]+35))
        self.add_widget(self.tinycolor)
        self.tinycolor.hide()
        
        @brush.event
        def on_press(touch):
            self.canvas.set_mode("draw")
        
        @color.event
        def on_press(touch):
            self.tinycolor.show()
            
        @color.event
        def on_release(touch):
            self.tinycolor.hide()
            
        @save.event
        def on_press(touch):
            self.canvas.save_image()
            
        @self.tinycolor.event
        def on_color_change(color):
            self.canvas.set_brush_color((color[0],color[1],color[2]))
        
    def draw(self):
        set_color(0.3,0.3,0.3,1.0)
        drawCSSRectangle(size=self.size,pos=self.pos,style={'border-radius': 10,'border-radius-precision': .1})
        self.tb.dispatch_event('on_draw')