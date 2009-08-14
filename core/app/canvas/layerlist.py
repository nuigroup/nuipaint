from __future__ import with_statement
from pymt import *
from core.app.observer import *

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
        if self.layer_text == 'No Layers':
            return True
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
        self.list_layout = MTKineticList(title=None,w_limit=1, deletable=False, searchable=False,size=(self.width-20,self.height-60),pos=(self.pos[0]+10,self.pos[1]+50))
        self.list_items = []
        self.selected_layers = []
        self.add_widget(self.list_layout)
        self.layer_manager = Observer.get("layer_manager")
        self.layer_list = self.layer_manager.layer_list

        if len(self.layer_list) == 0:
            entry = layerEntry(layer_text='No Layers')
            self.list_layout.add_widget(entry)
            self.list_items.append(entry)
        else:
            for layer in self.layer_list:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self)
                self.list_layout.add_widget(entry)
                self.list_items.append(entry)
        
        
        create = MTButton(label="New",pos=(self.pos[0]+10,self.pos[1]+10),size=(50,30),cls=('simple', 'colored'))
        self.add_widget(create)
        
        @create.event    
        def on_press(touch):
            if self.list_layout.pchildren[0].label == 'No Layers':
                for item in self.list_items:
                    self.list_layout.remove_widget(item)
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
                self.list_layout.add_widget(entry)
                self.list_items.append(entry)
        
        resize = MTButton(label="Resize",pos=(self.pos[0]+135,self.pos[1]+10),size=(55,30),cls=('simple', 'colored'))
        self.add_widget(resize)
        
    def updateLayerList(self):
        for item in self.list_items:
            self.list_layout.remove_widget(item)
            
        self.list_items = []
        
        self.layer_list = self.layer_manager.getLayerList()

        for layer in self.layer_list:
            if layer.id in self.selected_layers:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self,color=(1.0,0.4,0))
            else:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self)
            self.list_layout.add_widget(entry)
            self.list_items.append(entry)
            
    def set_new_list(self,layer_manager):
        for item in self.list_items:
            self.list_layout.remove_widget(item)
            
        self.list_items = []
        self.selected_layers = []
        self.layer_manager = layer_manager
        self.layer_list = self.layer_manager.layer_list

        if len(self.layer_list) == 0:
            entry = layerEntry(layer_text='No Layers')
            self.list_layout.add_widget(entry)
            self.list_items.append(entry)
        else:
            for layer in self.layer_list:
                entry = layerEntry(id=layer.id,layer_text="Layer "+str(layer.id),layer_ptr=layer,layer_list=self)
                self.list_layout.add_widget(entry)
                self.list_items.append(entry)
                
    def paste_layer(self,layer):
        if self.list_layout.pchildren[0].label == 'No Layers':
            for item in self.list_items:
                self.list_layout.remove_widget(item)
                self.list_items.remove(item)
        self.layer_manager.create_image_layer(pos=(0,0),size=(layer.width,layer.height),texture=layer.get_texture())        
        self.updateLayerList()
