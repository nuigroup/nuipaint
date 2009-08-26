from pymt import *
import pyglet
from filters import *

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.img = pyglet.image.load("puppy.jpg")
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
        elif type == "contrast":
            self.fbo.texture = self.filter.contrast(self.tex,self.size,value)
        elif type == "saturation":
            self.fbo.texture = self.filter.saturation(self.tex,self.size,value)
        elif type == "bw":
            self.fbo.texture = self.filter.bw(self.tex,self.size,value)
        elif type == "sepia":
            self.fbo.texture = self.filter.sepia(self.tex,self.size,value)
        elif type == "radialblur":
            self.fbo.texture = self.filter.radialblur(self.tex,self.size,value)


m = MTWindow()
c = Canvas()
m.add_widget(c)

lay = MTGridLayout(rows=8, cols=4)
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

contrast = MTLabel(label="Contrast")
lay.add_widget(contrast)

contrast_slide = MTSlider(min=1.0,max=2.0,orientation="horizontal")
lay.add_widget(contrast_slide)
@contrast_slide.event
def on_value_change(value):
    c.applyFilter("contrast",value)    

saturation = MTLabel(label="Saturation")
lay.add_widget(saturation)

saturation_slide = MTSlider(min=0.0,max=2.0,orientation="horizontal")
lay.add_widget(saturation_slide)
@saturation_slide.event
def on_value_change(value):
    c.applyFilter("saturation",value)     
    
bw = MTLabel(label="Black & White")
lay.add_widget(bw)

bw_slide = MTSlider(min=0.0,max=2.0,orientation="horizontal")
lay.add_widget(bw_slide)
@bw_slide.event
def on_value_change(value):
    c.applyFilter("bw",value) 
    
sepia = MTLabel(label="Sepia")
lay.add_widget(sepia)

sepia_slide = MTSlider(min=0.0,max=2.0,orientation="horizontal")
lay.add_widget(sepia_slide)
@sepia_slide.event
def on_value_change(value):
    c.applyFilter("sepia",value) 

runTouchApp()
