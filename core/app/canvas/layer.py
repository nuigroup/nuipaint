from __future__ import with_statement
from pymt import *
from pyglet.gl import *

class specialScatterW(MTScatterWidget):
    def __init__(self, **kwargs):
        super(specialScatterW, self).__init__(**kwargs)
    
    def on_touch_down(self, touches, touchID, x, y):
        # if the touch isnt on the widget we do nothing
        if not self.collide_point(x,y):
            return False

        # let the child widgets handle the event if they want
        lx, ly = self.to_local(x,y)
        if super(MTScatterWidget, self).on_touch_down(touches, touchID, lx, ly):
            return True

        # if the children didnt handle it, we bring to front & keep track
        # of touches for rotate/scale/zoom action
        #self.bring_to_front()
        self.touches[touchID] = Vector(x,y)
        return True
        
class AbstractLayer(specialScatterW):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.layer_manager = kwargs.get('layer_manager')        
        super(AbstractLayer, self).__init__(**kwargs)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)                
        self.color = (1,1,1,0)
        self.bgcolor = (1,1,1,1)
        self.layer_clear()
        self.id = kwargs.get('id')

    def layer_clear(self):
        with self.fbo:
            if self.moveable == False :
                glClearColor(1,1,1,1)
            else:
                glClearColor(*self.color)
            glClear(GL_COLOR_BUFFER_BIT)
            glClearColor(1,0,1,1)
            set_color(self.color)
            drawRectangle((0,0),(self.width,self.height))

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y): 
            self.touches[touchID] = self.to_local(x,y)
            if len(touches)==2 :                
                if touches[touchID].is_double_tap:
                    self.layer_manager.move_layer_down(self.id)
            elif touches[touchID].is_double_tap:
               self.layer_manager.move_layer_up(self.id)
            if self.layer_manager.mode == "draw":
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((x,y,x+1,y+1))                    
            elif self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_down(touches, touchID, x, y)
            return True
            
    def on_touch_move(self, touches, touchID, x, y):
        if touchID in self.touches:
            if self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_move(touches, touchID, x, y)
            elif self.layer_manager.mode == "draw":
                cur_pos = self.to_local(x,y)
                ox,oy = self.touches[touchID]
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((ox,oy,cur_pos[0],cur_pos[1]))                    
                self.touches[touchID] = self.to_local(x,y)
            return True
            
    def on_touch_up(self, touches, touchID, x,y):
        if touchID in self.touches:
            del self.touches[touchID]
            return True
    
            
       

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
                with gx_blending:
                    glColor4f(*self.bgcolor)
                    drawRectangle((0,0),(self.width,self.height))
                    drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
            else:
                with gx_blending:
                    if self.highlight == True :
                        glColor4f(0,0,1,0.2)
                        drawRectangle((0,0),(self.width,self.height))
                    drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))        
