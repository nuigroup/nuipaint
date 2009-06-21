from __future__ import with_statement
from pymt import *
from pyglet.gl import *

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
                self.do_smudge(self.touch_positions[touchID][0],self.touch_positions[touchID][1])
                #pass
                #glReadPixels(x, y, 32, 32, GL_RGB, GL_FLOAT, self.pixel_holder)
                #self.do_smudge(x,y,self.pixel_holder)
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
    
    def do_smudge(self, x, y):
        # First, extract region from texture
        region = self.fbo.texture.get_region(int(x) - 16, int(y) - 16, 32, 32)
        data = region.get_image_data()
        data.save(file="test.png")        
        # Extract pixels                
        format = 'RGBA'
        pitch = 32 * 4       
        pixels = data.get_data(format, pitch)
        data.save(file="test.png")
        
        rate = 0.5

        # Initialize state for smudge
        if not hasattr(self, 'state_smudge'):
            self.state_smudge = {}
            self.state_smudge_pitch = 32 * 3
            for i in xrange(0, 32 * 32 * 3):
                self.state_smudge[i] = 0

        # Do smudge
        for i in xrange(0, 32 * 32):
            iy = i >> 5
            ix = i & 0x1f

            # Change pixel only in the circle with 16 pixel diameter
            if ((ix - 16) * (ix - 16) + (iy - 16) * (iy - 16) > 120):
                continue

            # Get color
            r = pixels[ix + iy * pitch]
            g = pixels[ix + iy * pitch + 1]
            b = pixels[ix + iy * pitch + 2]

            # Update state
            state[ix + iy * self.state_smudge_pitch] =\
                rate * state[ix + iy * self.state_smudge_pitch] + (1.0 - rate) * r;
            state[ix + iy * self.state_smudge_pitch + 1] =\
                rate * state[ix + iy * self.state_smudge_pitch + 2] + (1.0 - rate) * g;
            state[ix + iy * self.state_smudge_pitch + 2] =\
                rate * state[ix + iy * self.state_smudge_pitch + 2] + (1.0 - rate) * b;

            # Put pixels
            pixels[ix + iy * pitch] = state[ix + iy * self.state_smudge_pitch]
            pixels[ix + iy * pitch + 1] = state[ix + iy * self.state_smudge_pitch + 1]
            pixels[ix + iy * pitch + 2] = state[ix + iy * self.state_smudge_pitch + 2]

        # Construct a texture from the new pixels
        data.set_data(format, pitch, pixels)
        texture = data.get_texture()

        # Draw texture on Fbo
        with self.fbo:
            drawTexturedRectangle(texture, pos=(x - 16, y - 16), size=(32, 32))

    """def do_smudge(self,x,y,buffer):
        temp = (GLfloat * 3072)(0)
        rate=0.5
        for i in range(3027,0,-3):
            iy = i >> 5;
            ix = i & 0x1f;
            # is it not on the circle of radius sqrt(120) at location 16,16?
            #if ((ix - 16) * (ix - 16) + (iy - 16) * (iy - 16) > 120):
            #    print i            
            #continue
            
            # it is on the circle, so grab it        
            temp[i-3] = rate * temp[i-3] + (1.0 - rate) * buffer[i-3]            
            temp[i-2] = rate * temp[i-2] + (1.0 - rate) * buffer[i-2]
            temp[i-1] = rate * temp[i-1] + (1.0 - rate) * buffer[i-1]

        self.fbo.bind()
  
        self.fbo.release()
            

        
    // opacity 100% --> new data not blended w/ existing data
    api->putpixel(canvas, x + ix - 16, y + iy - 16,
             SDL_MapRGB(canvas->format, api->linear_to_sRGB(state[ix][iy][0]),
                        api->linear_to_sRGB(state[ix][iy][1]),
                        api->linear_to_sRGB(state[ix][iy][2])));
  }"""
        