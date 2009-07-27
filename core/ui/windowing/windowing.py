from __future__ import with_statement
from pymt import *
from pyglet.gl import *

iconPath = os.path.join('core','ui','windowing', 'icons','')

class MTInnerWindowContainer(MTRectangularWidget):
    def __init__(self, **kwargs):
        super(MTInnerWindowContainer, self).__init__(**kwargs)

    def add_on_key_press(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().add_on_key_press(*largs, **kwargs)
    def remove_on_key_press(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().remove_on_key_press(*largs, **kwargs)
    def get_on_key_press(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().get_on_key_press(*largs, **kwargs)

    def add_on_text(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().add_on_text(*largs, **kwargs)
    def remove_on_text(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().remove_on_text(*largs, **kwargs)
    def get_on_text(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().get_on_text(*largs, **kwargs)

    def add_on_text_motion(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().add_on_text_motion(*largs, **kwargs)
    def remove_on_text_motion(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().remove_on_text_motion(*largs, **kwargs)
    def get_on_text_motion(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().get_on_text_motion(*largs, **kwargs)

    def add_on_text_motion_select(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().add_on_text_motion_select(*largs, **kwargs)
    def remove_on_text_motion_select(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().remove_on_text_motion_select(*largs, **kwargs)
    def get_on_text_motion_select(self, *largs, **kwargs):
        return self.parent.parent.get_parent_window().get_on_text_motion_select(*largs, **kwargs)

class windowing(MTScatterWidget):
    def __init__(self, **kargs):
        super(windowing, self).__init__(**kargs)
        self.container = MTInnerWindowContainer(pos=(0,0), size=self.size, style={'bg-color':(0,0,0)})
        super(windowing, self).add_widget(self.container)
        self.control_scale = 0.75
        self.setup_controls()
        self.register_event_type('on_fullscreen')
        self.register_event_type('on_unfullscreen')

    def setup_controls(self):
        self.controls = MTWidget()

        self.btn_fullscreen = MTImageButton(filename=iconPath+'fullscreen.png', scale=self.control_scale, cls='innerwindow-fullscreen')
        self.btn_fullscreen.push_handlers(on_release=self.fullscreen)
        self.controls.add_widget(self.btn_fullscreen)

        self.btn_close = MTImageButton(filename=iconPath+'filesave.png', scale=self.control_scale, cls='innerwindow-close')
        self.btn_close.push_handlers(on_release=self.close)
        self.controls.add_widget(self.btn_close)

        self.update_controls()

    def fullscreen(self, *largs, **kwargs):
        self.dispatch_event('on_fullscreen')
        root_win = self.parent.get_parent_window()

        # save state for restore
        self.old_children = root_win.children
        self.old_size = self.size

        # set new children
        root_win.children = []
        root_win.add_widget(root_win.sim)
        root_win.add_widget(self.container)

        btn_unfullscreen = MTButton(pos=(root_win.width-50, root_win.height-50),
                                    size=(50,50), label='Back')
        btn_unfullscreen.push_handlers(on_release=self.unfullscreen)
        root_win.add_widget(btn_unfullscreen)
        self.size = root_win.size
        self.container.size = self.size

    def unfullscreen(self, *largs, **kwargs):
        # restore old widget
        root_win = self.parent.get_parent_window()
        root_win.children = self.old_children

        # reset container parent
        self.container.parent = self

        # set old size
        self.size = self.old_size
        self.container.size = self.size
        self.dispatch_event('on_unfullscreen')

    def close(self, touch):
        self.parent.remove_widget(self)

    def add_widget(self, w):
        self.container.add_widget(w)

    def remove_widget(self, w):
        self.container.remove_widget(w)

    def get_parent_window(self):
        return self.container

    def get_scaled_border(self):
        return self.style.get('border-width') * (1.0 / self.get_scale_factor())

    def update_controls(self):
        scaled_border = self.get_scaled_border()
        center_x = self.width / 2
        center_y = - scaled_border
        for button in self.controls.children:
            button.scale = self.control_scale / self.get_scale_factor()
        self.btn_fullscreen.pos = center_x - self.btn_fullscreen.width - 2, \
                                  center_y - self.btn_fullscreen.height / 2
        self.btn_close.pos = center_x + 2, center_y - self.btn_close.height / 2

    def on_touch_down(self, touch):
        touch.push()
        touch.x, touch.y = super(windowing, self).to_local(touch.x, touch.y)
        if self.controls.dispatch_event('on_touch_down', touch):
            touch.pop()
            touch.grab(self)
            return True
        touch.pop()

        if super(windowing, self).on_touch_down(touch):
            return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            touch.push()
            touch.x, touch.y = super(windowing, self).to_local(touch.x, touch.y)
            if self.controls.dispatch_event('on_touch_move', touch):
                touch.pop()
                return True
            touch.pop()
        return super(windowing, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.push()
            touch.x, touch.y = super(windowing, self).to_local(touch.x, touch.y)
            if self.controls.dispatch_event('on_touch_up', touch):
                touch.pop()
                return True
            touch.pop()
        return super(windowing, self).on_touch_up(touch)

    def collide_point(self, x, y):
        scaled_border = self.get_scaled_border()
        local_coords = super(windowing,self).to_local(x, y)
        left, right = -scaled_border, self.width + scaled_border * 2
        bottom,top = -scaled_border, self.height + scaled_border * 2
        if local_coords[0] > left and local_coords[0] < right \
           and local_coords[1] > bottom and local_coords[1] < top:
            return True
        else:
            return False

    def draw(self):
        # select color from number of touch
        if len(self.touches) == 0:
            set_color(*self.style.get('bg-color'))
        elif len(self.touches) == 1:
            set_color(*self.style.get('bg-color-move'))
        else:
            set_color(*self.style.get('bg-color-full'))

        # draw border
        scaled_border = self.get_scaled_border()
        self.update_controls()
        drawRoundedRectangle(
            pos=(-scaled_border, -scaled_border),
            size=(self.width+scaled_border*2, self.height+scaled_border*2))

        # draw control background
        control_width = self.btn_fullscreen.width + self.btn_close.width
        drawRectangle(
            pos=((self.width/2)-(scaled_border + control_width / 2), -scaled_border),
            size=(scaled_border*2 + control_width, -scaled_border))

    def on_draw(self):
        with gx_matrix:
            glMultMatrixf(self.transform_mat)

            self.draw()
            self.controls.dispatch_event('on_draw')

            # use stencil for container
            with gx_stencil:
                drawRectangle((0, 0), size=self.size)
                stencilUse()
                self.container.dispatch_event('on_draw')

    def on_move(self, x, y):
        # no move on children
        pass

    def on_resize(self, w, h):
        # no resize of children
        pass
    