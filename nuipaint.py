from __future__ import with_statement
from pymt import *

from core import *

if __name__ == '__main__':
    w = MTWindow()
    cv = Canvas(pos=(w.width/2,w.height/2))
    w.add_widget(cv)    
    tb = toolbar(win=w,canvas=cv)
    w.add_widget(tb)
    topb = topBar(win=w,canvas=cv)
    w.add_widget(topb)
    kiney = MTFileBrowser(pos=(100,100),size=(400,200))
    w.add_widget(kiney)
    runTouchApp()