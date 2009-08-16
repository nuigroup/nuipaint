from __future__ import with_statement
from pymt import *
from core.app.observer import *
from pyglet.gl import *
from filters import *


class filterItem(MTButton):
    def __init__(self, **kwargs):
        super(filterItem, self).__init__(**kwargs)        
        kwargs.setdefault('color', self.style['bg-color'])
        self.filter_text   = kwargs.get('label')
        self.label = self.filter_text
        self.text_color = (0,0,0,1)
        if kwargs.get('text_color') == 'light':
            self.text_color = (1,1,1,1)
        self.labelWX = MTLabel(label=str(self.filter_text)[:15],color=self.text_color,bold=True)#,anchor_x="center",anchor_y="center",halign="center")
        self.add_widget(self.labelWX)
        self.size = (90,90)
        self.filterbox = kwargs.get('filterbox')
        self.color = kwargs.get('color') 
        self.img            = pyglet.image.load(kwargs.get('icon_file'))

    def draw(self):        
        set_color(*self.color)
        drawRectangle(self.pos, self.size)
        set_color(1,1,1,1)
        drawTexturedRectangle(texture=self.img.texture,pos=(self.pos[0],self.pos[1]), size=self.size)
        self.labelWX.pos = (self.x,self.y)
        
    def on_press(self, touch) :
        Observer.get('layer_manager').set_background(Observer.get('last_saved_background_view'))
        if (self.label).lower() == "blur":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.blur,min=0.0,max=5.0)
        elif (self.label).lower() == "sharpen":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.sharpen,min=0.0,max=5.0)
        elif (self.label).lower() == "brighten":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.brightness,min=0.0,max=2.0)
        elif (self.label).lower() == "contrast":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.contrast,min=1.0,max=2.0)
        elif (self.label).lower() == "saturation":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.saturation,min=0.0,max=2.0)
        elif (self.label).lower() == "b&w":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.bw,min=0.0,max=5.0)
        elif (self.label).lower() == "sepia":
            self.filterbox.set_current_filter(filter_function=self.filterbox.filter_engine.sepia,min=0.0,max=5.0)
           
class filterEntry(filterItem, MTKineticObject):
    def __init__(self, **kwargs):
        super(filterEntry, self).__init__(**kwargs)        


#Class Definations for the buttons inside filterlist        
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
	border-radius: 10;
	border-radius-precision: .1;
	font-size: 10;
	slider-border-radius-precision: .1;
	slider-border-radius: 20;
}

.roundedBorder {
    border-radius: 5;
    border-radius-precision: .1;
}

'''  
css_add_sheet(additional_css)

class FilterBox(MTRectangularWidget):
    def __init__(self, **kwargs):
        super(FilterBox, self).__init__(**kwargs)
        self.size = (140,300)
        self.list_layout = MTKineticList(title=None,w_limit=1, deletable=False, searchable=False,size=(90,self.height-60),pos=(self.pos[0]+10,self.pos[1]+50),cls=('roundedBorder'),padding_y=5)
        self.list_items = []
        self.add_widget(self.list_layout)
        
        self.layer_manager = Observer.get('layer_manager')
        #self.before_mod_texture =  Observer.get('last_saved_background_view')
        self.modding_texture = Observer.get('last_saved_background_view')
        
        self.filter_engine = Filter()
        self.current_filter_function = None
        
        blur = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','blur.jpg'),label="Blur")
        self.list_layout.add_widget(blur)
        
        bright = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','brightness.jpg'),label="Brighten")
        self.list_layout.add_widget(bright)
        
        bw = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','bw.jpg'),label="B&W")
        self.list_layout.add_widget(bw)
        
        contrast = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','contrast.jpg'),label="Contrast")
        self.list_layout.add_widget(blur)
        
        saturation = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','saturation.jpg'),label="Saturation",text_color="light")
        self.list_layout.add_widget(saturation)
        
        sharp = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','sharpness.jpg'),label="Sharpen")
        self.list_layout.add_widget(sharp)
        
        sepia = filterEntry(filterbox=self,icon_file=os.path.join('gfx','filter_icons','sepia.jpg'),label="Sepia")
        self.list_layout.add_widget(sepia)        
        
      
        self.slider = MTSlider(orientation='vertical',size=(20,self.height-60),pos=(self.list_layout.pos[0]+self.list_layout.width+10,self.pos[1]+50),cls=('roundedBorder'))
        self.add_widget(self.slider)
        
        @self.slider.event
        def on_value_change(value):
            if self.current_filter_function:
                back_texture = Observer.get('last_saved_background_view')
                self.modding_texture=self.current_filter_function(back_texture,(back_texture.width,back_texture.height),value)
                self.layer_manager.set_background(self.modding_texture)
        
        apply = MTButton(label="Apply",pos=(self.pos[0],self.pos[1]),size=(100,30),cls=('simple', 'colored'))
        self.add_widget(apply)
        apply.pos = (self.pos[0]+self.width/2-apply.width/2,self.pos[1]+10)
        @apply.event    
        def on_press(touch):
            self.apply_filter()
            self.hide()
        

    def set_current_filter(self, filter_function, min, max):
        self.current_filter_function = filter_function
        self.slider.min = min
        self.slider.max = max
        self.slider._value = 0

    def apply_filter(self):
        Observer.get('layer_manager').set_background(self.modding_texture)
        Observer.register('last_saved_background_view',Observer.get('canvas').current_canvas_view())
        

    