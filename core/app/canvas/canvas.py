from __future__ import with_statement
from pymt import *
from pyglet.image import *
from pyglet.gl import *
from layermanager import *
from core.app.observer import *
from os.path import join

class CanvasButtons(MTWidget):
    def __init__(self, **kwargs):
        super(CanvasButtons, self).__init__(**kwargs)

        self.toolbar_grid = MTBoxLayout(pos=(self.pos[0]+10,self.pos[1]+25),spacing=5)
        self.add_widget(self.toolbar_grid)
        
        close_button = MTImageButton(filename=os.path.join("gfx","icons","close_small.png"))
        self.toolbar_grid.add_widget(close_button)
        
        #work_area_button = MTImageButton(filename=os.path.join("gfx","icons","minimize_small.png"))
        #self.toolbar_grid.add_widget(work_area_button)
        
        self.size = (self.toolbar_grid._get_content_width()+30,self.toolbar_grid._get_content_height()+30)
        
        """@work_area_button.event
        def on_release(*largs):
            ob = Observer.get('canvas')
            if not ob.work_area_hidden:
                work_area_button._set_filename(filename=os.path.join("gfx","icons","maximize_small.png"))
                ob.hide_work_area()
            else:
                work_area_button._set_filename(filename=os.path.join("gfx","icons","minimize_small.png"))
                ob.show_work_area()
        """
        
        @close_button.event
        def on_press(*largs):
            self.parent.hide()
        
    def draw(self):
        set_color(0.3,0.3,0.3,1.0)
        drawCSSRectangle(size=self.size,pos=self.pos,style={'border-radius': 10,'border-radius-precision': .1})
        self.toolbar_grid.dispatch_event('on_draw')
        
class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.auto_bring_to_front = True
               
        self.buttons = CanvasButtons(pos=(0,self.height))
        self.add_widget(self.buttons)
        
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
        
        self.work_area_hidden = False
        self.prev_size = self.size
        self.prev_pos = self.pos
		
    def draw(self):
        with gx_matrix:
            glColor4f(0.3,0.3,0.3,1)
            drawCSSRectangle((0,0),(self.width,self.height),style=self.style)
            
    def set_mode(self,mode):
        self.layer_manager.set_mode(mode)

    def create_layer(self,pos=(0,0),size=(200,200)):
        self.layer_manager.create_layer(pos=pos,size=size)

    def get_image_data(self, ptexture):
        format = 'RGB'
        gl_format = GL_RGB

        if type(ptexture) == TextureRegion:
            texture = ptexture.owner
            z = ptexture.z
        else:
            texture = ptexture
            z = 0

        print texture.target, texture.id
        print texture.images, texture.width, texture.height
        glBindTexture(texture.target, texture.id)
        glPushClientAttrib(GL_CLIENT_PIXEL_STORE_BIT)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        buffer = \
            (GLubyte * (texture.width * texture.height * texture.images * len(format)))()
        print buffer
        glGetTexImage(texture.target, texture.level, 
                      gl_format, GL_UNSIGNED_BYTE, buffer)
        glPopClientAttrib()
        print 'buffer', buffer

        data = ImageData(texture.width, texture.height, format, buffer)
        print data
        if texture.images > 1:
            data = data.get_region(0, z * texture.height, texture.width, texture.height)
        if ptexture != texture:
            return data.get_region(ptexture.x, ptexture.y, ptexture.width, ptexture.height)
        return data
        
    def save_image(self):
        with self.fbo:
            bgcolor = list(self.layer_manager.background.bgcolor)[:3] + [1]
            glClearColor(*bgcolor)
            glClear(GL_COLOR_BUFFER_BIT)
            set_color(1, 1, 1, 1)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.layer_manager.background.dispatch_event('on_draw')
            for layer in self.layer_manager.layer_list :
                layer.dispatch_event('on_draw')
            
        data = self.get_image_data(self.fbo.texture)
        #data = self.get_image_data(self.layer_manager.background.fbo.texture)
        data.save(file='test.png')
    
    def current_canvas_view(self):
        with self.fbo:
            bgcolor = list(self.layer_manager.background.bgcolor)[:3] + [1]
            glClearColor(*bgcolor)
            glClear(GL_COLOR_BUFFER_BIT)
            set_color(1, 1, 1, 1)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            self.layer_manager.background.dispatch_event('on_draw')
            for layer in self.layer_manager.layer_list :
                layer.dispatch_event('on_draw')
                
        return self.fbo.texture
        
        
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
        
    def reset_fbo(self):
        with self.layer_manager.background.fbo:
            set_color(1, 1, 1, .99) 
            drawRectangle(pos=(0,0),size=self.size)
    
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
        
    def hide_work_area(self):
        self.work_area_hidden = True
        for child in self.children:
            if child == self.buttons:
                continue
            child.hide()
        self.prev_size = self.size
        self.prev_pos = self.pos
        self.size = (self.size[0],60)
        self.pos = (self.prev_pos[0],self.prev_pos[1]+self.prev_size[1])
        
    def show_work_area(self):
        self.work_area_hidden = False
        for child in self.children:
            if child == self.buttons:
                continue
            child.show()
        self.size = self.prev_size
        
    def close(self):
        self.parent.remove_widget(self)
		
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
    		
		
	
