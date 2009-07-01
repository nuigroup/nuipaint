from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from layer import *

class LayerManager(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_rotation', False)
        kwargs.setdefault('do_translation', False)
        super(LayerManager, self).__init__(**kwargs)
        self.mode = "zoom"
        self.canvas = kwargs.get('canvas')
        self.size = self.canvas.size
        self.layer_list = []
        self.background = NormalLayer(size=self.canvas.size,color=(1,1,1,1),moveable=False,layer_manager=self)
        self.add_widget(self.background)

        
    def set_mode(self,value):
        self.mode = value
        
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
        
        
    def create_layer(self,pos=(0,0),size=(200,200),color=(0,0,0,0.5)):
        layer = NormalLayer(id=len(self.layer_list),pos=pos,size=size,color=color,layer_manager=self)
        self.add_widget(layer)
        self.layer_list.append(layer)
    
    
    
        

        
    
        
   