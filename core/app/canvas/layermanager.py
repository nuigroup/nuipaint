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
        if kwargs.get('background'):
            self.background = ImageLayer(size=self.size,color=(1,1,1,1),moveable=False,layer_manager=self)
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
        kwargs.setdefault('color', self.style['bg-color'])
        self.id = kwargs.get('id')
        self.layer_text   = kwargs.get('layer_text')
        self.label = self.layer_text
        self.labelWX = MTLabel(label=str(self.layer_text)[:15])#,anchor_x="center",anchor_y="center",halign="center")
        self.add_widget(self.labelWX)
        self.size = (180,60)
        self.layer = kwargs.get('layer_ptr')
        self.color = kwargs.get('color') 
        self.layer_list = kwargs.get('layer_list')

    def draw(self):        
        set_color(*self.color)
        drawRectangle(self.pos, self.size)
        self.labelWX.pos = (self.x+60,self.y+25)
        
    def on_press(self, touch) :
        touches = getAvailableTouchs()
        if touch.is_double_tap:
            print  "Show layer options"
        else:
            if self.layer.highlight == False :
                self.layer.highlight = True
                self.color = (1.0,0.4,0)
                self.layer_list.selected_layers.append(self.id)
            else:
                self.layer.highlight = False 
                self.color = self.style['bg-color']
                self.layer_list.selected_layers.remove(self.id)
        return True
       
class layerEntry(layerItem, MTKineticObject):
    def __init__(self, **kwargs):
        super(layerEntry, self).__init__(**kwargs)
        self.layer_text   = kwargs.get('layer_text')

#Class Definations for the buttons inside layerlist        
additional_css = '''
.simple {
	draw-alpha-background: 1;
	draw-border: 1;
	draw-slider-alpha-background: 1;
	draw-slider-border: 1;
	draw-text-shadow: 1;
}

.colored {
	bg-color: #ff5c00;
	border-radius: 20;
	border-radius-precision: .1;
	font-size: 10;
	slider-border-radius-precision: .1;
	slider-border-radius: 20;
}

'''  
css_add_sheet(additional_css)

class LayerManagerList(MTRectangularWidget):
    def __init__(self, **kwargs):
        super(LayerManagerList, self).__init__(**kwargs)
        self.size = (200,300)
        self.list_layout = layerListScroller(w_limit=1, deletable=False, searchable=False,size=(self.width-20,self.height-60),pos=(self.pos[0]+10,self.pos[1]+50))
        self.list_items = []
        self.selected_layers = []
        self.add_widget(self.list_layout)
        self.layer_manager = kwargs.get('layer_manager')
        self.layer_list = self.layer_manager.layer_list

        if len(self.layer_list) == 0:
            entry = layerEntry(layer_text='No Layers')
            self.list_layout.add(entry)
            self.list_items.append(entry)
        else:
            for layer in self.layer_list:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self)
                self.list_layout.add(entry)
                self.list_items.append(entry)
        
        
        create = MTButton(label="New",pos=(self.pos[0]+10,self.pos[1]+10),size=(50,30),cls=('simple', 'colored'))
        self.add_widget(create)
        
        @create.event    
        def on_press(touch):
            if self.list_layout.pchildren[0].label == 'No Layers':
                for item in self.list_items:
                    self.list_layout.delete_item(item)
                    self.list_items.remove(item)
            self.layer_manager.create_layer(pos=(0,0),size=(200,200))
            self.updateLayerList()
        
        delete = MTButton(label="Delete",pos=(self.pos[0]+70,self.pos[1]+10),size=(55,30),cls=('simple', 'colored'))
        self.add_widget(delete)
        
        @delete.event    
        def on_press(touch):
            self.layer_manager.delete_layer(self.selected_layers)
            self.updateLayerList()
            if len(self.list_layout.pchildren) == 0 :
                entry = layerEntry(layer_text='No Layers')
                self.list_layout.add(entry)
                self.list_items.append(entry)
        
        resize = MTButton(label="Resize",pos=(self.pos[0]+135,self.pos[1]+10),size=(55,30),cls=('simple', 'colored'))
        self.add_widget(resize)
        
    def updateLayerList(self):
        for item in self.list_items:
            self.list_layout.delete_item(item)
            
        self.list_items = []
        
        self.layer_list = self.layer_manager.getLayerList()

        for layer in self.layer_list:
            if layer.id in self.selected_layers:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self,color=(1.0,0.4,0))
            else:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self)
            self.list_layout.add(entry)
            self.list_items.append(entry)
       
        
if __name__ == '__main__':
    w = MTWindow()
    ll = LayerManagerList(pos=(w.width-200,w.height-400))
    w.add_widget(ll)
    runTouchApp()    
        

        
    
        
   