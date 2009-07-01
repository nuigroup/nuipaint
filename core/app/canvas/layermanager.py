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
        self.background = Layer(size=self.canvas.size,color=(1,1,1,1),moveable=False,layer_manager=self)
        self.add_widget(self.background)
        self.layer1 = Layer(pos=(100,100),size=(200,200),color=(1,0,0,0.5),layer_manager=self)
        self.add_widget(self.layer1)
        self.layer2 = Layer(size=(300,200),color=(0,1,0,0.5),layer_manager=self)
        self.add_widget(self.layer2)
        self.layer3 = Layer(size=(250,150),color=(0,0,1,0.5),layer_manager=self)
        self.add_widget(self.layer3)
        
        self.layer_list.append(self.layer1)
        self.layer_list.append(self.layer2)
        self.layer_list.append(self.layer3)
        
    def set_mode(self,value):
        self.mode = value
        
    
        
   