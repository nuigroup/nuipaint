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


class FullScreenPaint(MTWidget):
    def __init__(self, **kwargs):
        super(FullScreenPaint,self).__init__(**kwargs)
        #Canvas
        w = kwargs.get('window')
        self.canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))#Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        self.add_widget(self.canvas) 
        
        #cv.create_layer(pos=(100,100),size=(200,200))
        #cv.create_layer(size=(300,200))
        #cv.create_layer(size=(250,150))
        
        lm = LayerManagerList(pos=(w.width-200,w.height-300),layer_manager=self.canvas.getListManager(),cls=('roundedBorder'))
        self.add_widget(lm)
        
        #File Browser
        fb = MTFileBrowser(pos=(100,500),size=(400,300))
        self.add_widget(fb)
        fb.hide()
        
        #Bottom Toolbar
        tb = toolbar(win=w,canvas=self.canvas)
        self.add_widget(tb)    
        #Top Toolbar
        topb = topBar(win=w,canvas=self.canvas,filebrowser=fb)
        self.add_widget(topb)
        
        #Side Ciruclar Menu
        cm = MTCircularMenu(pos=(-225,-225),radius=225,canvas=self.canvas)
        self.add_widget(cm)   
          
        cs = MTColorSelector(pos=(w.width-200,0),size=(200,200),win=w,canvas=self.canvas)
        self.add_widget(cs)
        
        #cv2 = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        #w.add_widget(cv2)
    
    def set_canvas(self, canvas):
        self.canvas = canvas

class WindowedPaint(MTWidget):
    def __init__(self, **kwargs):
        super(WindowedPaint, self).__init__(**kwargs)        
        self.canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))
        self.add_widget(self.canvas)
        #Bottom Toolbar
        tb = toolbar(win=w,canvas=self.canvas)
        self.add_widget(tb)
        
    def set_canvas(self, canvas):
        self.canvas = canvas
   
        
#The most abstract class holding each interaction widget
class NUIPaint(windowing):
    def __init__(self, **kwargs):
        super(NUIPaint, self).__init__(**kwargs)
        w = self.get_parent_window()
        
        self.canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))#Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        
        full_mode_painter = kwargs.get('full_mode')
        full_mode_painter.set_canvas(self.canvas)
        
        windowed_mode_painter = kwargs.get('win_mode')
        windowed_mode_painter.set_canvas(self.canvas)
    
if __name__ == '__main__':
    w = MTWindow()
    #temporary instantiated object
    full = FullScreenPaint(window=w)
    windowed = WindowedPaint(window=w)
    
    in_win = NUIPaint(full_mode = full, win_mode = windowed,size=(540,440),style={'bg-color':(1,1,1),'bg-color-move':(1,0,0),'bg-color-full':(0,0,1),'border-width':20})
    w.add_widget(in_win)

    runTouchApp()
  