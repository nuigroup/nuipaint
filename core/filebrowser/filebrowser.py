from __future__ import with_statement
from pymt import *
from pyglet.gl import *
import os, sys, random
from pyglet.text import Label

class KineticBrowseLayout(MTKineticList):
    def __init__(self, **kwargs):
        super(KineticBrowseLayout, self).__init__(**kwargs)
        
    def draw(self):
        set_color(*self.bgcolor)
        drawRectangle(self.pos, self.size)  #background
        super(MTKineticList, self).on_draw()
        #drawRectangle((self.x, self.height + self.y - 40), (self.width, 40))  #Title Bar
        #self.title.draw()
        for w in self.widgets:
            w.on_draw()
            
class MTIconObject(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        super(MTIconObject, self).__init__(**kwargs)
        self.filename = kwargs.get('filename')
        self.label_txt = kwargs.get('label')
        self.type_image = None
        if os.path.isdir(self.filename):
            self.type_image = 'core/filebrowser/icons/folder.png'
        else:
            ext = self.label_txt.split('.')[-1]
            if ext in ['jpg', 'jpeg']:
                self.type_image = 'core/filebrowser/icons/image-jpeg.png'
            elif ext in ['svg']:
                self.type_image = 'core/filebrowser/icons/image-svg.png'
            elif ext in ['png']:
                self.type_image = 'core/filebrowser/icons/image-png.png'
            elif ext in ['bmp']:
                self.type_image = 'core/filebrowser/icons/image-bmp.png'
            elif ext in ['gif']:
                self.type_image = 'core/filebrowser/icons/image-gif.png'
            elif ext in ['mpg', 'mpeg', 'avi', 'mkv', 'flv']:
                self.type_image = 'core/filebrowser/icons/video.png'
            else:
                self.type_image = 'core/filebrowser/icons/unknown.png'
        self.size           = (80, 80)                
        img            = pyglet.image.load(self.type_image)
        self.image     = pyglet.sprite.Sprite(img)
        self.image.x        = self.x
        self.image.y        = self.y
        self.scale          = kwargs.get('scale')
        self.image.scale    = self.scale
        self.labelWX = MTLabel(label=str(self.label_txt)[:15],anchor_x="center",anchor_y="center",halign="center")
        self.add_widget(self.labelWX)

    def draw(self):
        self.image.x        = self.x
        self.image.y        = self.y
        self.image.scale    = self.scale
        self.image.draw()
        self.labelWX.pos = (int(self.x+20),int(self.y-5))

            
class MTFileEntry(MTIconObject, MTKineticObject):
    def __init__(self, **kwargs):
        self.filename   = kwargs.get('filename')
        self.browser    = kwargs.get('browser')
        super(MTFileEntry, self).__init__(**kwargs)
        
    def on_press(self, touches, touchID, x, y):
        if os.path.isdir(self.filename):
            self.browser.set_path(self.filename)
        if self.db.visible and self.db.on_touch_down(touches, touchID, x, y):
            return True
            
class MTFileBrowser(MTWidget):
    def __init__(self, **kwargs):
        super(MTFileBrowser, self).__init__(**kwargs)
        self.kb = KineticBrowseLayout(pos=self.pos, size=self.size, w_limit=4, deletable=False, searchable=False)
        self.add_widget(self.kb)
        self.dl = GlDisplayList()
        self.path = '.'
        self.close_button = MTImageButton(filename="core/filebrowser/close.png")
        @self.close_button.event
        def on_press(touchID, x, y):
            self.hide()
        self.add_widget(self.close_button)
    
    def update_listing(self):
        self.path = os.path.abspath(self.path)
        for name in os.listdir(self.path):
            filename = os.path.join(self.path, name)
            self.kb.add(MTFileEntry(label=name,filename=filename, browser=self))
        self.kb.add(MTFileEntry(label='..',filename=os.path.join(self.path, '../'), browser=self))
            
    def set_path(self, path):
        self.path = path
        self.remove_widget(self.kb)
        self.kb = None
        self.kb = KineticBrowseLayout(pos=self.pos, size=self.size, w_limit=4, deletable=False, searchable=False)
        self.add_widget(self.kb)
        self.dl.clear()

    
    def draw(self):
        if not self.dl.is_compiled():
            self.update_listing()
            with DO(self.dl, gx_blending):
                self.close_button.pos = (self.x+self.width-5,self.y+self.height-2)
                set_color(0.8, 0.8, 0.8, 1)
                drawRoundedRectangle(pos=(self.x-10,self.y-10),size=(self.width+20,self.height+20), radius=10)                
                set_color(1, 1, 1, 1)
                drawRectangle(self.pos,self.size)
                for w in self.children:
                    w.dispatch_event('on_draw')
        self.dl.draw()


