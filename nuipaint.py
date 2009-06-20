from __future__ import with_statement
from math import cos,sin,pi
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
    fb.hide()
    #Bottom Toolbar
    tb = toolbar(win=w,canvas=cv)
    w.add_widget(tb)
    #Top Toolbar
    topb = topBar(win=w,canvas=cv,filebrowser=fb)
    w.add_widget(topb)
    #Side Ciruclar Menu
    kt = MTKinetic(velstop=5.0)
    cm = MTCircularMenu(pos=(0,0),radius=200)
    kt.add_widget(cm)
    for i in range (18):
        teta = float((360/18)*i*(pi/180))
        x =  int(143*cos(teta))
        y =  int(143*sin(teta))
        im = MTImageButton(filename="gfx/icons/flickr.png",pos=(x,y))
        cm.add_widget(im)
    w.add_widget(kt)
      
    cs = MTColorSelector(pos=(w.width-200,0),size=(200,200),win=w,canvas=cv)
    w.add_widget(cs)
    runTouchApp()
  