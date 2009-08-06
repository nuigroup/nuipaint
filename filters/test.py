from pymt import *
import pyglet
from filters import *

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.img = pyglet.image.load("death.jpg")
        self.sprite = pyglet.sprite.Sprite(self.img)
        self.size = (self.img.width, self.img.height)
        self.fbo = Fbo(size=self.size, with_depthbuffer=False)
        self.need_redraw = True
        self.tex = self.img.get_texture()
        self.filter = Filter()
        
    def set_image(self):
        with self.fbo:
            set_color(1, 1, 1)
            drawTexturedRectangle(texture=self.tex, size=self.size)

    def draw(self):
        if self.need_redraw:
            self.set_image()
            self.need_redraw = False
        set_color(1, 1, 1)
        drawTexturedRectangle(texture=self.fbo.texture, size=self.size)
    
    def applyFilter(self,type,value):
        if type == "blur":
            self.fbo.texture = self.filter.blur(self.tex,self.size,value)
        elif type == "sharp":
            self.fbo.texture = self.filter.sharpen(self.tex,self.size,value)
        elif type == "brightness":
            self.fbo.texture = self.filter.brightness(self.tex,self.size,value)


m = MTWindow()
c = Canvas()
m.add_widget(c)

lay = MTGridLayout(rows=3, cols=2)
m.add_widget(lay)

blur = MTLabel(label="Blur")
lay.add_widget(blur)

blur_slide = MTSlider(min=0.0,max=5.0,orientation="horizontal")
lay.add_widget(blur_slide)
@blur_slide.event
def on_value_change(value):
    c.applyFilter("blur",value)

sharp = MTLabel(label="Sharp")
lay.add_widget(sharp)

sharp_slide = MTSlider(min=0.0,max=5.0,orientation="horizontal")
lay.add_widget(sharp_slide)
@sharp_slide.event
def on_value_change(value):
    c.applyFilter("sharp",value)    
    
brightness = MTLabel(label="Brightness")
lay.add_widget(brightness)

brightness_slide = MTSlider(min=0.0,max=2.0,orientation="horizontal")
lay.add_widget(brightness_slide)
@brightness_slide.event
def on_value_change(value):
    c.applyFilter("brightness",value)    
    

runTouchApp()
