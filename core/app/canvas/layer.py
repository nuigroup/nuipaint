from __future__ import with_statement
from pymt import *
from pyglet.gl import *

class specialScatterW(MTScatterWidget):
    def __init__(self, **kwargs):
        super(specialScatterW, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        # if the touch isnt on the widget we do nothing
        if not self.collide_point(touch.x,touch.y):
            return False

        # let the child widgets handle the event if they want
        prevx,prevy = touch.x,touch.y
        lx, ly = self.to_local(touch.x,touch.y)
        touch.x,touch.y = lx,ly
        if super(MTScatterWidget, self).on_touch_down(touch):
            return True

        # if the children didnt handle it, we bring to front & keep track
        # of touches for rotate/scale/zoom action
        #self.bring_to_front()
        touch.x,touch.y = prevx,prevy
        self.touches[touch.id] = Vector(touch.x,touch.y)
        return True
        
class AbstractLayer(specialScatterW):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.layer_manager = kwargs.get('layer_manager')        
        super(AbstractLayer, self).__init__(**kwargs)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)                
        self.color = (1,1,1,1)
        self.bgcolor = (1,1,1,1)
        #self.layer_clear()
        self.id = kwargs.get('id')

    def layer_clear(self):
        with self.fbo:
            if self.moveable == False :
                glClearColor(1,1,1,1)
            else:
                glClearColor(*self.color)
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(1,1,1,1)
            set_color(self.color)
            drawRectangle((0,0),(self.width,self.height))

    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y): 
            #prevx,prevy = touch.x,touch.y
            self.touches[touch.id] = self.to_local(touch.x,touch.y)
            if len(touches)==2 :                
                if touches[touch.id].is_double_tap:
                    self.layer_manager.move_layer_down(self.id)
            elif touches[touch.id].is_double_tap:
               self.layer_manager.move_layer_up(self.id)
            if self.layer_manager.mode == "draw":
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((x,y,x+1,y+1))                    
            elif self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_down(touch)
            return True
            
    def on_touch_move(self, touch):
        if touch.id in self.touches:
            if self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_move(touch)
            elif self.layer_manager.mode == "draw":
                cur_pos = self.to_local(touch.x,touch.y)
                ox,oy = self.touches[touch.id]
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((ox,oy,cur_pos[0],cur_pos[1]))                    
                self.touches[touch.id] = self.to_local(touch.x,touch.y)
            return True
            
    def on_touch_up(self, touch):
        if touch.id in self.touches:
            del self.touches[touch.id]
            return True
            
    def getLayerManager(self):
        return self.layer_manager
         

class NormalLayer(AbstractLayer):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.moveable = kwargs.get('moveable')
        if self.moveable == False :
            kwargs.setdefault('do_scale', False)
            kwargs.setdefault('do_rotation', False)
            kwargs.setdefault('do_translation', False)
        super(NormalLayer, self).__init__(**kwargs)
        self.highlight =  False        
        
    def draw(self):
        with gx_matrix:
            #glColor4f(*self.color)
            if self.moveable == False :
                glColor4f(*self.bgcolor)
                drawRectangle((0,0),(self.width,self.height))
                drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
            else:
                drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
                if self.highlight == True :
                    glColor4f(0,0,1,0.2)
                    drawRectangle((0,0),(self.width,self.height))                    

class ImageLayer(AbstractLayer):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.moveable = kwargs.get('moveable')
        if self.moveable == False :
            kwargs.setdefault('do_scale', False)
            kwargs.setdefault('do_rotation', False)
            kwargs.setdefault('do_translation', False)
        super(ImageLayer, self).__init__(**kwargs)
        self.highlight =  False 
        self.background = "images/photo3.jpg"
        img = pyglet.image.load(self.background)
        self.image  = pyglet.sprite.Sprite(img)
  
        
    def draw(self):
        with gx_matrix:
                self.image.draw()
                drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
 