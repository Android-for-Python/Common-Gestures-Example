from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from commongestures import CommonGestures

### A gesture sensitive BoxLayout
###################################################

class GestureBoxLayout(CommonGestures, BoxLayout):

    def __init__(self, **args):
        super().__init__( **args)
        self.text = ''
        self.orientation='vertical'
        self.label0 = Label()
        self.label1 = Label()
        self.add_widget(self.label0)
        self.add_widget(self.label1)
    
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            Rectangle(pos=self.pos, size=self.size)
        self.label1.text = self.text

    def location(self, x, y):
        return ' x={} y={}'.format(round(x),round(y))

    def cg_tap(self, touch, x, y):
        self.label0.text = 'tap' + self.location(x,y)

    def cg_two_finger_tap(self, touch, x, y):
        self.label0.text = 'two finger tap' + self.location(x,y)

    def cg_double_tap(self, touch, x, y):
        self.label0.text = 'double tap' + self.location(x,y)

    def cg_long_press(self, touch, x, y):
        self.label0.text = 'long press or move\n' + self.location(x, y)

    def cg_long_press_end(self, touch, x, y):
        self.label0.text = 'long press\n' + self.location(x, y)

    def cg_long_press_move_to(self, touch, x, y, velocity):
        self.label0.text = 'long press move to\n' + self.location(x,y) +\
            '\nvelocity={}'.format(round(velocity))

    def cg_long_press_move_end(self, touch, x, y):
        self.label0.text = 'long press move to\n' + self.location(x,y)

    def cg_move_to(self, touch, x, y, velocity):
        self.label0.text = 'move to' + self.location(x,y) +\
            '\nvelocity={}'.format(round(velocity))

    def cg_move_end(self, touch, x, y):
        self.label0.text = 'move end' + self.location(x,y) 

    def cg_scale(self, touch0, touch1, scale, x, y):
        scale = round(scale * 1000) / 1000
        self.label0.text = 'scale = {} centered\nat x={} y={}'.format(scale,
                                                                      round(x),
                                                                      round(y))
    def cg_swipe_vertical(self, touch, bottom_to_top):
        self.label0.text = 'swipe '
        if bottom_to_top:
            self.label0.text += 'up'
        else:
            self.label0.text += 'down'

    def cg_wheel(self, touch, scale, x, y):
        self.label0.text = 'Scroll '
        if scale < 1:
            self.label0.text += 'up'
        else:
            self.label0.text += 'down'

    def cg_ctrl_wheel(self, touch, scale, x, y):
        self.label0.text = 'Mouse wheel zoom '
        if scale < 1:
            self.label0.text += 'out'
        else:
            self.label0.text += 'in'

    def cg_shift_wheel(self, touch, scale, x, y):
        self.label0.text = 'Scroll '
        if scale < 1:
            self.label0.text += 'left'
        else:
            self.label0.text += 'right'

    # Hide the notice of the move of zero pixels pre-empted by swipe
    def cg_move_start(self, touch, x, y):
        self._save = self.label0.text

    def cg_swipe_horizontal(self, touch, left_to_right):
        self.label0.text = self._save
