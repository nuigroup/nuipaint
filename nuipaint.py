from __future__ import with_statement
from pymt import *

from core import *

if __name__ == '__main__':
    w = MTWindow()
    #Canvas
    cv = Canvas(pos=(w.width/2,w.height/2))
    w.add_widget(cv)    
    #File Browser
    fb = MTFileBrowser(pos=(100,500),size=(400,300))
    w.add_widget(fb)
    #Bottom Toolbar
    tb = toolbar(win=w,canvas=cv)
    w.add_widget(tb)
    #Top Toolbar
    topb = topBar(win=w,canvas=cv,filebrowser=fb)
    w.add_widget(topb)
    #Side Ciruclar Menu
    #kt = MTKinetic(velstop=5.0)
    cm = MTCircularMenu(pos=(300,300),radius=150)
    w.add_widget(cm)
    #w.add_widget(kt)
    runTouchApp()
  