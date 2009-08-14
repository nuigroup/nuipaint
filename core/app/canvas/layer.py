from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from filters import *
from core.app.observer import *

def customPaintLine(*largs, **kwargs):
    glBlendEquationSeparate(GL_FUNC_ADD, GL_MAX)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
            GL_ONE, GL_ONE)
    paintLine(*largs, **kwargs)
    glBlendEquationSeparate(GL_FUNC_ADD, GL_FUNC_ADD)
       
class AbstractLayer(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.layer_manager = kwargs.get('layer_manager')        
        super(AbstractLayer, self).__init__(**kwargs)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)                
        self.color = (1,1,1,1)
        self.bgcolor = (1,1,1,1)
        self.layer_clear()
        self.id = kwargs.get('id')
        #self.smudge_shader = Shader(vertex_shader_src, fragment_shader_src)
        self.temp_tex = None
        self.filter = Filter()
        
        self.brush_fbo = Fbo(size=(16, 16), with_depthbuffer=False)
        self.smudge_region = None
        self.ox,self.oy = 0,0
    def layer_clear(self):
        with self.fbo:
            glClearColor(0, 0, 0, 0)
            glClear(GL_COLOR_BUFFER_BIT)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y): 
            touches = getAvailableTouchs()
            if len(touches)==2 :                
                if touch.is_double_tap:
                    self.layer_manager.move_layer_down(self.id)
            elif touch.is_double_tap:
               self.layer_manager.move_layer_up(self.id)
            if self.layer_manager.mode == "draw":
                self.ox,self.oy = touch.x,touch.y
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    customPaintLine((touch.x,touch.y,touch.x+1,touch.y+1), numsteps=1)
            elif self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_down(touch)
            elif self.layer_manager.mode == "smudge":
                self.temp_tex = self.settemptex(self.to_local(touch.x,touch.y)) 
            return True
            
    def on_touch_move(self, touch):
        if self.collide_point(touch.x,touch.y): 
            if self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_move(touch)
            elif self.layer_manager.mode == "draw":
                cur_pos = self.to_local(touch.x,touch.y)
                ox, oy = self.ox, self.oy
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    numsteps = Vector(ox, oy).distance(Vector(cur_pos[0], cur_pos[1]))
                    customPaintLine((ox,oy,cur_pos[0],cur_pos[1]), numsteps=int(numsteps))
                self.ox,self.oy = cur_pos
            elif self.layer_manager.mode == "smudge":
                self.set_brush_fbo(self.to_local(touch.x,touch.y))
                self.smudge(self.to_local(touch.x,touch.y))
                self.temp_tex = self.settemptex(self.to_local(touch.x,touch.y))
            return True

    def getLayerManager(self):
        return self.layer_manager
        
    def settemptex(self, origin, location=(0,0)):
        x,y = map(int,origin)
        return self.fbo.texture.get_region(x - 16, y - 16, 3, 32)
        
    def set_brush_fbo(self, origin, location=(0,0)):
        x,y = map(int,origin)
        self.smudge_region = self.fbo.texture.get_region(x - 8, y - 8, 16, 16)
        with self.brush_fbo:
            drawTexturedRectangle(self.smudge_region, pos=origin, size=(32, 32))
        
    def smudge(self, origin, location=(0,0)):
        with self.brush_fbo:
            alt = self.filter.circularblur(self.smudge_region,(16,16),0.5)        
        with self.fbo:
            drawTexturedRectangle(alt, pos=origin, size=(16, 16))
            

class NormalLayer(AbstractLayer):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.moveable = kwargs.get('moveable')
        if self.moveable == False :
            kwargs.setdefault('do_scale', False)
            kwargs.setdefault('do_rotation', False)
            kwargs.setdefault('do_translation', False)
            kwargs.setdefault('auto_bring_to_front', False)
        super(NormalLayer, self).__init__(**kwargs)
        self.highlight =  False

    def clearfbo(self):
        with self.fbo:
            set_color(1, 1, 1, 1)
            drawRectangle(pos=(0,0),size=(self.width,self.height))
        
    def draw(self):
        drawTexturedRectangle(texture=self.fbo.texture, size=self.size)
        if self.moveable and self.highlight:
            set_color(0,0,1,0.5)
            drawRectangle(size=self.size)

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
        if kwargs.get('file'):
            self.background = kwargs.get('file')
        else:
            self.background = "brushes/brush_particle.png"
        img = pyglet.image.load(self.background)
        self.tex  = img.get_texture()
        self.size = (self.width,self.height)
        with self.fbo:
            set_color(1, 1, 1, 1) 
            drawTexturedRectangle(self.tex, (0,0),(self.width,self.height))
  
    def set_new_fbo_image(self,texture):
        with self.fbo:
            set_color(1, 1, 1, 1)
            drawTexturedRectangle(texture, (0,0),(self.width,self.height))
    
    def draw(self):
        with gx_matrix:
            set_color(1, 1, 1, 1) 
            drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
