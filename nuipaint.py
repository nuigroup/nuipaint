from __future__ import with_statement
from math import cos,sin,pi
from pymt import *

from core import *


if __name__ == '__main__':
    w = MTWindow()
    #Canvas
    cv = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120))
    w.add_widget(cv) 
    #cv.create_layer(pos=(100,100),size=(200,200),color=(1,0,0,0.2))
    #cv.create_layer(size=(300,200),color=(0,1,0,0.2))
    #cv.create_layer(size=(250,150),color=(0,0,1,0.2))    
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
    cm = MTCircularMenu_Manager(pos=(-225,-225),radius=225,canvas=cv)
    w.add_widget(cm)   
      
    cs = MTColorSelector(pos=(w.width-200,0),size=(200,200),win=w,canvas=cv)
    w.add_widget(cs)
   
    runTouchApp()
  