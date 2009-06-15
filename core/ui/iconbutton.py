from __future__ import with_statement
from pymt import *
from pyglet.gl import *

class MTIconButton(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        super(MTIconButton, self).__init__(**kwargs)
        self.icon_file = kwargs.get('icon_file')
        self.label_txt = kwargs.get('label')
        self.size           = (60, 50)                
        img            = pyglet.image.load(self.icon_file)
        self.image     = pyglet.sprite.Sprite(img)
        self.image.x        = self.x
        self.image.y        = self.y
        self.scale          = kwargs.get('scale')
        self.image.scale    = self.scale
        self.labelWX = MTLabel(label=str(self.label_txt)[:15],anchor_x="center",anchor_y="center",halign="center")
        self.add_widget(self.labelWX)
        self.y = self.y + 5

    def draw(self):
        self.image.x        = self.x
        self.image.y        = self.y+5
        self.image.scale    = self.scale
        self.image.draw()
        self.labelWX.pos = (int(self.x+22),int(self.y+2))