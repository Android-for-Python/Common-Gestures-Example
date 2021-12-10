from kivy.app import App
from kivy.uix.screenmanager import Screen
from gestures4kivy import CommonGestures

### A swipe sensitive Screen, parent of all screen layouts
class SwipeScreen(Screen, CommonGestures):
    def cg_swipe_horizontal(self, touch, right):
        # one finger horizontal swipe
        App.get_running_app().swipe_screen(right)
