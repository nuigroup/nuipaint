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
    

class Layer(specialScatterW):
    def __init__(self, **kwargs):
        self.moveable = kwargs.get('moveable')
        if self.moveable == False :
            kwargs.setdefault('do_scale', False)
            kwargs.setdefault('do_rotation', False)
            kwargs.setdefault('do_translation', False)
        super(Layer, self).__init__(**kwargs)        
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
        self.color = kwargs.get('color')
        set_brush('brushes/brush_particle.png')
        self.layer_clear()
        self.touch_positions = {}
        self.mode = "zoom"
        set_brush_size(25)
        self.brush_color=(0,0,0,1)

    def layer_clear(self):
        self.fbo.bind()
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT)
        set_color(self.color)
        drawRectangle((0,0),(self.width,self.height))
        self.fbo.release()

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y): 
            self.touch_positions[touchID] = self.to_local(x,y)            
            if self.mode == "draw":
                self.fbo.bind()
                set_color(*self.brush_color)
                set_brush('brushes/brush_particle.png')
                set_brush_size(25)
                drawCircle(pos=self.to_local(x,y), radius=1)            
                self.fbo.release()
            elif self.mode == "zoom":
                super(Layer, self).on_touch_down(touches, touchID, x, y)

            return True
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.touch_positions.has_key(touchID):
            if self.mode == "zoom":
                super(Layer, self).on_touch_move(touches, touchID, x, y)
            elif self.mode == "draw":
                cur_pos = self.to_local(x,y)
                ox,oy = self.touch_positions[touchID]
                self.fbo.bind()
                set_color(*self.brush_color)
                set_brush('brushes/brush_particle.png')
                set_brush_size(25)
                paintLine((ox,oy,cur_pos[0],cur_pos[1]))
                self.fbo.release()
                self.touch_positions[touchID] = self.to_local(x,y)
            return True

    def draw(self):
        with gx_matrix:
           glColor4f(*self.color)
           drawRectangle((0,0),(self.width,self.height))
           #with gx_blending:
           #     drawTexturedRectangle(self.fbo.texture, (-6,-6),(self.width+12,self.height+12))
    
    def set_mode(self,mode):
        self.mode = mode
        
    def set_brush_color(self,color):
        self.brush_color = color