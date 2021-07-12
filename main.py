from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import platform
from kivy.core.window import Window
from screens import Screen1, Screen2, Screen3, Screen4, Screen5

if platform == 'win':
    # Dispose of that nasty red dot on Windows
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')

class MyApp(App):
    def build(self):
        if platform == 'android':
            Window.bind(on_keyboard = self.inhibit_android_back_gesture)
        self.sm = ScreenManager()
        self.screens = [Screen1(name='1'),
                        Screen2(name='2'),
                        Screen3(name='3'),
                        Screen4(name='4'),
                        Screen5(name='5')]
        for s in self.screens:
            self.sm.add_widget(s)
        return self.sm

    # assumes screen names '1','2','3'....
    def swipe_screen(self, right):
        i = int(self.sm.current)
        if right:
            self.sm.transition.direction = 'right'
            self.sm.current = str(max(1,i-1))
        else:
            self.sm.transition.direction = 'left'
            self.sm.current = str(min(len(self.screens),i+1))

    # As a 'Android back gesture/button' example:
    # Inhibit the OS's 'back gesture/button' except on the app's home screen.
    def inhibit_android_back_gesture(self,window,key,*args):
        # The back button is not a keyboard a 'Back' it is a keyboard 'Esc'
        if key == 27 and self.sm.current != '1':
            # Android CAN NOT use the back button/gesture          
            # The user will still see the > or < animation
            # but the app pause behavior will not occur.
            return True   
        else:
            # Android CAN use the back button/gesture to pause the app
            return False  
    
MyApp().run()

