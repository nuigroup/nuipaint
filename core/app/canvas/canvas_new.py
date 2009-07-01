from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from layermanager import *

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.canvas_area = MTStencilContainer(pos=(20,20),size=(500,400))
        self.add_widget(self.canvas_area)
        self.layer_manager = LayerManager(pos=(20,20),canvas=self)
        self.canvas_area.add_widget(self.layer_manager)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
		
    def draw(self):
        with gx_matrix:
            glColor4f(0,0,0,1)
            drawRectangle((0,0),(self.width,self.height))
            
    def set_mode(self,mode):
        self.layer_manager.set_mode(mode)

    def create_layer(self,pos=(0,0),size=(200,200),color=(0,0,0,0.5)):
        self.layer_manager.create_layer(pos=pos,size=size,color=color)
        
    def save_image(self):
        with self.fbo:
            self.layer_manager.background.dispatch_event('on_draw')
            for layer in self.layer_manager.layer_list :
                layer.dispatch_event('on_draw')
		data = (self.fbo.texture).get_image_data()
        data.save(file='test.png')
		
if __name__ == '__main__':
    w = MTWindow()
    canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120))
    w.add_widget(canvas)
    draw_but = MTButton(label="Painting")
    w.add_widget(draw_but)
    @draw_but.event    
    def on_press(touchID, x, y):
        canvas.set_mode(mode='draw')
    zoom_but = MTButton(label="Layering",pos=(draw_but.width+5,0))
    w.add_widget(zoom_but)
    @zoom_but.event    
    def on_press(touchID, x, y):
        canvas.set_mode(mode='zoom')
    
    add_but = MTButton(label="Save",pos=(draw_but.width+zoom_but.width+10,0))
    @add_but.event    
    def on_press(touchID, x, y):
        canvas.save_image()
    w.add_widget(add_but)
    
    canvas.create_layer(pos=(100,100),size=(200,200),color=(1,0,0,0.8))
    canvas.create_layer(size=(300,200),color=(0,1,0,0.8))
    canvas.create_layer(size=(250,150),color=(0,0,1,0.8))
    runTouchApp()
    		
		
	