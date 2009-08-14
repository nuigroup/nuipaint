from pymt import *
from pyglet.gl import *

class AlphaWindow(MTWidget):
    def __init__(self, **kwargs):
        super(AlphaWindow, self).__init__(**kwargs)
        self.tsize = (64, 64)
        self.fbo1 = Fbo(size=self.tsize)
        self.fbo2 = Fbo(size=self.tsize)
        self.fbo3 = Fbo(size=self.tsize)
        self.need_redraw = True
        self.s, self.d = 0, 0

    def on_touch_down(self, touch):
        self.s = int(touch.x / 64)
        self.d = int(touch.y / 64)

    def on_touch_move(self, touch):
        self.s = int(touch.x / 64)
        self.d = int(touch.y / 64)

    def draw(self):
        if self.need_redraw:
            with self.fbo1:
                set_color(1, 0, 0, .5)
                drawRectangle(size=self.tsize)
                set_color(0, 0, 1)
                drawLine((10, 10 , 54, 54), width=8)
            with self.fbo2:
                set_color(1, 1, 1)
                drawRectangle(size=(32, 64))
                set_color(0, 0, 0)
                drawRectangle(pos=(32, 0), size=(32, 64))
                set_color(0.5, 0.5, 0.5)
                drawRectangle(pos=(28, 0), size=(8, 64))
            with self.fbo3:
                set_color(1, 1, 1, .1)
                drawRectangle(size=self.tsize)
                set_color(0, 1, 0)
                drawLine((10, 54, 54, 10), width=8)
                set_color(0, 0, 0)
                drawLine((10, 32 , 54, 32), width=8)
            self.need_redraw = False

        alphasrc = (GL_ZERO, GL_ONE,
                 GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
                 GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA,
                 GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR,
                 GL_SRC_ALPHA_SATURATE)
        alphadst = (GL_ZERO, GL_ONE,
                 GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
                 GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA,
                 GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR)

        self.d = min(self.d, len(alphadst)-1)
        self.s = min(self.s, len(alphasrc)-1)
        for x in xrange(len(alphasrc)):
            for y in xrange(len(alphadst)):
                pos = x * 64, y * 64
                set_color(1, 1, 1)
                drawTexturedRectangle(
                    texture=self.fbo1.texture, pos=pos, size=self.tsize)
                set_color(1, 1, 1, 0.999, sfactor=alphasrc[self.s],
                          dfactor=alphadst[self.d])
                #set_color(1, 1, 1, 0.999, sfactor=GL_DST_COLOR, dfactor=GL_ZERO)
                drawTexturedRectangle(
                    texture=self.fbo2.texture, pos=pos, size=self.tsize)
                set_color(1, 1, 1, 0.999, sfactor=alphasrc[x], dfactor=alphadst[y])
                drawTexturedRectangle(
                    texture=self.fbo3.texture, pos=pos, size=self.tsize)

m = MTWindow()
m.add_widget(AlphaWindow())
runTouchApp()
