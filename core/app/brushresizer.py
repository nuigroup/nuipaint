from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.app.observer import *


class MTBrushResizer(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('canvas', None)    
        super(MTBrushResizer, self).__init__(**kwargs)
        self.canvas = Observer.get('canvas')
        self.bound  = MTStencilContainer(size=self.size,pos=self.pos)
        self.add_widget(self.bound)
        self.brush_image = MTScatterImage(pos=self.pos,filename="brushes/brush_particle.png",do_translation=False,do_rotation=False,scale_min=0.1)
        self.bound.add_widget(self.brush_image)
        self.current_brush = "brushes/brush_particle.png"
        self.original_brush_size = 64
        self.current_brush_size = 64
        
    def on_touch_down(self,touch):        
        if self.collide_point(touch.x,touch.y):
            touch.grab(self)
            self.brush_image.on_touch_down(touch)
            return True
            
    def on_touch_move(self,touch):        
        if self.collide_point(touch.x,touch.y) and touch.grab_current == self:
            self.brush_image.on_touch_move(touch)
            self.brush_image.do_translation = True
            self.brush_image.center = (self.bound.width/2,self.bound.height/2)
            self.brush_image.do_translation = False
            brush_scale = self.brush_image.get_scale_factor()
            self.current_brush_size = int(self.original_brush_size * brush_scale)
            Observer.get('canvas').set_brush(sprite=self.current_brush,size=self.current_brush_size)
            return True
        
    def set_brush(self,brush_image,brush_size):
        self.bound.remove_widget(self.brush_image)
        self.brush_image = MTScatterImage(filename=brush_image,do_translation=False,do_rotation=False,scale_min=0.1)
        self.current_brush = brush_image
        self.bound.add_widget(self.brush_image)
        Observer.get('canvas').set_brush(sprite=brush_image,size=brush_size)
        self.current_brush_size = self.original_brush_size
        Observer.register('current_brush_size',self.current_brush_size)
        
        
        
    
            
     