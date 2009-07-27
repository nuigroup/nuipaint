from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.ui.toolbar import toolbarHolder

class windowBar(MTWidget):
    def __init__(self, **kwargs):
        super(windowBar, self).__init__(**kwargs)
        self.canvas = kwargs.get('canvas')
        self.filebrowser = kwargs.get('filebrowser')
        self.handler = kwargs.get('handler')
        tb = toolbarHolder(size=(20,44),spacing=10)
        color = MTImageButton(filename='gfx/icons/color.png')
        tb.add_widget(color)
        brush = MTImageButton(filename='gfx/icons/brush.png')
        tb.add_widget(brush)
        save = MTImageButton(filename='gfx/icons/filesave_tiny.png')
        tb.add_widget(save)
        self.add_widget(tb)
        tb.size = (tb._get_content_width()-65,tb.height)
        tb.pos = (int(self.handler.size[0]/2-tb.size[0]/2), -5)
        

        @brush.event
        def on_press(touch):
            self.canvas.set_mode("draw")