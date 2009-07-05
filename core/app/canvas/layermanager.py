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
        #self.size = self.canvas.size
        self.layer_list = []
        self.brush_color = (0,0,0,1)
        self.brush_sprite = "brushes/brush_particle.png"
        self.brush_size = 64
        self.background = NormalLayer(size=self.size,color=(1,1,1,1),moveable=False,layer_manager=self)
        self.add_widget(self.background)

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
        
        
    def create_layer(self,pos=(0,0),size=(200,200),color=(0,0,0,0.5)):
        layer = NormalLayer(id=len(self.layer_list),pos=pos,size=size,color=color,layer_manager=self)
        self.add_widget(layer)
        self.layer_list.append(layer)

class layerListScroller(MTKineticList):
    def __init__(self, **kwargs):
        super(layerListScroller, self).__init__(**kwargs)
        
    def draw(self):
        set_color(*self.style['bg-color'])
        drawRectangle(self.pos, self.size)  #background
        super(MTKineticList, self).on_draw()
        for w in self.widgets:
            w.on_draw()
            
class layerItem(MTButton):
    def __init__(self, **kwargs):
        super(layerItem, self).__init__(**kwargs)
        self.layer_text   = kwargs.get('layer_text')
        self.label = self.layer_text
        self.labelWX = MTLabel(label=str(self.layer_text)[:15])#,anchor_x="center",anchor_y="center",halign="center")
        self.add_widget(self.labelWX)
        self.size = (180,60)
        self.layer = kwargs.get('layer_ptr')

    def draw(self):        
        set_color(*self.style['bg-color'])
        drawRectangle(self.pos, self.size)
        self.labelWX.pos = (self.x+70,self.y+25)
        
    def on_press(self, touches, touchID, x, y):
        if touches[touchID].is_double_tap:
            print  "Show layer options"
        else:
            if self.layer.highlight == False :
                self.layer.highlight = True 
            else:
                self.layer.highlight = False 
        return True
       
class layerEntry(layerItem, MTKineticObject):
    def __init__(self, **kwargs):
        super(layerEntry, self).__init__(**kwargs)
        self.layer_text   = kwargs.get('layer_text')
    
            
class LayerManagerList(MTRectangularWidget):
     def __init__(self, **kwargs):
        super(LayerManagerList, self).__init__(**kwargs)
        self.size = (200,400)
        self.layer_list = kwargs.get('layer_list')
        self.list_layout = layerListScroller(w_limit=1, deletable=False, searchable=False,size=(self.width-20,self.height-20),pos=(self.pos[0]+10,self.pos[1]+10))
        self.add_widget(self.list_layout)
        z=1
        if len(self.layer_list) == 0:
            entry = layerEntry(layer_text='No Layers')
            self.list_layout.add_widget(entry)
        else:
            for layer in self.layer_list:
                entry = layerEntry(layer_text=str(z),layer_ptr=layer)
                self.list_layout.add_widget(entry)
                z+=1
        
     
    
if __name__ == '__main__':
    w = MTWindow()
    ll = LayerManagerList(pos=(w.width-200,w.height-400))
    w.add_widget(ll)
    runTouchApp()    
        

        
    
        
   