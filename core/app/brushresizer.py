from __future__ import with_statement
from pymt import *
from pyglet.gl import *


class MTBrushResizer(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('canvas', None)    
        super(MTBrushResizer, self).__init__(**kwargs)
        self.canvas = kwargs.get('canvas')
        self.bound  = MTStencilContainer(size=self.size)
        self.add_widget(self.bound)
        self.brush_image = MTScatterImage(filename="brushes/brush_particle.png",do_translation=False,do_rotation=False,scale_min=0.1)
        self.bound.add_widget(self.brush_image)
        self.current_brush = "brushes/brush_particle.png"
        self.current_brush_size = 64

    
    def set_brush(self,brush_image,brush_size):
        self.bound.remove_widget(self.brush_image)
        self.brush_image = MTScatterImage(filename=brush_image,do_translation=False,do_rotation=False,scale_min=0.1)
        self.current_brush = brush_image
        self.bound.add_widget(self.brush_image)
        self.canvas.set_brush(sprite=brush_image,size=brush_size)
        
    def on_touch_down(self,touch):
        if self.collide_point(touch.x,touch.y):
            brush_scale = self.brush_image.get_scale_factor()
            self.current_brush_size = self.current_brush_size * brush_scale
            if self.current_brush_size > 200 :
                self.current_brush_size = 200
            elif self.current_brush_size < 10:
                self.current_brush_size = 10
            self.canvas.set_brush(sprite=self.current_brush,size=self.current_brush_size)
            super(MTBrushResizer, self).on_touch_down(touch)