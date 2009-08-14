from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.ui.toolbar import toolbarHolder
from core.ui.iconbutton import MTIconButton
from core.app.observer import *

class topBar(MTWidget):
    def __init__(self, **kwargs):
        super(topBar, self).__init__(**kwargs)
        self.parent_win = Observer.get('window')
        self.filebrowser = Observer.get('file_browser')
        self.clipboard = Observer.get('clipboard')
        self.handler = Observer.get('inner_window_handler')
        self.canvas = Observer.get('canvas')
        tb = toolbarHolder(size=(100,70),spacing=10)
        tb.pos = (0, self.parent_win.height-tb.height+5)
        save_icon = MTIconButton(icon_file='gfx/icons/filesave.png',label="Save")
        tb.add_widget(save_icon)
        open_icon = MTIconButton(icon_file='gfx/icons/fileopen.png',label="Open")
        tb.add_widget(open_icon)
        #undo_icon = MTIconButton(icon_file='gfx/icons/undo.png',label="Undo")
        #tb.add_widget(undo_icon)
        #redo_icon = MTIconButton(icon_file='gfx/icons/redo.png',label="Redo")
        #tb.add_widget(redo_icon)
        cut_icon = MTIconButton(icon_file='gfx/icons/cut.png',label="Cut")
        tb.add_widget(cut_icon)
        copy_icon = MTIconButton(icon_file='gfx/icons/copy.png',label="Copy")
        tb.add_widget(copy_icon)
        paste_icon = MTIconButton(icon_file='gfx/icons/paste.png',label="Paste")
        tb.add_widget(paste_icon)
        fullscreen_icon = MTIconButton(icon_file='gfx/icons/unfullscreen.png',label="MiniMode")
        tb.add_widget(fullscreen_icon)
        self.add_widget(tb)
        tb.size = (tb._get_content_width()-45,tb.height)
        
        @open_icon.event
        def on_press(touch):
            self.filebrowser.show()
        
        @fullscreen_icon.event
        def on_press(touch):
            self.handler.unfullscreen()
            
        @copy_icon.event
        def on_press(touch):
            tex = self.canvas.get_fbo_texture()
            self.clipboard.set_data(tex)
            
        @paste_icon.event
        def on_press(touch):
            print self.clipboard.get_data()
            