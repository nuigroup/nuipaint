from __future__ import with_statement
from pymt import *
import pyglet

class Filter:
    def __init__(self):
        self.shader = None
        self.current_shader = 0
        self.fbo = None
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
         
        first_pass_fbo = Fbo(size=texture_size, with_depthbuffer=False)
        #horizontal pass
        with first_pass_fbo:
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
            drawTexturedRectangle(first_pass_fbo.texture, size=self.fbo.size)
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
        
    def brightness(self,texture,texture_size,value):
        brightnessv_shader_src = """
            void main() {
               gl_TexCoord[0] = gl_MultiTexCoord0;
               gl_Position = ftransform();
            }
        """
        
        brightnessf_shader_src = """
            uniform float value;
            uniform sampler2D last_spot;
            void main()
            {
               vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
               gl_FragColor = mix(gl_FragColor, col, value);
            }
        """
        
        if self.current_shader != 3 :
            self.shader = Shader(vertex_source=brightnessv_shader_src, fragment_source=brightnessf_shader_src)
            self.current_shader = 3
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
        
    def contrast(self,texture,texture_size,value):
        contrastv_shader_src = """
            void main() {
               gl_TexCoord[0] = gl_MultiTexCoord0;
               gl_Position = ftransform();
            }
        """
        
        contrastf_shader_src = """
            uniform float value;
            uniform sampler2D last_spot;
            void main()
            {
                vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
               
               // Increase or decrease theese values to adjust r, g and b color channels seperately
                const float AvgLumR = 0.5;
                const float AvgLumG = 0.5;
                const float AvgLumB = 0.5;
                const vec4 LumCoeff = vec4(0.2125, 0.7154, 0.0721, 1.0);
                
                vec4 AvgLumin = vec4(AvgLumR, AvgLumG, AvgLumB, 1.0);
                vec4 brtColor = col * 1.0;
                vec4 intensity = vec4(dot(brtColor, LumCoeff));
                vec4 satColor = mix(intensity, brtColor, 1.0);
                vec4 conColor = mix(AvgLumin, satColor, value);
                
               gl_FragColor = mix(gl_FragColor, conColor, 1.0);
            }

        """
        
        if self.current_shader != 4 :
            self.shader = Shader(fragment_source=contrastf_shader_src)
            self.current_shader = 4
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
        
    def saturation(self,texture,texture_size,value):
        saturationf_shader_src = """
            uniform float value;
            uniform sampler2D last_spot;
            void main()
            {
                vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
               
               // Increase or decrease theese values to adjust r, g and b color channels seperately
                const float AvgLumR = 0.5;
                const float AvgLumG = 0.5;
                const float AvgLumB = 0.5;
                const vec4 LumCoeff = vec4(0.2125, 0.7154, 0.0721, 1.0);
                
                vec4 AvgLumin = vec4(AvgLumR, AvgLumG, AvgLumB, 1.0);
                vec4 brtColor = col * 1.0;
                vec4 intensity = vec4(dot(brtColor, LumCoeff));
                vec4 satColor = mix(intensity, brtColor, value);
                
               gl_FragColor = mix(gl_FragColor, satColor, 1.0);
            }

        """
        
        if self.current_shader != 5 :
            self.shader = Shader(fragment_source=saturationf_shader_src)
            self.current_shader = 5
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
        
    def bw(self,texture,texture_size,value):
        bwf_shader_src = """
            uniform float value;
            uniform sampler2D last_spot;
            void main()
            {
                vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
                float or,og,ob,r,g,b;
                or = col.r;
                og = col.g;
                ob = col.b;
                
                r = (or * 0.3086 + og * 0.6094 + ob * 0.0820);
				g = (or * 0.3086 + og * 0.6094 + ob * 0.0820);
				b = (or * 0.3086 + og * 0.6094 + ob * 0.0820);

                vec4 finalColor = vec4(r,g,b,1.0);       
                gl_FragColor = mix(gl_FragColor, finalColor, 1.0);
            }

        """
        
        if self.current_shader != 6 :
            self.shader = Shader(fragment_source=bwf_shader_src)
            self.current_shader = 6
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
    
    def sepia(self,texture,texture_size,value):
        sepiaf_shader_src = """
            uniform float value;
            uniform sampler2D last_spot;
            void main()
            {
                vec4 col = texture2D(last_spot, gl_TexCoord[0].st);
                float or,og,ob,r,g,b;
                or = col.r;
                og = col.g;
                ob = col.b;
                
                r = (or * 0.393 + og * 0.769 + ob * 0.189);
				g = (or * 0.349 + og * 0.686 + ob * 0.168);
				b = (or * 0.272 + og * 0.534 + ob * 0.131);

                vec4 finalColor = vec4(r,g,b,1.0);       
                gl_FragColor = mix(gl_FragColor, finalColor, 1.0);
            }

        """
        
        if self.current_shader != 7 :
            self.shader = Shader(fragment_source=sepiaf_shader_src)
            self.current_shader = 7
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        #run glsl code
        with self.fbo:
            self.shader.use()
            self.shader['value'] = value
            set_color(1, 1, 1)
            drawTexturedRectangle(self.current_texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture
        
    def circularblur(self,texture,texture_size,value):
        blurv_shader_src = """
            varying vec3 position;
            void main()

            {
               gl_TexCoord[0] = gl_MultiTexCoord0;
               position = vec3(gl_MultiTexCoord0 - 0.5) * 5.0;
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
                    varying vec3 position;
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
                        
                        if (point_dist  < 0.5) {
                            gl_FragColor =  color / weight;
                        }                        
                        else
                        {
                            gl_FragColor =  vec4(0,0,0,0.0);//vec4(1,0,0,0.0);
                        }
                    }
            """
        
        if self.current_shader != 8 :
            self.shader = Shader(vertex_source=blurv_shader_src, fragment_source=blurf_shader_src)
            self.current_shader = 8
            
        if self.current_texture != texture :    
            self.current_texture = texture
            self.fbo = Fbo(size=texture_size, with_depthbuffer=False)
            
        first_pass_fbo = Fbo(size=texture_size, with_depthbuffer=False)
        #horizontal pass
        with first_pass_fbo:
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
            drawTexturedRectangle(first_pass_fbo.texture, size=self.fbo.size)
            self.shader.stop()
            
        return self.fbo.texture