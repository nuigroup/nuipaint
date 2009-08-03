from __future__ import with_statement
from pymt import *
import pyglet

default_vertex = """
void main()

{
   gl_TexCoord[0] = gl_MultiTexCoord0;
   gl_Position = ftransform();
}
"""

default_fragment = """
uniform sampler2D last_spot;
void main()
{
   vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
   gl_FragColor = mix(gl_FragColor, col, 1.0);
}
"""

class Filter:
    def __init__(self):
        self.shader = Shader(vertex_source=default_vertex, fragment_source=default_fragment)
        self.current_shader = 0
        self.fbo = Fbo(size=(512,512), with_depthbuffer=False)
        self.current_texture = None
        
    def blur(self,texture,texture_size,value):
        blurv_shader_src = """
            void main()

            {
               gl_TexCoord[0] = gl_MultiTexCoord0;
               gl_Position = ftransform();
            }
            """

        blurf_shader_src = """
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
        
        if self.current_shader != 1 :
            self.shader = Shader(vertex_source=blurv_shader_src, fragment_source=blurf_shader_src)
            self.current_shader = 1
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #horizontal pass
        with self.fbo:
            self.shader.use()
            #self.shader['value'] = value
            self.shader['size_x'] = float(texture_size[0])
            self.shader['size_y'] = float(texture_size[1])
            self.shader['kernel_size'] = value
            self.shader['direction'] = 0.0
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        #vertical pass
        with self.fbo:
            self.shader.use()
            #self.shader['value'] = value
            self.shader['size_x'] = float(texture_size[0])
            self.shader['size_y'] = float(texture_size[1])
            self.shader['kernel_size'] = value
            self.shader['direction'] = 1.0
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.fbo.texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
        
    def sharpen(self,texture,texture_size,value):
        sharpenv_shader_src = """
            void main() {

              gl_TexCoord[0] = gl_MultiTexCoord0;
              gl_Position = ftransform();

            }
        """

        sharpenf_shader_src = """
            #define KERNEL_SIZE 9

            float kernel[KERNEL_SIZE];

            uniform sampler2D colorMap;
            uniform float width;
            uniform float height;

            uniform float value;

            float step_w = value/width;
            float step_h = value/height;

            vec2 offset[KERNEL_SIZE];
                                     
            void main(void)
            {
               int i = 0;
               vec4 sum = vec4(0.0);
               
               offset[0] = vec2(-step_w, -step_h);
               offset[1] = vec2(0.0, -step_h);
               offset[2] = vec2(step_w, -step_h);
               
               offset[3] = vec2(-step_w, 0.0);
               offset[4] = vec2(0.0, 0.0);
               offset[5] = vec2(step_w, 0.0);
               
               offset[6] = vec2(-step_w, step_h);
               offset[7] = vec2(0.0, step_h);
               offset[8] = vec2(step_w, step_h);
               
               kernel[0] = -1.0; 	kernel[1] = -1.0;	kernel[2] = -1.0;
               kernel[3] = -1.0;	kernel[4] = 9.0;	kernel[5] = -1.0;
               kernel[6] = -1.0;   kernel[7] = -1.0;	kernel[8] = -1.0;
               
               
                for( i=0; i<KERNEL_SIZE; i++ )
                   {
                        vec4 tmp = texture2D(colorMap, gl_TexCoord[0].st + offset[i]);
                        sum += tmp * kernel[i];
                   }
              
               gl_FragColor = sum;
            }
        """
        
        if self.current_shader != 2 :
            self.shader = Shader(vertex_source=sharpenv_shader_src, fragment_source=sharpenf_shader_src)
            self.current_shader = 2
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['width'] = float(texture_size[0])
            self.shader['height'] = float(texture_size[1])
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture