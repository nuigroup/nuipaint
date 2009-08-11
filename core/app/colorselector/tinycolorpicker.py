from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from numpy import *

class MTTinyColorPicker(MTWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('canvas', None)    
        super(MTTinyColorPicker, self).__init__(**kwargs)
        self.bg  = os.path.join(os.path.dirname(__file__),"colorcircle.png")
        self.img = pyglet.image.load(self.bg)
        self.sprite = pyglet.sprite.Sprite(self.img)
        self.color = (0,0,0,1)
        self.register_event_type('on_color_change')
        self.size = (self.img.width,self.img.height)

    def draw(self):
        with gx_matrix:
            glTranslated(self.pos[0],self.pos[1],0)
            self.sprite.draw()
            
    def to_local(self,x,y):
        return((int(x-self.pos[0]),int(y-self.pos[1])))
            
    def on_color_change(self, color):
        pass
            
    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y):
            dx,dy = self.to_local(touch.x,touch.y)
            temp = self.pick_color(dx,dy)
            self.color = (float(temp[0]/255.0),float(temp[1]/255.0),float(temp[2]/255.0),1)
            self.dispatch_event('on_color_change', self.color)
            return True
            
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            dx,dy = self.to_local(touch.x,touch.y)
            temp = self.pick_color(dx,dy)
            self.color = (float(temp[0]/255.0),float(temp[1]/255.0),float(temp[2]/255.0),1)
            self.dispatch_event('on_color_change', self.color)
            return True
    
    def pick_color(self,x,y):
        region = self.img.texture.get_region(int(x), int(y), 1, 1)
        data = region.get_image_data()
        format = 'RGB'
        pitch = 1 * len(format)       
        pixel_data = data.get_data(format, pitch)
        pixel = map(ord, list(pixel_data))
        return (pixel[0],pixel[1],pixel[2])