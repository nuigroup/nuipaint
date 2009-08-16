from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from layer import *
from core.app.observer import *

class LayerManager(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        super(LayerManager, self).__init__(**kwargs)
        self.mode = "zoom"
        self.canvas = kwargs.get('canvas')
        #self.size = self.canvas.size
        self.layer_list = []
        self.brush_color = (0,0,0,1)
        self.brush_sprite = "brushes/brush_particle.png"
        self.brush_size = 64
        if kwargs.get('background'):
            self.background = ImageLayer(size=self.size,color=(1,1,1,1),moveable=False,layer_manager=self,file=kwargs.get('background'))
        else:
            self.background = NormalLayer(size=self.size,color=(1,1,1,1),moveable=False,layer_manager=self)
        self.add_widget(self.background)
        self.layer_counter = 0

    def set_mode(self,value):
        self.mode = value
        
    def set_brush_color(self,color):
        self.brush_color = color
    
    def set_brush(self,sprite,size):
        self.brush_sprite = sprite
        self.brush_size = size
        
    def move_layer_up(self,layer_id):  #double tapp on the layer to move up one layer at a time
        if layer_id < len(self.layer_list)-1:
            a = self.layer_list[layer_id]
            b = self.layer_list[layer_id+1]
            a.id = layer_id+1
            b.id = layer_id
            
            self.layer_list[layer_id] = b
            self.layer_list[layer_id+1] = a
            
            for layer in self.layer_list:
                self.remove_widget(layer)
                
            for layer in self.layer_list:
                self.add_widget(layer)

    def move_layer_down(self,layer_id): #hold one finger down and double tapp with another on the layer to move down one layer at a time
        if layer_id > 0:
            a = self.layer_list[layer_id]
            b = self.layer_list[layer_id-1]
            a.id = layer_id-1
            b.id = layer_id
            
            self.layer_list[layer_id] = b
            self.layer_list[layer_id-1] = a
            
            for layer in self.layer_list:
                self.remove_widget(layer)
                
            for layer in self.layer_list:
                self.add_widget(layer) 
        
    def getLayerList(self):
        return self.layer_list
    
    def create_layer(self,pos=(0,0),size=(200,200)):
        layer = NormalLayer(id=self.layer_counter,pos=pos,size=size,layer_manager=self)
        self.add_widget(layer)
        self.layer_counter += 1
        self.layer_list.append(layer)
        
    def create_image_layer(self,pos=(0,0),size=(200,200),texture=None):
        layer = ImageLayer(id=self.layer_counter,pos=pos,size=size,layer_manager=self)
        self.add_widget(layer)
        self.layer_counter += 1
        self.layer_list.append(layer)
        layer.set_new_fbo_image(texture)
        
    def delete_layer(self,selected_layers):
        list = self.layer_list
        del_list = []
        for layer in list:
            if layer.id in selected_layers:
                del_list.append(layer)
                
        for ele in del_list:
            self.layer_list.remove(ele)
            self.remove_widget(ele)
        del_list = []

    def draw(self):
        set_color(*self.background.bgcolor)
        drawRectangle(size=self.background.size)
        set_color(1, 1, 1, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
 
    def set_canvas(self,canvas):
        self.canvas = canvas
        
