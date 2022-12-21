from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.utils import platform
from gestures4kivy import CommonGestures

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

    def set_label(self, text, x, y):
        self.label0.text = '{}\nFocus x={} y={}'.format(text,round(x),round(y))

    def cgb_primary(self, touch, focus_x, focus_y):
        self.set_label('Primary Event',focus_x, focus_y)

    def cgb_secondary(self, touch, focus_x, focus_y):
        self.set_label('Secondary Event',focus_x, focus_y)

    def cgb_select(self, touch, focus_x, focus_y, long_press):
        self.set_label('Select',focus_x, focus_y)

    def cgb_long_press_end(self, touch, focus_x, focus_y):
        self.set_label('Long Press End', focus_x, focus_y)

    def cgb_drag(self, touch, focus_x, focus_y, delta_x, delta_y):
        self.set_label('Drag',focus_x, focus_y)

    def cgb_scroll(self, touch, focus_x, focus_y, delta_y, velocity):
        self.set_label('Scroll',focus_x, focus_y)
        self.label0.text += '\ndelta y={}'.format(round(delta_y))
        self.label0.text += '\nvelocity={}'.format(round(velocity))

    def cgb_pan(self, touch, focus_x, focus_y, delta_y, velocity):
        if platform in ['android', 'ios']:
            # Can disambiguate between swipe and pan 
            self.set_label('Pan',focus_x, focus_y)
            self.label0.text += '\ndelta y={}'.format(round(delta_y))
            self.label0.text += '\nvelocity={}'.format(round(velocity))

    def cgb_zoom(self, touch0, touch1, focus_x, focus_y, delta_scale):
        self.set_label('Zoom',focus_x, focus_y)
        fmt = round(delta_scale * 1000)/1000
        self.label0.text += '\ndelta scale={}'.format(fmt)

    def cgb_rotate(self, touch0, touch1, focus_x, focus_y, delta_angle):
        if platform in ['android', 'ios']:
            self.label0.text += '{}\nFocus x={} y={}'.format('\n\nRotate',
                                                             round(focus_x),
                                                             round(focus_y))
        else:
            self.set_label('Rotate',focus_x, focus_y)
        fmt = round(delta_angle * 1000)/1000
        self.label0.text += '\ndelta angle={}'.format(fmt)

        
