from __future__ import with_statement
from math import cos,sin,pi
from pymt import *

from core import *

additional_css = '''
.roundedBorder {
    border-radius: 20;
    border-radius-precision: .1;
}

'''
css_add_sheet(additional_css)

if __name__ == '__main__':
    w = MTWindow()
    #Canvas
    cv = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))
    w.add_widget(cv) 
    
    cv.create_layer(pos=(100,100),size=(200,200))
    cv.create_layer(size=(300,200))
    cv.create_layer(size=(250,150))
    
    lm = LayerManagerList(pos=(w.width-200,w.height-300),layer_list=cv.getList(),cls=('roundedBorder'))
    w.add_widget(lm)
    
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
    cm = MTCircularMenu(pos=(-225,-225),radius=225,canvas=cv)
    w.add_widget(cm)   
      
    cs = MTColorSelector(pos=(w.width-200,0),size=(200,200),win=w,canvas=cv)
    w.add_widget(cs)
   
    runTouchApp()
  