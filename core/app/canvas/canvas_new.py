from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from layermanager import *

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.canvas_area = CanvasArea(pos=(10,10),size=(500,400))
        self.add_widget(self.canvas_area)
		
    def draw(self):
        with gx_matrix:
            glColor4f(0,0,0,1)
            drawRectangle((0,0),(self.width,self.height))

class CanvasArea(MTStencilContainer):
    def __init__(self, **kwargs):
        super(CanvasArea, self).__init__(**kwargs)
        self.layer_manager = LayerManager(pos=(10,10),canvas=self)
        self.add_widget(self.layer_manager)
        
    #def draw(self):
    #    pass
        #self.draw() 
		
		
		
if __name__ == '__main__':
    w = MTWindow()
    canvas = Canvas(size=(520,420))
    w.add_widget(canvas)    
    runTouchApp()
    		
		
	