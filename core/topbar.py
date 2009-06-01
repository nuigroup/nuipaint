from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from core.toolbar import toolbarHolder
from core.iconbutton import MTIconButton

class topBar(MTWidget):
    def __init__(self, **kwargs):
        super(topBar, self).__init__(**kwargs)
        self.parent_win = kwargs.get('win')
        self.filebrowser = kwargs.get('filebrowser')
        tb = toolbarHolder(size=(100,70),spacing=10)
        tb.pos = (0, self.parent_win.height-tb.height+5)
        save_icon = MTIconButton(icon_file='gfx/icons/filesave.png',label="Save")
        tb.add_widget(save_icon)
        open_icon = MTIconButton(icon_file='gfx/icons/fileopen.png',label="Open")
        tb.add_widget(open_icon)
        undo_icon = MTIconButton(icon_file='gfx/icons/undo.png',label="Undo")
        tb.add_widget(undo_icon)
        redo_icon = MTIconButton(icon_file='gfx/icons/redo.png',label="Redo")
        tb.add_widget(redo_icon)
        fullscreen_icon = MTIconButton(icon_file='gfx/icons/fullscreen.png',label="FullMode")
        tb.add_widget(fullscreen_icon)
        self.add_widget(tb)
        tb.size = (tb._get_content_width()-45,tb.height)
        
        @open_icon.event
        def on_press(touchID, x, y):
            self.filebrowser.show()
        