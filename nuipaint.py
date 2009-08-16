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
        self.w = Observer.get('window')
        self.handler = kwargs.get('handler')
        self.canvas = Observer.get("canvas")
        self.add_widget(self.canvas) 
        Observer.register("layer_manager",self.canvas.getListManager())
        
        self.lm = LayerManagerList(pos=(w.width-200,w.height-300),cls=('roundedBorder'))
        self.add_widget(self.lm)
        Observer.register("layer_manager_list",self.lm)
        
        #File Browser
        self.fb = MTFileBrowser(pos=(100,400),size=(400,380),exit_on_submit=False)
        self.add_widget(self.fb)
        self.fb.hide()
        Observer.register("file_browser",self.fb)
        
        @self.fb.event
        def on_select(list):
            for item in list:
                img = pyglet.image.load(item)
                new_canvas = Canvas(size=(img.width,img.height),pos=(0,0),cls=('roundedBorder'),background=item)
                self.add_widget(new_canvas)       
            
        #Bottom Toolbar
        self.tb = toolbar()
        self.add_widget(self.tb)
            
        #Top Toolbar
        self.topb = topBar()
        self.add_widget(self.topb)
        
        #Brush Resizer
        self.br = MTBrushResizer(size=(100,100))
        self.add_widget(self.br)
        
        #Side Ciruclar Menu
        self.cm = MTCircularMenu(pos=(-225,-225),radius=225)
        self.add_widget(self.cm)
        
        #Intialize Circular menu with brushes
        brush_list = []
        #by default generate a brushes list in circular menu        
        for brush in glob('brushes/*.png'):
            brush_list.append([brush,self.br.set_brush,brush])
            
        self.cm.set_list(list=brush_list)        
          
        self.cs = MTColorSelector(pos=(w.width-200,0),size=(200,200))
        self.add_widget(self.cs)
        
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def register_to_observer(self):
        Observer.register("window",self.w)
        Observer.register("inner_window_handler",self.handler)
        Observer.register("canvas",self.canvas)
        Observer.register("layer_manager",self.canvas.getListManager())
        Observer.register("layer_manager_list",self.lm)
        Observer.register("file_browser",self.fb)
        Observer.register("bottom_toolbar",self.tb)
        Observer.register("top_toolbar",self.topb)
        Observer.register("brush_resizer",self.br)
        Observer.register("circular_menu",self.cm)
        Observer.register("color_selector",self.cs)


class WindowedPaint(MTWidget):
    def __init__(self, **kwargs):
        super(WindowedPaint, self).__init__(**kwargs)        
        self.canvas = Observer.get('canvas')
        self.add_widget(self.canvas)
        #Bottom Toolbar
        self.wb = windowBar()
        self.add_widget(self.wb)
        
    def set_canvas(self, canvas):
        self.canvas = canvas

        
#The most abstract class holding each interaction widget
class NUIPaint(windowing):
    def __init__(self, **kwargs):
        super(NUIPaint, self).__init__(**kwargs)
        self.win = Observer.get('window')
        
        if kwargs.get('file'):
            self.canvas = Canvas(size=(self.size[0],self.size[1]),pos=(0,0),cls=('roundedBorder'),background=kwargs.get('file'))
        else:
            self.canvas = Canvas(size=(self.size[0],self.size[1]),pos=(40,40),cls=('roundedBorder'))
            
        Observer.register("inner_window_handler",self)
        Observer.register("canvas",self.canvas)
        
        self.full_mode_painter = FullScreenPaint()      
        
        self.windowed_mode_painter = WindowedPaint()
        self.add_widget(self.windowed_mode_painter)
        self.on_unfullscreen()
        
    def on_fullscreen(self):
        self.add_widget(self.full_mode_painter)
        self.full_mode_painter.register_to_observer()
        self.canvas.enableTransformations()
        self.canvas.init_transform((self.win.width/2-self.canvas.width/2,self.win.height/2-self.canvas.height/2), 0, 1)
        self.windowed_mode_painter.wb.hide()
        self.remove_widget(self.windowed_mode_painter)
                    
    def on_unfullscreen(self):
        self.add_widget(self.windowed_mode_painter)        
        self.canvas.disableTransformations()
        self.canvas.init_transform((-20,-20), 0, 1)
        self.windowed_mode_painter.wb.show()
        self.windowed_mode_painter.wb.bring_to_front()
        self.remove_widget(self.full_mode_painter)

def init_nuipaint(w, *largs):
    Observer.register('window',w)
    
    clipboard = Clipboard()
    Observer.register('clipboard',clipboard)
    
    fb = MTFileBrowser(pos=(100,100),size=(400,380),exit_on_submit=False)
    w.add_widget(fb)
    Observer.register('desktop_file_browser',fb)
    Observer.get('desktop_file_browser').hide()
    
    
    new_button = MTIconButton(pos=(10,10),icon_file="gfx/icons/new_L.png",label="New")
    w.add_widget(new_button)
    
    @new_button.event
    def on_press(touch):
        win  = MTPopup(label_submit="Create", title="New Canvas",size=(400, 350),pos=(10,100))
        xml = XMLWidget(xml='''<?xml version="1.0"?>
        <MTGridLayout cols="2" rows="2" spacing="2" padding="2">
            <MTLabel label="'Width'" autoheight="True"/>
            <MTTextInput id="'input_width'" label="'500'" height="30"/>
            <MTLabel label="'Height'" autoheight="True"/>
            <MTTextInput id="'input_height'" label="'400'" height="30"/>
        </MTGridLayout>
        ''')
        win.add_widget(xml.children[0], True)
        width_txt = getWidgetById('input_width')
        height_txt = getWidgetById('input_height')

        w.add_widget(win)
        @win.event
        def on_submit(*largs):
            new_win = NUIPaint(pos=(200,200),size=(int(width_txt.get_label()),int(height_txt.get_label())),style={'bg-color':(0.3,0.3,0.3,1),'bg-color-move':(0.3,0.3,0.3),'bg-color-full':(0.3,0.3,0.3),'border-width':20})
            w.add_widget(new_win)
    
    open_button = MTIconButton(pos=(new_button.width+30,10),icon_file="gfx/icons/open_L.png",label="Open")
    w.add_widget(open_button)
    
    @open_button.event
    def on_press(touch):
        fb.show()
        
    @fb.event
    def on_select(list):
        for item in list:
            img = pyglet.image.load(item)
            open_window = NUIPaint(file=item,window = w,pos=(200,200),size=(img.width,img.height),style={'bg-color':(0.3,0.3,0.3,1),'bg-color-move':(0.3,0.3,0.3),'bg-color-full':(0.3,0.3,0.3),'border-width':20})
            w.add_widget(open_window)
    
if __name__ == '__main__':
    w = MTWindow()
    clock.schedule_once(curry(init_nuipaint, w), 0)    
    runTouchApp()
  
