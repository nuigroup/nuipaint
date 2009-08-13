from pymt import *
from pyglet.gl import *

class AlphaWindow(MTWidget):
    def __init__(self, **kwargs):
        super(AlphaWindow, self).__init__(**kwargs)
        self.tsize = (64, 64)
        self.fbo1 = Fbo(size=self.tsize)
        self.fbo2 = Fbo(size=self.tsize)
        self.need_redraw = True

    def draw(self):
        if self.need_redraw:
            with self.fbo1:
                set_color(0, 0, 0, 0)
                drawRectangle(size=self.tsize)
                set_color(0, 0, 1)
                drawLine((10, 10 , 40, 40), width=8)
            with self.fbo2:
                set_color(0, 0, 0, 0)
                drawRectangle(size=self.tsize)
                set_color(0, 1, 0)
                drawLine((10, 40 , 40, 10), width=8)
                set_color(0, 0, 0)
                drawLine((10, 24 , 40, 24), width=8)
            self.need_redraw = False

        alpha = (GL_ZERO, GL_ONE, GL_DST_COLOR, GL_ONE_MINUS_DST_COLOR,
                 GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
                 GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR)
        for x in xrange(len(alpha)):
            for y in xrange(len(alpha)):
                pos = x * 64, y * 64
                set_color(1, 1, 1)
                drawTexturedRectangle(
                    texture=self.fbo1.texture, pos=pos, size=self.tsize)
                set_color(1, 1, 1, 0.99, sfactor=alpha[x], dfactor=alpha[y])
                drawTexturedRectangle(
                    texture=self.fbo2.texture, pos=pos, size=self.tsize)

m = MTWindow()
m.add_widget(AlphaWindow())
runTouchApp()
