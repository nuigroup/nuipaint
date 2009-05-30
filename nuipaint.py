from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from PIL import Image
from pyglet.image import ImageData
import ImageEnhance


class ImageScatter(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('filename', 'images/photo.jpg')
        if kwargs.get('filename') is None:
            raise Exception('No filename given to MTScatterImage')
        kwargs.setdefault('loader', None)

        super(ImageScatter, self).__init__(**kwargs)

        self.touch_positions = {}

        self.pim = Image.open(kwargs.get('filename'))
        self.contrast_enh = ImageEnhance.Contrast(self.pim)
        self.pim = self.contrast_enh.enhance(1.0)

        self.bright_enh = ImageEnhance.Brightness(self.pim)
        self.pim = self.bright_enh.enhance(1.0)

        self.color_enh = ImageEnhance.Color(self.pim)
        self.pim = self.color_enh.enhance(1.0)

        self.sharp_enh = ImageEnhance.Sharpness(self.pim)
        self.pim = self.sharp_enh.enhance(1.0)

        self.bdata = self.pim.tostring()
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)
        self.image  = pyglet.sprite.Sprite(self.img)
        self.width = self.pim.size[0]
        self.height = self.pim.size[1]


        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
        self.color = (0,1,0,1.0)
        set_brush('brushes/brush_particle.png')
        self.layer_clear()

    def layer_clear(self):
        self.fbo.bind()
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.fbo.release()


    def on_touch_down(self, touches, touchID, x, y):
        global workimage
        if self.collide_point(x,y):
            if touches[touchID].is_double_tap:
                workimage = self
            self.touch_positions[touchID] = (x,y)
            self.fbo.bind()
            glColor4f(0,1,0,1)
            
            #not transformed
            #drawCircle(pos=(x,y), radius=10)
            
            #transformed
            drawCircle(pos=self.to_local(x,y), radius=10)
            
            self.fbo.release()
            super(ImageScatter, self).on_touch_down(touches, touchID, x, y)
            return True

    def draw(self):
        with gx_matrix:
            glColor4f(1,1,1,1)
            drawRectangle((-6,-6),(self.width+12,self.height+12))
            glScaled(float(self.width)/self.image.width, float(self.height)/self.image.height, 2.0)
            self.image.draw()
            with gx_blending:
                drawTexturedRectangle(self.fbo.texture, (-6,-6),(self.width+12,self.height+12))



    def changeContrast(self,value):
        self.pim = self.contrast_enh.enhance(value)
        self.bdata = self.pim.tostring()
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)
        self.image  = pyglet.sprite.Sprite(self.img)

    def changeBrightness(self,value):
        self.pim = self.bright_enh.enhance(value)
        self.bdata = self.pim.tostring()
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)
        self.image  = pyglet.sprite.Sprite(self.img)

    def changeColorize(self,value):
        self.pim = self.color_enh.enhance(value)
        self.bdata = self.pim.tostring()
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)
        self.image  = pyglet.sprite.Sprite(self.img)

    def changeSharpness(self,value):
        self.pim = self.sharp_enh.enhance(value)
        self.bdata = self.pim.tostring()
        self.img = ImageData(self.pim.size[0], self.pim.size[1], 'RGB', self.bdata, pitch=-self.pim.size[0]*3)
        self.image  = pyglet.sprite.Sprite(self.img)

workimage = ImageScatter()

def filter_slider_cb(type, value):
	global workimage
	if type == 'contrast':
		workimage.changeContrast(value)
	elif type == 'brightness':
		workimage.changeBrightness(value)
	elif type == 'colorize':
		workimage.changeColorize(value)
	elif type == 'sharpness':
		workimage.changeSharpness(value)

if __name__ == '__main__':
    w = MTWindow()

    #add the images
    image = ImageScatter()
    w.add_widget(image)
    #image = ImageScatter(filename="photo2.jpg")
    #w.add_widget(image)
    #image = ImageScatter(filename="photo3.jpg")
    #w.add_widget(image)
    workimage = image

    #setup layoyut for the filter sliders and labels
    cplayout = MTGridLayout(rows=4,cols=2,spacing=5)

    kw = {'min': 0, 'max': 5, 'value': 1, 'orientation': 'horizontal'}
    ctlbl = MTFormLabel(label="Contrast")
    cplayout.add_widget(ctlbl)
    sl = MTSlider(**kw)
    sl.push_handlers(on_value_change=curry(filter_slider_cb, 'contrast'))
    cplayout.add_widget(sl)

    ctlb2 = MTFormLabel(label="Brightness")
    cplayout.add_widget(ctlb2)
    s2 = MTSlider(**kw)
    s2.push_handlers(on_value_change=curry(filter_slider_cb, 'brightness'))
    cplayout.add_widget(s2)

    ctlb3 = MTFormLabel(label="Colorize")
    cplayout.add_widget(ctlb3)
    s3 = MTSlider(**kw)
    s3.push_handlers(on_value_change=curry(filter_slider_cb, 'colorize'))
    cplayout.add_widget(s3)

    ctlb4 = MTFormLabel(label="Sharpness")
    cplayout.add_widget(ctlb4)
    s4 = MTSlider(**kw)
    s4.push_handlers(on_value_change=curry(filter_slider_cb, 'sharpness'))
    cplayout.add_widget(s4)

    #setup filter icon and the menu system
    filterBut = MTImageButton(filename="gfx/icons/filters.jpg")
    filterBut.x,filterBut.y = int(w.width/2-filterBut.width/2),0
    w.add_widget(filterBut)

    menuholder = MTRectangularWidget(bgcolor=(0,0,0))
    menuholder.width = cplayout._get_content_width()
    menuholder.height = cplayout._get_content_height()
    menuholder.x=filterBut.x-int(menuholder.width/2-filterBut.width/2)
    menuholder.y=filterBut.y+filterBut.height
    cplayout.pos = menuholder.pos
    menuholder.add_widget(cplayout)

    w.add_widget(menuholder)
    menuholder.hide()



    @filterBut.event
    def on_press(touchID, x, y):
        menuholder.show()
        menuholder.bring_to_front()

    @filterBut.event
    def on_release(touchID, x, y):
        menuholder.hide()

    #exitbut = MTImageButton(filename="icons/stop.png")
    #exitbut.x = int(w.width-exitbut.width)
    #exitbut.y = int(w.height-exitbut.height)
    #w.add_widget(exitbut)
    #@exitbut.event
    #def on_press(touchID, x, y):
    #    sys.exit()




    runTouchApp()
