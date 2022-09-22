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
                 'try a "primary event", "secondary event", "select", ' +\
                 '"drag", "scroll", "zoom", or "rotate". ', COLS) +\
                 '\n\n' +\
            fill('The coordinates are widget coordinates.',COLS) 
        if not mobile:
            if platform == 'macosx':
                text += '\n\n' +\
                    fill('MacOS: Zoom is Cmd-scroll, rotate is Option-scroll.',
                         COLS)
            else:
                text += '\n\n' +\
                    fill('Mouse: Zoom is Ctrl-wheel, rotate is Alt-wheel.',
                         COLS) + '\n' +\
                    fill('Touchpad: Rotate is Alt-scroll.',
                         COLS)
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
                
        text='FOURTH SCREEN.\n\n'
        if not mobile:
            text += (fill('Move the cursor inside the box to ' +\
                          'drag, zoom, or rotate the box.', COLS) + '\n')
            text += fill('Mouse users use "Ctrl-scroll wheel" to zoom.',COLS)
            text += fill('Use "Alt-scroll" to rotate.',COLS)            
        else:
            text += fill('Drag, zoom, or rotate the box.', COLS) + '\n'
            text += fill('To rotate, twist two fingers around the box.',
                         COLS)
            text += fill('To drag, long press and wait for the blue ' +\
                         'circle, then move finger.', COLS)
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
            fill('Zoom, scroll, and (slowly) pan the image.',COLS) + '\n'+\
            fill('Double Tap or long press to fully zoom out.',COLS) + '\n' +\
            fill('Swipe right to see the previous screen.',COLS)
        if not mobile:
            text += '\n' +\
                fill('Mouse users use "ctrl-scroll wheel" to zoom, ' +\
                     '"shift-scroll wheel" to pan, and ' +\
                     '"scroll-wheel" to scroll.',COLS)
        self.label.text = text

        
