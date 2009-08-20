from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from filters import *
from core.app.observer import *
from pyglet import clock

def customPaintLine(*largs, **kwargs):
    glBlendEquationSeparate(GL_FUNC_ADD, GL_MAX)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
            GL_ONE, GL_ONE)
    paintLine(*largs, **kwargs)
    glBlendEquationSeparate(GL_FUNC_ADD, GL_FUNC_ADD)
    
smudgev_shader_src = """
            void main()

            {
               gl_TexCoord[0] = gl_MultiTexCoord0;
               gl_Position = ftransform();
            }
"""

smudgef_shader_src = """
                    uniform sampler2D   tex;
                    uniform float direction;
                    uniform float kernel_size;
                    uniform float size_x ;
                    uniform float size_y ;
                    uniform float value;
                    void main (void) {
                        float rho = 10.0;
                        vec2 dir = direction < 0.5 ? vec2(1.0,0.0) : vec2(0.0,1.0);
                        vec4 orgcolor = texture2D(tex, gl_TexCoord[0].st);
    
                        float dx = 1.0 / size_x;
                        float dy = 1.0 / size_y;

                        vec2  st = gl_TexCoord [0].st;

                        vec4    color = vec4 (0.0, 0.0, 0.0, 0.0);
                        float   weight = 0.0;
                        for (float i = -1.0*kernel_size ; i <= kernel_size ; i+=1.0) {
                            float fac = exp (-(i * i) / (2.0 * rho * rho));
                            weight += fac;
                            color += texture2D (tex, st + vec2 (dx*i, dy*i) * dir) * fac;
                        }
                        float radius = 0.5;
                        
                        float point_dist = sqrt((0.5-gl_TexCoord[0].s)*(0.5-gl_TexCoord[0].s)+(0.5-gl_TexCoord[0].t)*(0.5-gl_TexCoord[0].t));
                        
                        if (point_dist  > 0.5) {
                            discard;
                        }                        
                        gl_FragColor =  orgcolor;//color / weight;
                    }
"""
       
erasev_shader_src = """
void main()

{
   gl_TexCoord[0] = gl_MultiTexCoord0;
   gl_Position = ftransform();
}
"""

erasef_shader_src = """
uniform sampler2D last_spot;
void main()
{
   vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
   float point_dist = sqrt((0.5-gl_TexCoord[0].s)*(0.5-gl_TexCoord[0].s)+(0.5-gl_TexCoord[0].t)*(0.5-gl_TexCoord[0].t));
   if (point_dist  > 0.5)
        discard;
   gl_FragColor = vec4(0,0,0,0.0);
}
"""

