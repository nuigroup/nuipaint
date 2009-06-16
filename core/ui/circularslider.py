from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import degrees,sqrt,acos,pi,cos,sin,radians

def drawSemiCircle(pos=(0,0), inner_radius=100,outer_radius=100,slices=32,loops=1,start_angle=0,sweep_angle=0):
    gluPartialDisk(gluNewQuadric(), inner_radius, outer_radius, slices, loops, start_angle,sweep_angle )

class MTCircularScroller(MTWidget): 
    def __init__(self, **kwargs):
        kwargs.setdefault('radius', 200)
        kwargs.setdefault('thickness', 40)
        kwargs.setdefault('padding', 3)
        kwargs.setdefault('sweep_angle', 90)
        super(MTCircularScroller, self).__init__(**kwargs)
        self.radius = kwargs.get('radius')        
        self.last_touch = (0, 0)
        self.angle = 0.0
        self.rotation = kwargs.get('rotation')
        self.radius_line = (int(self.radius*sin(radians(self.rotation))),int(self.radius*cos(radians(self.rotation))))
        self.thickness = kwargs.get('thickness')
        self.padding = kwargs.get('padding')
        self.sweep_angle = kwargs.get('sweep_angle')
        self.slider_fill_angle = 0.0
        self.slider_color = kwargs.get('slider_color')

    def collide_point(self, x, y):
        point_dist = Vector(self.pos).distance((x, y))
        return  point_dist<= self.radius and point_dist > self.radius-self.thickness

    def on_touch_down(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            prev_angle = self.slider_fill_angle
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()
            if self.angle<0:
                if 360+self.angle > self.sweep_angle: #If touch is beyond the bound of sliders area
                    self.slider_fill_angle = prev_angle
            else:
                if self.angle > self.sweep_angle:
                    self.slider_fill_angle = prev_angle
            return True
    
    def on_touch_up(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            pass            
            
    def on_touch_move(self, touches, touchID, x, y):
        if self.collide_point(x, y):
            prev_angle = self.slider_fill_angle
            self.last_touch = (x - self.pos[0], y - self.pos[1])
            self.calculate_angle()            
            if self.angle<0:
                if 360+self.angle > self.sweep_angle:     #If touch is beyond the bound of sliders area
                    self.slider_fill_angle = prev_angle
            else:
                if self.angle > self.sweep_angle:
                    self.slider_fill_angle = prev_angle
            
            return True
            
    def calculate_angle(self):
        self.angle = Vector(self.radius_line).angle(self.last_touch)
        if self.angle<0:
            self.slider_fill_angle = self.angle+360
        else:
            self.slider_fill_angle = self.angle
        #print self.slider_fill_angle
 
    def on_draw(self):
        with gx_matrix_identity:
            set_color(*self.style.get('bg-color'))
            glTranslated(self.pos[0], self.pos[1], 0)
            glRotatef(-self.rotation, 0, 0, 1)
            drawSemiCircle((0,0),self.radius-self.thickness,self.radius,32,1,0,self.sweep_angle)
            set_color(*self.slider_color)
            drawSemiCircle((0,0),self.radius-self.thickness+self.padding,self.radius-self.padding,32,1,0,self.slider_fill_angle)
            #drawTriangle(pos=(0, 0), w=40, h=100)


if __name__ == '__main__':
    w = MTWindow()
    cm = MTCircularScroller(pos=(w.width/2,w.height/2),radius=300,thickness=100,padding=5,sweep_angle=90,slider_color=(1,0,0,0.5),rotation=-45)
    w.add_widget(cm)
    
    cm2 = MTCircularScroller(pos=(w.width/2-100,w.height/2-100),radius=150,thickness=70,padding=5,sweep_angle=135,slider_color=(1,1,0,0.5),rotation=55)
    w.add_widget(cm2)
    
    cm3 = MTCircularScroller(pos=(300,200),radius=150,thickness=70,padding=5,sweep_angle=135,slider_color=(0,1,0,0.5),rotation=-55)
    w.add_widget(cm3)

    cm4 = MTCircularScroller(pos=(300,600),radius=200,thickness=70,padding=5,sweep_angle=360,slider_color=(0,0,1,0.5),rotation=0)
    w.add_widget(cm4)
    
    runTouchApp()


