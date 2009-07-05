from __future__ import with_statement
from pymt import *
from pyglet.gl import *
from math import cos,sin,radians,pi,degrees
from glob import glob

class MTCircularItem(MTButton):
    def __init__(self, **kwargs):
        kwargs.setdefault('scale', 1.0)
        kwargs.setdefault('filename', None)
        if kwargs.get('filename') is None:
            raise Exception('No filename given to Item')
        super(MTCircularItem, self).__init__(**kwargs)
        self.action_handler = kwargs.get('handler')
        self.action_value = kwargs.get('value')
        self.filename		= kwargs.get('filename')
        self.scale          = kwargs.get('scale')
        self.image.scale    = self.scale
        self.size           = (self.image.width, self.image.height)
        self.x = self.x-self.width/2
        self.y = self.y-self.height/2
        self.image.x        = self.x
        self.image.y        = self.y
        
    def collide_point(self, x, y):
        if( x > self.x-self.width/2  and x < self.x+self.width/2 and
           y > self.y-self.height/2 and y < self.y+self.height/2  ):
            return True
        
    def on_press(self, touchID, x, y):
        self.action_handler(sprite=self.action_value,size=64)
        
    def _get_filename(self):
        return self._filename
        
    def _set_filename(self, filename):
        self._filename = filename
        img            = pyglet.image.load(filename)
        self.image     = pyglet.sprite.Sprite(img)
    filename = property(_get_filename, _set_filename)

    def on_draw(self):
        self.image.x        = self.x-self.width/2
        self.image.y        = self.y-self.height/2
        self.image.scale    = self.scale
        self.size           = (self.image.width, self.image.height)
        self.image.draw()

class MTCircularMenu(MTWidget):
    def __init__(self, **kwargs):
        super(MTCircularMenu, self).__init__(**kwargs)
        self.canvas = kwargs.get('canvas')
        self.pos = kwargs.get('pos')
        self.radius = kwargs.get('radius')
       
        kt = MTKinetic(velstop=5.0)
        self.circular_menu_render = MTCircularMenu_Render(pos=self.pos,radius=self.radius)
        kt.add_widget(self.circular_menu_render)
        self.add_widget(kt)        
        
                
        brush_list = []
        #by default generate a brushes list in circular menu        
        for brush in glob('brushes/*.png'):
            brush_list.append([brush,self.canvas.set_brush,brush])
            
        self.set_list(list=brush_list)
        
        
    def set_list(self,list):
        for item in list:
            im = MTCircularItem(filename=item[0],handler=item[1],value=item[2])
            self.circular_menu_render.add_widget(im)

class MTCircularMenu_Render(MTScatterWidget):
    def __init__(self, **kwargs):
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_rotation', True)
        kwargs.setdefault('do_translation', False)
        super(MTCircularMenu_Render, self).__init__(**kwargs)
        self.radius = kwargs.get('radius')
        self.size = (self.radius*2,self.radius*2)
        self.pos = kwargs.get('pos')
        super(MTCircularMenu_Render, self).init_transform(self.pos, 0, 1)
        
    def collide_point(self, x, y):
        return Vector(self.pos).distance((x, y)) <= self.radius
        
    def add_widget(self, widget, do_layout=True):
        super(MTCircularMenu_Render, self).add_widget(widget)
        self.need_layout = True
        if do_layout:
            self.do_layout()
            
    def do_layout(self):
        x = int((self.radius-40)*cos(radians(20*(len(self.children)-1))))
        y = int((self.radius-40)*sin(radians(20*(len(self.children)-1))))
        self.children[len(self.children)-1].x = x
        self.children[len(self.children)-1].y = y
                
    def rotate_zoom_move(self, touchID, x, y):
        # we definitly have one point
        p1_start = Vector(*self.touches[touchID])
        p1_now   = Vector(x, y)

        # if we have a second point, do the scale/rotate/move thing
        # find intersection between lines...the point around which to rotate
        intersect = Vector(self.pos)

        # compute rotation angle
        old_line = p1_start - intersect
        new_line = p1_now - intersect
        rotation = -1.0 * old_line.angle(new_line)

        scale = 1.0

        # just comnpute a translation component if we only have one point
        trans = p1_now - p1_start

        # apply to our transformation matrix
        self.apply_angle_scale_trans(rotation, scale, trans, intersect)

        # save new position of the current touch
        self.touches[touchID] = Vector(x,y)
        
    def draw(self):
        #set_color(0,1,0,1)
        #drawCircle((0,0), 10)
        set_color(*self.style.get('bg-color'))
        #drawRectangle((0,0),self.size)
        drawCircle((0,0), self.radius)
        #drawCircle(self.pos, self.radius-64)
        #drawTriangle(self.pos, w=40, h=100)
            
            
if __name__ == '__main__':
    w = MTWindow()
    cm = MTCircularMenu_Manager(pos=(0,0))
    w.add_widget(cm)  
    for i in range (12):
        teta = float((360/12)*i*(pi/180))
        x =  int(90*cos(teta))
        y =  int(90*sin(teta))
        im = MTImageButton(filename="../../../gfx/icons/flickr.png",pos=(x,y))
        cm.add_widget(im) 

    runTouchApp()