class AbstractLayer(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('layer_manager', None)
        self.layer_manager = kwargs.get('layer_manager')
        kwargs.setdefault('auto_bring_to_front', False)        
        super(AbstractLayer, self).__init__(**kwargs)
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)                
        self.color = (1,1,1,1)
        self.bgcolor = (1,1,1,1)
        self.layer_clear()
        self.id = kwargs.get('id')
        #self.smudge_shader = Shader(vertex_shader_src, fragment_shader_src)
        self.temp_tex = None
        self.erase_filter = Shader(erasev_shader_src, erasef_shader_src)
        
        self.smudge_filter = Shader(smudgev_shader_src, smudgef_shader_src)
        
        self.brush_fbo = Fbo(size=(16, 16), with_depthbuffer=False)
        self.erase_fbo = Fbo(size=(16, 16), with_depthbuffer=False)
        self.smudge_region = None
        self.erase_region = None
        self.ox,self.oy = 0,0
        
        self.order_done = True
        
    def layer_clear(self):
        with self.fbo:
            glClearColor(0, 0, 0, 0)
            glClear(GL_COLOR_BUFFER_BIT)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x,touch.y): 
            touches = getAvailableTouchs()
            if len(touches)==2 :               
                if touch.is_double_tap:
                    if self.order_done:
                        self.layer_manager.move_layer_down(self.id)
                        self.order_done = False
                        clock.schedule_once(self.reset_order_done, 0.25)
            elif touch.is_double_tap:
                if self.order_done:
                    self.layer_manager.move_layer_up(self.id)
                    self.order_done = False
                    clock.schedule_once(self.reset_order_done, 0.25)
            elif self.layer_manager.mode == "draw":
                self.ox,self.oy = touch.x,touch.y
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    customPaintLine((touch.x,touch.y,touch.x+1,touch.y+1), numsteps=1)
            elif self.layer_manager.mode == "zoom":
                super(AbstractLayer, self).on_touch_down(touch)
            elif self.layer_manager.mode == "erase":
                self.set_erase_fbo(self.to_local(touch.x,touch.y))
                self.erase(self.to_local(touch.x,touch.y))               
            elif self.layer_manager.mode == "smudge":
                self.set_brush_fbo(self.to_local(touch.x,touch.y))
                self.smudge(self.to_local(touch.x,touch.y))
            touch.grab(self)
            self.touches[touch.id] = Vector(touch.x, touch.y)
            return True
            
    def on_touch_move(self, touch):
        if touch.id in self.touches and touch.grab_current == self: 
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
            elif self.layer_manager.mode == "erase":
                self.set_erase_fbo(self.to_local(touch.x,touch.y))
                self.erase(self.to_local(touch.x,touch.y))
            elif self.layer_manager.mode == "smudge":
                self.set_brush_fbo(self.to_local(touch.x,touch.y))
                self.smudge(self.to_local(touch.x,touch.y))
            return True
            
    def reset_order_done(self,dt):
        self.order_done = True

    def getLayerManager(self):
        return self.layer_manager
        
    def set_brush_fbo(self, origin, location=(0,0)):
        x,y = map(int,origin)
        self.smudge_region = self.fbo.texture.get_region(x - 16, y - 16, 32, 32)
        with self.brush_fbo:
            set_color(1,1,1,1)
            drawTexturedRectangle(self.smudge_region, pos=(0,0), size=(32, 32))
    
    def set_erase_fbo(self, origin, location=(0,0)):
        x,y = map(int,origin)
        self.erase_region = self.fbo.texture.get_region(x - 8, y - 8, 16, 16)
        with self.erase_fbo:
            set_color(1,1,1,1)
            drawTexturedRectangle(self.erase_region, pos=(0,0), size=(16, 16))
        
    def smudge(self, origin, location=(0,0)):
        with self.fbo:
            self.smudge_filter.use()
            self.smudge_filter['size_x'] = 32.0
            self.smudge_filter['size_y'] = 32.0
            self.smudge_filter['kernel_size'] = 1.0
            self.smudge_filter['direction'] = 0.0
            set_color(1,1,1,1)
            drawTexturedRectangle(self.brush_fbo.texture, pos=(origin[0]-16,origin[1]-16), size=(32, 32))
            self.smudge_filter.stop()
            self.smudge_filter.use()
            self.smudge_filter['size_x'] = 32.0
            self.smudge_filter['size_y'] = 32.0
            self.smudge_filter['kernel_size'] = 1.0
            self.smudge_filter['direction'] = 1.0
            set_color(1,1,1,1)
            drawTexturedRectangle(self.brush_fbo.texture, pos=(origin[0]-16,origin[1]-16), size=(32, 32))
            self.smudge_filter.stop()
            
    def erase(self, origin, location=(0,0)):
        with self.fbo:
            self.erase_filter.use()
            set_color(1,1,1,1)
            drawTexturedRectangle(self.erase_fbo.texture, pos=(origin[0]-8,origin[1]-8), size=(16, 16))
            self.erase_filter.stop()
            

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
            
    def set_new_fbo_image(self,texture):
        with self.fbo:
            set_color(1, 1, 1, 1)
            drawTexturedRectangle(texture, (0,0),(self.width,self.height))
        
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
            kwargs.setdefault('auto_bring_to_front', False)
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
        drawTexturedRectangle(texture=self.fbo.texture, size=self.size)
        if self.moveable and self.highlight:
            set_color(0,0,1,0.5)
            drawRectangle(size=self.size)
