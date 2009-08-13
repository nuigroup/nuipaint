from pymt import *
import pyglet
from filters import *
from pyglet.gl import *
from pyglet import clock

class Canvas(MTWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.img = pyglet.image.load("puppy.jpg")
        self.sprite = pyglet.sprite.Sprite(self.img)
        self.size = (self.img.width, self.img.height)
        self.fbo = Fbo(size=self.size, with_depthbuffer=False)
        self.need_redraw = True
        self.tex = self.img.get_texture()
        self.filter = Filter()
        self.label = MTLabel(pos=self.pos,label=kwargs.get('label'),color=(1,0,0,1),font_size=12,bold=True)
        #self.add_widget(self.label)
        
    def set_image(self):
        self.tex = self.img.get_texture()
        with self.fbo:
            set_color(1, 1, 1)
            drawTexturedRectangle(texture=self.tex, size=self.size)

    def draw(self):
        if self.need_redraw:
            self.set_image()
            self.need_redraw = False
        set_color(1, 1, 1)
        drawTexturedRectangle(pos=self.pos, texture=self.fbo.texture, size=self.size)
        with gx_matrix:
            glTranslated(self.x,self.y,0)
            self.label.draw()
            
    
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


def init_example(m, *largs):
    grid = MTGridLayout(rows=2, cols= 4, uniform_width=True,uniform_height=True,spacing=10)
    m.add_widget(grid)

    c1 = Canvas(label="Original Image")
    grid.add_widget(c1)
    c1.applyFilter("none",1.0)

    c2 = Canvas(label="50% Blur")
    grid.add_widget(c2)
    c2.applyFilter("blur",2.50)

    c3 = Canvas(label="25% Sharp")
    grid.add_widget(c3)
    c3.applyFilter("sharp",1.25)

    c4 = Canvas(label="75% Saturation ")
    grid.add_widget(c4)
    c4.applyFilter("saturation",1.5)

    c5 = Canvas(label="Black & White")
    grid.add_widget(c5)
    c5.applyFilter("bw",1.5)

    c6 = Canvas(label="50% Bright")
    grid.add_widget(c6)
    c6.applyFilter("brightness",1.5)

    c7 = Canvas(label="Sepia")
    grid.add_widget(c7)
    c7.applyFilter("sepia",1.5)

    c8 = Canvas(label="75% Contrast")
    grid.add_widget(c8)
    c8.applyFilter("contrast",1.5)

if __name__ == '__main__':
    m = MTWindow()
    clock.schedule_once(curry(init_example, m), 0)
    runTouchApp()

