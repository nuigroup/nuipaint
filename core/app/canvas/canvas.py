from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from layermanager import *
from core.app.observer import *

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)        
        if kwargs.get('background'):
            self.back_image = pyglet.image.load(kwargs.get('background'))
            self.size = (self.back_image.width,self.back_image.height)
            
        self.canvas_area = MTStencilContainer(pos=(20,20),size=(self.width,self.height))
        self.add_widget(self.canvas_area)
        if kwargs.get('background'):
            self.layer_manager = LayerManager(pos=(20,20),canvas=self,size=(self.width,self.height),background=kwargs.get('background'))
        else:
            self.layer_manager = LayerManager(pos=(20,20),canvas=self,size=(self.width,self.height))
        self.canvas_area.add_widget(self.layer_manager)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
        self.canvas_size = kwargs.get('size')
        self.size = (self.canvas_size[0]+40,self.canvas_size[1]+40)

		
    def draw(self):
        with gx_matrix:
            glColor4f(0.3,0.3,0.3,1)
            drawCSSRectangle((0,0),(self.width,self.height),style=self.style)
            
    def set_mode(self,mode):
        self.layer_manager.set_mode(mode)

    def create_layer(self,pos=(0,0),size=(200,200)):
        self.layer_manager.create_layer(pos=pos,size=size)
        
    def save_image(self):
        with self.fbo:
            set_color(1, 1, 1, .99) 
            self.layer_manager.background.dispatch_event('on_draw')
            for layer in self.layer_manager.layer_list :
                set_color(1, 1, 1, .99) 
                layer.dispatch_event('on_draw')
            
        data = (self.fbo.texture).get_image_data()
        data.save(file='test.png')
        
    def set_brush_color(self,color):
        self.layer_manager.set_brush_color(color)
    
    def set_brush(self,sprite,size):
        self.layer_manager.set_brush(sprite,size)
        
    def collide_point(self, x,y):
        local_coords = self.to_local(x,y)
        if local_coords[0] > 0 and local_coords[0] < self.width \
           and local_coords[1] > 0 and local_coords[1] < self.height:
            return True
        else:
            return False
        
    def getListManager(self):
        return self.layer_manager
        
    def disableTransformations(self):
        self.do_scale       = False
        self.do_rotation    = False
        self.do_translation = False
    
    def enableTransformations(self):
        self.do_scale       = True
        self.do_rotation    = True
        self.do_translation = True
    
    def get_fbo_texture(self):
        with self.fbo:
            set_color(1, 1, 1, .99) 
            self.layer_manager.background.dispatch_event('on_draw')
        return self.fbo.texture
    
    def on_touch_down(self,touch):
        if self.collide_point(touch.x,touch.y):
            if Observer.get('canvas') != self:
                Observer.register('canvas',self)
                Observer.register('layer_manager',self.layer_manager)
                self.reset_all_canvas_deps()
                Observer.get("layer_manager_list").set_new_list(self.layer_manager)
            super(Canvas, self).on_touch_down(touch)
            
    def reset_all_canvas_deps(self):
        Observer.get("bottom_toolbar").canvas = self
        Observer.get("top_toolbar").canvas = self
        Observer.get("brush_resizer").canvas = self
        Observer.get("circular_menu").canvas = self
        Observer.get("color_selector").canvas = self
		
if __name__ == '__main__':
    w = MTWindow()
    canvas = Canvas(size=(540,440),pos=(w.width/2-260,w.height/2-120))
    w.add_widget(canvas)
    draw_but = MTButton(label="Painting")
    w.add_widget(draw_but)
    @draw_but.event    
    def on_press(touch) :
        canvas.set_mode(mode='draw')
    zoom_but = MTButton(label="Layering",pos=(draw_but.width+5,0))
    w.add_widget(zoom_but)
    @zoom_but.event    
    def on_press(touch) :
        canvas.set_mode(mode='zoom')
    
    add_but = MTButton(label="Save",pos=(draw_but.width+zoom_but.width+10,0))
    @add_but.event    
    def on_press(touch) :
        canvas.save_image()
    w.add_widget(add_but)
    
    canvas.create_layer(pos=(100,100),size=(200,200))
    canvas.create_layer(size=(300,200))
    canvas.create_layer(size=(250,150))
    runTouchApp()
    		
		
	