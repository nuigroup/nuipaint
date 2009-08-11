from __future__ import with_statement
from pymt import *
from pyglet.gl import *

vertex_shader_src = """
void main()
{
   gl_TexCoord[0] = gl_MultiTexCoord0;
   //gl_TexCoord[1] = gl_MultiTexCoord1;
   gl_Position = ftransform();
}
"""

fragment_shader_src = """
    uniform sampler2D   tex;
    uniform float direction;
    uniform float kernel_size;
    uniform float size_x ;
    uniform float size_y ;
    uniform float value;
void main (void) {
    float rho = 10.0;
    vec2 dir = direction < 0.5 ? vec2(1.0,0.0) : vec2(0.0,1.0);

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
    gl_FragColor =  color / weight;
}
"""

fragment2_shader_src = """
uniform sampler2D last_spot;
void main()
{
   vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
   float or,og,ob,r,g,b,x,y;
   x = gl_TexCoord[0].s;
   y = gl_TexCoord[0].t;
   float rate = 0.5;
   or = col.r;
   og = col.g;
   ob = col.b;
   r = rate * or + (1.0 - rate) * or;
   g = rate * og + (1.0 - rate) * og;
   b = rate * ob + (1.0 - rate) * ob;
   vec4 finalColor = vec4(r,g,b,1.0);
   if (x < 0.5) {
        //vec4 finalColor = vec4(r,g,b,1.0);
   } else {
        vec4 finalColor = vec4(1.0,0.0,0.0,1.0);
   }
   
   /*
   float cv = 0.5;
   vec4 color0 = texture2D(last_spot, gl_TexCoord[0].st);  
   vec4 color1 = texture2D(last_spot, gl_TexCoord[1].st);
   vec4 color = vec4(color0 * cv + color1 * (1 - cv));
   */
   
   gl_FragColor = mix(gl_FragColor, finalColor, 1.0);
}
"""

class specialScatterW(MTScatterWidget):
    def __init__(self, **kwargs):
        super(specialScatterW, self).__init__(**kwargs)
    
    def on_touch_down(self, touch):
        x, y = touch.x, touch.y

        # if the touch isnt on the widget we do nothing
        if not self.collide_point(x, y):
            return False

        # let the child widgets handle the event if they want
        touch.push()
        touch.x, touch.y = self.to_local(x, y)
        if super(MTScatterWidget, self).on_touch_down(touch):
            touch.pop()
            return True
        touch.pop()

        # if the children didnt handle it, we bring to front & keep track
        # of touches for rotate/scale/zoom action
        touch.grab(self)
        #self.bring_to_front()
        self.touches[touch.id] = Vector(x, y)
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
        self.smudge_shader = Shader(vertex_shader_src, fragment_shader_src)
        self.temp_tex = None

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
            touches = getAvailableTouchs()
            self.touches[touch.id] = self.to_local(touch.x,touch.y)
            if len(touches)==2 :                
                if touch.is_double_tap:
                    self.layer_manager.move_layer_down(self.id)
            elif touch.is_double_tap:
               self.layer_manager.move_layer_up(self.id)
            if self.layer_manager.mode == "draw":
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((touch.x,touch.y,touch.x+1,touch.y+1))                    
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
                ox,oy = self.to_local(touch.x,touch.y)
                with self.fbo:
                    set_color(*self.layer_manager.brush_color)
                    set_brush(self.layer_manager.brush_sprite,self.layer_manager.brush_size)
                    paintLine((ox,oy,cur_pos[0],cur_pos[1]))                    
                self.touches[touch.id] = self.to_local(touch.x,touch.y)
            elif self.layer_manager.mode == "smudge":
                self.smudge(self.to_local(touch.x,touch.y))
                self.temp_tex = self.settemptex(self.to_local(touch.x,touch.y))
            return True
            
    #def on_touch_up(self, touch):
    #    if self.collide_point(touch.x,touch.y): 
    #        del self.touches[touch.id]
    #        return True
            
    def getLayerManager(self):
        return self.layer_manager
        
    def settemptex(self, origin, location=(0,0)):
        x,y = map(int,origin)
        return self.fbo.texture.get_region(x - 16, y - 16, 32, 32)
        
    def smudge(self, origin, location=(0,0)):
        x,y = map(int,origin)
        region = self.fbo.texture.get_region(x - 16, y - 16, 32, 32)
        with self.fbo:
            self.smudge_shader.use()
            self.smudge_shader['size_x'] = 32
            self.smudge_shader['size_y'] = 32
            self.smudge_shader['kernel_size'] = 3.0
            self.smudge_shader['direction'] = 0.0
            drawTexturedRectangle(self.temp_tex, pos=origin, size=(32, 32))
            drawTexturedRectangle(region, pos=origin, size=(32, 32))
            self.smudge_shader.stop()
         

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
        #self.need_redraw = True        

    def clearfbo(self):
        with self.fbo:
            glColor4f(1,1,1,1)
            drawRectangle(pos=(0,0),size=(self.width,self.height))
        
    def draw(self):
        #glColor4f(*self.color)
        #if self.need_redraw:
        #    self.clearfbo()
        #    self.need_redraw = False
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
        self.background = kwargs.get('file')
        img = pyglet.image.load(self.background)
        self.image  = pyglet.sprite.Sprite(img)
  
        
    def draw(self):
        with gx_matrix:
                self.image.draw()
                drawTexturedRectangle(self.fbo.texture, (0,0),(self.width,self.height))
 