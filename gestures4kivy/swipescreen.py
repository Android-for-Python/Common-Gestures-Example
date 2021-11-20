from gestures4kivy.commongestures import CommonGestures

from kivy.app import App
from kivy.uix.screenmanager import Screen


# A swipe sensitive Screen, parent of all screen layouts
class SwipeScreen(Screen, CommonGestures):

    def cg_swipe_horizontal(self, touch, right):
        App.get_running_app().swipe_screen(right)
