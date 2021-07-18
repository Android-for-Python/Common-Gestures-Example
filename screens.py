from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.utils import platform
from textwrap import fill

from swipescreen import SwipeScreen
from gesturelabel import GestureLabel
from gestureboxlayout  import GestureBoxLayout
from gesturecanvas import GestureCanvas
from zoomimage import ZoomImage

### SwipeScreen layouts

class Screen1(SwipeScreen):
    def __init__(self, **args):
        super().__init__(**args)
        self.label = Label()
        self.add_widget(self.label)

    def on_size(self, *args):
        mobile = platform == 'android' or platform == 'ios'
        if self.width > self.height:
            COLS = 80
        else:
            COLS = 40
        text='FIRST SCREEN.\n\n' +\
            fill('Swipe to the left to pull the next screen from the right.',
                 COLS) + '\n\n' +\
            fill('On the screens after this one you can also swipe right '+\
                 'to pull the previous screen.',COLS) + '\n\n' +\
            fill('There are five screens.',COLS) 
        if not mobile:
            text += '\n\n' +\
                fill('Mouse users hold the left button and ' +\
                     'swipe the mouse.',COLS) + '\n\n' +\
                fill('Touch pad users the swipe begins with ' +\
                     'a tap and a half, as usual.',COLS)
        self.label.text = text

class Screen2(SwipeScreen):
    def __init__(self, **args):
        super().__init__(**args)
        label = Label()
        box2 = BoxLayout(orientation='horizontal')
        box2.add_widget(Label())
        box2.add_widget(GestureLabel())
        box1 = BoxLayout(orientation='vertical')
        box1.add_widget(box2)
        box1.add_widget(label)
        self.add_widget(box1)
        self.label = label
        self.box1 = box1
        self.box2 = box2

    def on_size(self, *args):
        mobile = platform == 'android' or platform == 'ios'
        if mobile:
            COLS = 40
            if self.width > self.height:
                self.box1.orientation = 'horizontal'
                self.box2.orientation = 'vertical'
            else:
                self.box1.orientation = 'vertical'
                self.box2.orientation = 'horizontal'
        else:
            if self.width > self.height:
                COLS = 80
            else:
                COLS = 40

        text='SECOND SCREEN.\n\n' +\
            fill('The gesture sensitive widget is grey. In the grey area ' +\
                 'try a "tap", "double tap", "long press", "move", ' +\
                 '"long press move", "scale gesture" or "vertical swipe". ' +\
                 'A "long press move" begins with a "long press".', COLS) +\
                 '\n\n' +\
            fill('A horizonal swipe anywhere in the screen changes the ' +\
                 'screen, because of the SwipeScreen class.',COLS) + '\n\n' +\
            fill('The coordinates are widget coordinates.',COLS) 
        if not mobile:
            text += '\n' +\
                fill('Touch pad: like the "horizontal swipe", the ' +\
                     '"long press", "long press move", and "move" begin ' +\
                     'with a tap and a half. Mouse wheel: try "wheel", ' +\
                     '"ctrl-wheel", and "shift-wheel".',COLS)
        self.label.text = text


class Screen3(SwipeScreen):
    def __init__(self, **args):
        super().__init__(**args)
        self.box = GestureBoxLayout()
        self.add_widget(self.box)

    def on_size(self, *args):
        mobile = platform == 'android' or platform == 'ios'
        if mobile:
            COLS = 40
            if self.width > self.height:
                self.box.orientation = 'horizontal'
            else:
                self.box.orientation = 'vertical'
        else:
            if self.width > self.height:
                COLS = 80
            else:
                COLS = 40

        text = 'THIRD SCREEN.\n\n' +\
            fill('The whole screen is sensitive to gestures ' +\
                 'because in this case the gestures are bound to a Layout.',
                 COLS) + '\n\n' +\
            fill('Try the same gestures as before, the results of the ' +\
                 'gesture are displayed in a child Widget.',COLS) + '\n\n' +\
            fill('Coordinates are always of the touch sensitive area.',COLS)
        self.box.text = text

        
class Screen4(SwipeScreen):
    def __init__(self, **args):
        super().__init__(**args)
        self.label = Label()
        box = BoxLayout(orientation='vertical')
        box.add_widget(GestureCanvas())
        box.add_widget(self.label)
        self.add_widget(box)
        self.box = box

    def on_size(self, *args):
        mobile = platform == 'android' or platform == 'ios'
        if mobile:
            COLS = 40
            if self.width > self.height:
                self.box.orientation = 'horizontal'
            else:
                self.box.orientation = 'vertical'
        else:
            if self.width > self.height:
                COLS = 80
            else:
                COLS = 40
                
        text='FOURTH SCREEN.\n\n' +\
            fill('Use "long press move" and "zoom" to change items on a ' +\
                 'canvas.',COLS) + '\n\n'+\
            fill('Long press on the red box, wait for visual feedback ' +\
                 'then it can be dragged.', COLS) + '\n' +\
            fill('Visual feedback is helpful with long press.', COLS) +'\n\n' +\
            fill('Change the size of the box with a pinch/spread gesture ' +\
                 'centered on the box.',COLS)
        if not mobile:
            text += '\n' +\
                fill('Touch pad and mouse users, place the cursor on the ' +\
                     'box.',COLS) + '\n' +\
                fill('Mouse users use "ctrl-scroll wheel" to zoom.',COLS)
        self.label.text = text


class Screen5(SwipeScreen):
    def __init__(self, **args):
        super().__init__(**args)
        label = Label()  
        box = BoxLayout(orientation='vertical')
        box.add_widget(ZoomImage(source = 'test.jpg'))
        box.add_widget(label)
        self.add_widget(box)
        self.box = box
        self.label = label

    def on_size(self, *args):
        mobile = platform == 'android' or platform == 'ios'
        if mobile:
            COLS = 40
            if self.width > self.height:
                self.box.orientation = 'horizontal'
            else:
                self.box.orientation = 'vertical'
        else:
            self.label.size_hint_y = 0.4
            if self.width > self.height:
                COLS = 80
            else:
                COLS = 40
                
        text='LAST SCREEN.\n\n' +\
            fill('Zoom in using a spread gesture.Zoom out using a pinch ' +\
                 'gesture.',COLS) + '\n'+\
            fill('Pan using a move gesture.',COLS) +\
            '\n' +\
            fill('Double Tap to fully Zoom out.',COLS) + '\n' +\
            fill('Swipe right to see the previous screen.',COLS)
        if not mobile:
            text += '\n' +\
                fill('Mouse users use "ctrl-scroll wheel" to zoom, ' +\
                     '"shift-scroll wheel" to pan horizontally, and ' +\
                     '"scroll-wheel" to pan vertically',COLS)
        self.label.text = text

        
