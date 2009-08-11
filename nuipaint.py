from __future__ import with_statement
from math import cos,sin,pi
from pymt import *
from pyglet import clock

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
        handler = kwargs.get('handler')
        #self.canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'))#Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background="images/photo3.jpg")
        self.canvas = kwargs.get('canvas')
        self.add_widget(self.canvas) 
        
        #cv.create_layer(pos=(100,100),size=(200,200))
        #cv.create_layer(size=(300,200))
        #cv.create_layer(size=(250,150))
        
        lm = LayerManagerList(pos=(w.width-200,w.height-300),layer_manager=self.canvas.getListManager(),cls=('roundedBorder'))
        self.add_widget(lm)
        
        #File Browser
        fb = MTFileBrowser(pos=(100,400),size=(400,380))
        self.add_widget(fb)
        fb.hide()
        
        @fb.event
        def on_select(filelist):
            print filelist       
            
        #Bottom Toolbar
        tb = toolbar(win=w,canvas=self.canvas)
        self.add_widget(tb)    
        #Top Toolbar
        topb = topBar(win=w,canvas=self.canvas,filebrowser=fb,handler=handler)
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
        self.wb = windowBar(win=w,canvas=self.canvas, handler = kwargs.get('handler'))
        self.add_widget(self.wb)
        
    def set_canvas(self, canvas):
        self.canvas = canvas
   
        
#The most abstract class holding each interaction widget
class NUIPaint(windowing):
    def __init__(self, **kwargs):
        super(NUIPaint, self).__init__(**kwargs)
        self.win = kwargs.get('window')
        
        if kwargs.get('file'):
            self.canvas = Canvas(size=(384,512),pos=(w.width/2-260,w.height/2-120),cls=('roundedBorder'),background=kwargs.get('file'))
        else:
            self.canvas = Canvas(size=(540,440),pos=(self.win.width/2-260,self.win.height/2-120),cls=('roundedBorder'))
        
        self.full_mode_painter = FullScreenPaint(window=self.win,canvas=self.canvas, handler = self)      
        
        self.windowed_mode_painter = WindowedPaint(window=self.win,canvas=self.canvas, handler = self)
        self.add_widget(self.windowed_mode_painter)
        self.on_unfullscreen()
        
    def on_fullscreen(self):
        self.add_widget(self.full_mode_painter)
        self.canvas.enableTransformations()
        self.canvas.init_transform((self.win.width/2-self.canvas.width/2,self.win.height/2-self.canvas.height/2), 0, 1)
        self.windowed_mode_painter.wb.hide()
        self.remove_widget(self.windowed_mode_painter)
                    
    def on_unfullscreen(self):
        self.add_widget(self.windowed_mode_painter)
        self.windowed_mode_painter.wb.show()
        self.canvas.disableTransformations()
        self.canvas.init_transform((-20,-20), 0, 1)
        self.remove_widget(self.full_mode_painter)

def init_nuipaint(w, *largs):    
    fb = MTFileBrowser(pos=(100,400),size=(400,380))
    w.add_widget(fb)
    fb.hide()
    
    new_button = MTIconButton(pos=(10,10),icon_file="gfx/icons/new_L.png",label="New")
    w.add_widget(new_button)
    
    @new_button.event
    def on_press(touch):
        new_win = NUIPaint(window = w,pos=(100,100),size=(500,400),style={'bg-color':(0.3,0.3,0.3,1),'bg-color-move':(0.3,0.3,0.3),'bg-color-full':(0.3,0.3,0.3),'border-width':20})
        w.add_widget(new_win)
    
    open_button = MTIconButton(pos=(new_button.width+30,10),icon_file="gfx/icons/open_L.png",label="Open")
    w.add_widget(open_button)
    
    @open_button.event
    def on_press(touch):
        fb.show()
        
    @fb.event
    def on_select(list):
        img = pyglet.image.load(list[0])
        open_window = NUIPaint(file=list[0],window = w,pos=(300,400),size=(img.width,img.height),style={'bg-color':(0.3,0.3,0.3,1),'bg-color-move':(0.2,0.2,0.2),'bg-color-full':(0.2,0.2,.2),'border-width':20})
        w.add_widget(open_window)
    
if __name__ == '__main__':
    w = MTWindow()
    clock.schedule_once(curry(init_nuipaint, w), 0)    
    runTouchApp()
  