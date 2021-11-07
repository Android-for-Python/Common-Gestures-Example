from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from gestures4kivy import CommonGestures

### A gesture sensitive Label
###################################################

class GestureLabel(Label, CommonGestures):

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            Rectangle(pos=self.pos, size=self.size)
    
    def location(self, x, y):
        return 'x={} y={}'.format(round(x),round(y))

    def cg_tap(self, touch, x ,y):
        self.text = 'tap ' + self.location(x, y)

    def cg_two_finger_tap(self, touch, x, y):
        self.text = 'two finger tap ' + self.location(x,y)

    def cg_double_tap(self, touch, x, y):
        self.text = 'double tap ' + self.location(x,y)

    def cg_long_press(self, touch, x, y):
        self.text = 'long press or move\n' + self.location(x, y)
        
    def cg_long_press_end(self, touch, x, y):
        self.text = 'long press ' + self.location(x, y)
        
    def cg_move_to(self, touch, x, y, velocity):
        self.text = 'move to ' + self.location(x, y) +\
            '\nvelocity={}'.format(round(velocity))

    def cg_move_end(self, touch, x, y):
        self.text = 'move end ' + self.location(x, y)

    def cg_long_press_move_to(self, touch, x, y, velocity):
        self.text = 'long press move to\n' + self.location(x, y) +\
            '\nvelocity={}'.format(round(velocity))

    def cg_long_press_move_end(self, touch, x, y):
        self.text = 'long press move end\n' + self.location(x, y) 

    def cg_scale(self, touch0, touch1, scale, x, y):
        scale = round(scale * 1000) / 1000
        self.text = 'scale = {} centered\nat x={} y={}'.format(scale, round(x),
                                                              round(y))

    def cg_swipe_vertical(self, touch, bottom_to_top):
        self.text = 'swipe '
        if bottom_to_top:
            self.text += 'up'
        else:
            self.text += 'down'

    def cg_wheel(self, touch, scale, x, y):
        self.text = 'Scroll '
        if scale < 1:
            self.text += 'up'
        else:
            self.text += 'down'
        
    def cg_ctrl_wheel(self, touch, scale, x, y):
        self.text = 'Mouse wheel zoom '
        if scale < 1:
            self.text += 'out'
        else:
            self.text += 'in'

    def cg_shift_wheel(self, touch, scale, x, y):
        self.text = 'Scroll '
        if scale < 1:
            self.text += 'left'
        else:
            self.text += 'right'

    # Hide the notice of the move of zero pixels pre-empted by swipe
    def cg_move_start(self, touch, x, y):
        self._save = self.text

    def cg_swipe_horizontal(self, touch, left_to_right):
        self.text = self._save
