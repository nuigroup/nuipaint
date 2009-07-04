from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from numpy import *
import string

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
                set_brush('brushes/brush_particle.png')
                set_brush_size(25)
                drawCircle(pos=self.to_local(x,y), radius=1)            
                self.fbo.release()
            elif self.mode == "zoom":
                super(Canvas, self).on_touch_down(touches, touchID, x, y)
            elif self.mode == "smudge":
                self.do_smudge(self.touch_positions[touchID][0],self.touch_positions[touchID][1])

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
                set_brush('brushes/brush_particle.png')
                set_brush_size(25)
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
        # Extract pixels                
        format = 'RGB'
        pitch = 32 * len(format)       
        pixel_data = data.get_data(format, pitch)
        pixels_list = map(ord, list(pixel_data))
		
        pixels = zeros((32,32,3), float)
        z = 0
        for i in range(0,31):
            for j in range(0,31):
                for k in range(0,2):
                    pixels[i,j,k] = pixels_list[z]
                    z += 1				
        #work
        state=zeros((32,32,3), float)
        rate = 0.5
        
        #i = 32 * 32;
        for i in range (32*32,0,-1) :
            iy = i >> 5
            ix = i & 0x1f
            # is it not on the circle of radius sqrt(120) at location 16,16?
            if (ix - 16) * (ix - 16) + (iy - 16) * (iy - 16) > 120 :
                continue
            # it is on the circle, so grab it
            
            # Get color
            r = float(pixels[ix,iy,0])/float(255)
            g = float(pixels[ix,iy,1])/float(255)
            b = float(pixels[ix,iy,02])/float(255)
            #print r,g,b
			
            state[ix,iy,0] = rate * state[ix,iy,0] + (1.0 - rate) * r
            state[ix,iy,1] = rate * state[ix,iy,1] + (1.0 - rate) * g
            state[ix,iy,2] = rate * state[ix,iy,2] + (1.0 - rate) * b
        
        #put back pixel
        z = 0
        for i in range(0,31):
            for j in range(0,31):
                for k in range(0,2):
                    pixels_list[z] = pixels[i,j,k]
                    z += 1
					
        data.set_data(format, pitch, ''.join(map(chr, pixels_list)))
        texture = data.get_texture()

        # Draw texture on Fbo
        with self.fbo:
            drawTexturedRectangle(texture, pos=(x - 16, y - 16), size=(32, 32))    
    
    
        