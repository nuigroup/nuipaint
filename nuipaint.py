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
        #self.canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))#Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        self.canvas = kwargs.get('canvas')
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
        self.canvas = kwargs.get('canvas')
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
        self.win = kwargs.get('window')
        
        self.canvas = Canvas(size=(540,440),pos=(self.win.width/2-260,self.win.height/2-120),cls=('roundedBorder'))#Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        
        self.full_mode_painter = FullScreenPaint(window=self.win,canvas=self.canvas)      
        
        self.windowed_mode_painter = WindowedPaint(window=self.win,canvas=self.canvas)
        self.add_widget(self.windowed_mode_painter)
        self.on_unfullscreen()
        
    def on_fullscreen(self):
        self.add_widget(self.full_mode_painter)
        self.canvas.enableTransformations()
        self.canvas.init_transform((self.win.width/2-self.canvas.width/2,self.win.height/2-self.canvas.height/2), 0, 1)
        self.remove_widget(self.windowed_mode_painter)
            
    def on_unfullscreen(self):
        self.add_widget(self.windowed_mode_painter)
        self.canvas.disableTransformations()
        self.canvas.init_transform((0,0), 0, 1)
        self.remove_widget(self.full_mode_painter)
    
if __name__ == '__main__':
    w = MTWindow()
    
    in_win = NUIPaint(window = w,size=(540,440),style={'bg-color':(1,1,1),'bg-color-move':(1,0,0),'bg-color-full':(0,0,1),'border-width':20})
    w.add_widget(in_win)

    runTouchApp()
  