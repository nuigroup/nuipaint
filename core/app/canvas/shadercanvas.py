from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from pyglet.image import ImageData

vertex_shader_src = """
void main()

{
   gl_TexCoord[0] = gl_MultiTexCoord0;
   gl_Position = ftransform();
}
"""

fragment_shader_src = """
uniform sampler2D last_spot;
void main()
{
   vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
   gl_FragColor = mix(gl_FragColor, col, 0.5);
}
"""

class Canvas(MTScatterWidget):
    def __init__(self, **kwargs):
        super(Canvas, self).__init__(**kwargs)
        self.width = 500
        self.height = 400
        self.fbo = Fbo(size=(self.width, self.height), with_depthbuffer=False)
        self.color = (0,1,0,1.0)
        set_brush('brushes/brush_particle.png')
        self.layer_clear()
        self.touch_positions = {}
        self.mode = "zoom"
        set_brush_size(25)
        self.brush_color=(0,0,0,1)
        #self.pixel_holder = (GLfloat * 3072)(0)
        self.smudge_shader = Shader(vertex_shader_src, fragment_shader_src)

    def layer_clear(self):
        self.fbo.bind()
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.fbo.release()

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x,y): 
            self.touch_positions[touchID] = self.to_local(x,y)            
            if self.mode == "draw":
                self.fbo.bind()
                set_color(*self.brush_color)
                drawCircle(pos=self.to_local(x,y), radius=1)            
                self.fbo.release()
            elif self.mode == "zoom":
                super(Canvas, self).on_touch_down(touches, touchID, x, y)
            elif self.mode == "smudge":
                self.smudge((self.touch_positions[touchID][0],self.touch_positions[touchID][1]))                
            return True
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.touch_positions.has_key(touchID):
            if self.mode == "zoom":
                super(Canvas, self).on_touch_move(touches, touchID, x, y)
            elif self.mode == "draw":
                cur_pos = self.to_local(x,y)
                ox,oy = self.touch_positions[touchID]
                self.fbo.bind()
                set_color(*self.brush_color)
                paintLine((ox,oy,cur_pos[0],cur_pos[1]))
                self.fbo.release()
                self.touch_positions[touchID] = self.to_local(x,y)
            return True

    def draw(self):
        with gx_matrix:
            glColor4f(1,1,1,1)
            drawRectangle((-6,-6),(self.width+12,self.height+12))
            glScaled(float(self.width)/500, float(self.height)/400, 2.0)            
            with gx_blending:
                drawTexturedRectangle(self.fbo.texture, (-6,-6),(self.width+12,self.height+12))

    def set_mode(self,mode):
        self.mode = mode
        
    def set_brush_color(self,color):
        self.brush_color = color
    
    def smudge(self, origin, location=(0,0)):
        x,y = map(int,origin)
        region = self.fbo.texture.get_region(x - 16, y - 16, 32, 32)
        with self.fbo:
            self.smudge_shader.use()
            drawTexturedRectangle(region, pos=origin, size=(32, 32))
            self.smudge_shader.stop()