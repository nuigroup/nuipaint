from __future__ import with_statement
from pymt import *

from core import *

if __name__ == '__main__':
    w = MTWindow()
    cv = Canvas(pos=(w.width/2,w.height/2))
    w.add_widget(cv)    
    fb = MTFileBrowser(pos=(100,w.height-400),size=(350,250))
    w.add_widget(fb)
    tb = toolbar(win=w,canvas=cv)
    w.add_widget(tb)
    topb = topBar(win=w,canvas=cv,filebrowser=fb)
    w.add_widget(topb)
    runTouchApp()