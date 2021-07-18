########################################################################
#
# Common Gestures
#
# Detects the common gestures for `scale`, `move`, `swipe`, `long press`,
# `long press move`, `tap`, and `double tap`.
# A `long press move move` is initiated with a `long press`. 
# On the desktop it also detects `mouse wheel` and the touchpad equivalent
# `two finger move`.
#
# These gestures can be **added** to Kivy widgets by subclassing a
# Kivy Widget and `CommonGestures`, and then including the methods for
# the required gestures.
#
# CommonGestures methods detect gestures, and do not define behaviors.
#
# Source https://github.com/Android-for-Python/Common-Gestures-Example
#
###########################################################################


from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.metrics import Metrics
from kivy.config import Config
from kivy.utils import platform
from functools import partial
from time import time
from math import sqrt

class CommonGestures(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mobile = platform == 'android' or platform == 'ios'
        if not mobile:
            Window.bind(on_key_down=self._ctrl_key_down)
            Window.bind(on_key_down=self._shift_key_down)
            Window.bind(on_key_up=self._key_up)
        self._CTRL = False
        self._SHIFT = False
        self._new_gesture()
        #### Sensitivity
        self._DOUBLE_TAP_TIME     = Config.getint('postproc',
                                                  'double_tap_time') / 1000
        self._DOUBLE_TAP_DISTANCE = Config.getint('postproc',
                                                  'double_tap_distance')
        self._LONG_PRESS          = 0.4                 # sec, convention
        self._MOVE_VELOCITY_SAMPLE = 0.2                # sec
        self._SWIPE_TIME          = 0.1                 # sec 
        self._SWIPE_VELOCITY      = 10                  # inches/sec, heuristic
        self._WHEEL_SENSITIVITY   = 1.1                 # heuristic

    #####################
    # Kivy Touch Events
    #####################

    ### touch down ###
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._touches.append(touch)
            if touch.is_mouse_scrolling:
                self._gesture_state = 'Wheel'
                scale = self._WHEEL_SENSITIVITY
                if touch.button == 'scrollup':
                    scale = 1/scale
                x, y = self._touch_to_widget(touch)
                if self._CTRL:
                    self.cg_ctrl_wheel(touch,scale, x, y)
                elif self._SHIFT:
                    self.cg_shift_wheel(touch,scale, x, y)
                else:
                    self.cg_wheel(touch,scale, x, y)

            elif len(self._touches) == 1:
                self._gesture_state = 'Dont Know' 
                # schedule a posssible long press
                self._long_press_schedule =\
                    Clock.schedule_once(partial(self._long_press_event, touch),
                                        self._LONG_PRESS)
                # schedule a posssible tap 
                if not self._single_tap_schedule:
                    self._single_tap_schedule =\
                        Clock.schedule_once(partial(self._single_tap_event,
                                                    touch),
                                            self._DOUBLE_TAP_TIME)
            elif len(self._touches) == 2:
                self._gesture_state = 'Scale'
                # If two fingers it cant be a long press, swipe or tap
                self._not_long_press() 
                self._not_single_tap()
                self._not_swipe()
                x, y = self._scale_to_widget(self._touches[0], self._touches[1])
                self.cg_scale_start(self._touches[0],self._touches[1], x, y)

        return super().on_touch_down(touch)

    ### touch move ###
    def on_touch_move(self, touch):
        if touch in self._touches:
            if touch.dx or touch.dy:
                # If moving it cant be a pending long press or tap
                self._not_long_press()
                self._not_single_tap() 
                # State changes
                if self._gesture_state == 'Long Pressed':
                    self._gesture_state = 'Long Press Move'
                    x, y = self._touch_down_to_widget(touch)
                    self._start_velocity_clock(touch)
                    self.cg_long_press_move_start(touch, x, y)

                elif self._gesture_state == 'Dont Know':
                    # possible pre-empt as swipe
                    self._swipe_schedule =\
                        Clock.schedule_once(partial(self._possible_swipe,
                                                    touch,  time()),
                                            self._SWIPE_TIME)
                    self._gesture_state = 'Move' 
                    x, y = self._touch_down_to_widget(touch)
                    self._start_velocity_clock(touch)
                    self.cg_move_start(touch, x, y)

                # Callback updates
                if self._gesture_state == 'Scale' and len(self._touches) > 1:
                    touch0 = self._touches[0]
                    touch1 = self._touches[1]
                    finger_distance = touch0.distance(touch1)
                    if self._finger_distance:
                        scale = finger_distance / self._finger_distance
                        if abs(scale) != 1:
                            x, y = self._scale_to_widget(touch0, touch1)
                            # use the focus for collide point test
                            # (so fat fingers can be outside the widget)
                            if x > 0 and x < self.width and\
                               y > 0 and y < self.height:
                                self.cg_scale(touch0,touch1,scale, x, y)
                    self._finger_distance = finger_distance

                elif self.collide_point(*touch.pos):
                    x, y = self._touch_to_widget(touch)
                    if self._gesture_state == 'Move':
                        self.cg_move_to(touch, x, y, self._velocity)
                        
                    elif self._gesture_state == 'Long Press Move':
                        self.cg_long_press_move_to(touch, x, y, self._velocity)
                        
        return super().on_touch_move(touch)                    

    ### touch up ###
    def on_touch_up(self, touch):
        if touch in self._touches:
            self._not_long_press()
            self._not_swipe()
            x, y = self._touch_to_widget(touch)

            if self._gesture_state == 'Dont Know':
                if touch.is_double_tap:
                    self._not_single_tap()
                    self.cg_double_tap(touch, x, y)
                    self._new_gesture()
                else:
                    self._remove_gesture(touch)

            elif self._gesture_state == 'Scale':
                # Kivy Windows (and maybe others) sometimes inserts a
                # bogus event
                if len(self._touches) == 2 or len(self._touches) == 3:
                    self.cg_scale_end(self._touches[0], self._touches[1])
                    self._new_gesture()

            elif self._gesture_state == 'Long Press Move':
                self._stop_velocity_clock()
                self.cg_long_press_move_end(touch, x, y)
                self._new_gesture()

            elif self._gesture_state == 'Move':
                self._stop_velocity_clock()
                self.cg_move_end(touch, x, y)
                self._new_gesture()

            elif self._gesture_state == 'Long Pressed':
                self.cg_long_press_end(touch, x, y)
                self._new_gesture()
                
            elif self._gesture_state == 'Wheel' or\
                 self._gesture_state == 'Swipe':
                self._new_gesture()

        return super().on_touch_up(touch)                

    ############################################
    # gesture utilities
    ############################################

    ### long press clock ###
    def _long_press_event(self, touch, dt):
        distance_squared = (touch.x-touch.ox)**2 + (touch.y-touch.oy)**2
        if distance_squared < self._DOUBLE_TAP_DISTANCE **2:
            x, y = self._touch_to_widget(touch)
            self.cg_long_press(touch, x, y)
            self._gesture_state = 'Long Pressed'

    def _not_long_press(self):
        if self._long_press_schedule:
            Clock.unschedule(self._long_press_schedule)
            self._long_press_schedule = None

    ### single tap clock ###
    def _single_tap_event(self, touch, dt):
        if self._gesture_state == 'Dont Know':
            if not self._long_press_schedule:
                x, y = self._touch_to_widget(touch)
                self.cg_tap(touch,x,y)
                self._new_gesture()

    def _not_single_tap(self):
        if self._single_tap_schedule:
            Clock.unschedule(self._single_tap_schedule)
            self._single_tap_schedule = None

    ### swipe clock ###
    def _possible_swipe(self, touch, start_time, dt):
        self._not_swipe()
        if self._has_swipe_velocity(touch, start_time):
            # A Swipe pre-empts a Move, so reset the Move
            x, y = self._touch_down_to_widget(touch)
            self.cg_move_to(touch, x, y, self._velocity)
            self.cg_move_end(touch, x, y)
            self._gesture_state = 'Swipe'
            if self.touch_horizontal(touch):
                self.cg_swipe_horizontal(touch, touch.x-touch.ox > 0)
            else:
                self.cg_swipe_vertical(touch, touch.y-touch.oy > 0)


    def _not_swipe(self):
        if self._swipe_schedule:
            Clock.unschedule(self._swipe_schedule)
            self._swipe_schedule = None

    def _has_swipe_velocity(self, touch, start_time):
        period = time() - start_time
        distance = sqrt((touch.x-touch.ox)**2 +\
                        (touch.y-touch.oy)**2)
        if period:
            velocity = distance / (period * Metrics.dpi)
        else:
            velocity = 0
        return velocity > self._SWIPE_VELOCITY

    ### velocity clock, for move operations ###
    def _start_velocity_clock(self,touch):
        self._velocity_time = time()
        self._velocity_x = touch.x
        self._velocity_y = touch.y
        self._velocity_schedule =\
            Clock.schedule_interval(partial(self._velocity_clock, touch),
                                    self._MOVE_VELOCITY_SAMPLE)
                    
    def _velocity_clock(self, touch, dt):
        now = time()
        period = now - self._velocity_time
        distance = sqrt((touch.x - self._velocity_x)**2 +\
                        (touch.y - self._velocity_y)**2)
        if period:
            self._velocity = distance / (period * Metrics.dpi) 
        else:
            self._velocity = 0
        self._velocity_time = now
        self._velocity_x = touch.x
        self._velocity_y = touch.y

    def _stop_velocity_clock(self):
        if self._velocity_schedule:
            Clock.unschedule(self._velocity_schedule)
            self._velocity_schedule = None

    ### touch direction ###

    def touch_horizontal(self, touch):
        return abs(touch.x-touch.ox) > abs(touch.y-touch.oy)

    def touch_vertical(self, touch):
        return abs(touch.y-touch.oy) > abs(touch.x-touch.ox)

    ### to widget coordinates ###
    
    def _scale_to_widget(self, touch0, touch1):
        midx = abs(touch0.x - touch1.x)/2 + min(touch0.x, touch1.x)
        midy = abs(touch0.y - touch1.y)/2 + min(touch0.y, touch1.y)
        # convert to widget
        x = midx - self.x
        y = midy - self.y
        return x, y

    def _touch_to_widget(self, touch):
        return (touch.x - self.x, touch.y - self.y)

    def _touch_down_to_widget(self, touch):
        return (touch.ox - self.x, touch.oy - self.y)

    ### gesture utilities ###

    def _remove_gesture(self, touch):
        if touch and len(self._touches):
            if touch in self._touches:
                self._touches.remove(touch)
            
    def _new_gesture(self):
        self._touches = []
        self._long_press_schedule = None
        self._single_tap_schedule = None
        self._velocity_schedule = None
        self._swipe_schedule = None
        self._gesture_state = 'None'
        self._finger_distance = 0
        self._velocity = 0

    ### CTRL SHIFT key detect
    def _ctrl_key_down(self, a, b, c, d, modifiers):
        if 'ctrl' in modifiers:
            self._CTRL = True

    def _shift_key_down(self, a, b, c, d, modifiers):
        if 'shift' in modifiers:
            self._SHIFT = True
        
    def _key_up(self, *args):
        self._CTRL = False
        self._SHIFT = False

    ############################################
    # User Events
    # define some subset in the derived class
    ############################################

    ############# Tap, Double Tap, and Long Press
    def cg_tap(self, touch, x, y):
        pass

    def cg_double_tap(self, touch, x, y):
        pass

    def cg_long_press(self, touch, x, y):
        pass

    def cg_long_press_end(self, touch, x, y):
        pass

    ############## Move
    def cg_move_start(self, touch, x, y):
        pass

    def cg_move_to(self, touch, x, y, velocity):
        # velocity is average of the last self._MOVE_VELOCITY_SAMPLE sec,
        # in inches/sec  :)
        pass

    def cg_move_end(self, touch, x, y):
        pass

    ############### Move preceded by a long press.
    # cg_long_press() called first, cg_long_press_end() is not called
    def cg_long_press_move_start(self, touch, x, y):
        pass

    def cg_long_press_move_to(self, touch, x, y, velocity):
        # velocity is average of the last self._MOVE_VELOCITY_SAMPLE,
        # in inches/sec  :)
        pass

    def cg_long_press_move_end(self, touch, x, y):
        pass

    ############### a fast move
    def cg_swipe_horizontal(self, touch, left_to_right):
        pass

    def cg_swipe_vertical(self, touch, bottom_to_top):
        pass

    ############### pinch/spread
    def cg_scale_start(self, touch0, touch1, x, y):
        pass

    def cg_scale(self, touch0, touch1, scale, x, y):
        pass

    def cg_scale_end(self, touch0, touch1):
        pass

    ############# Mouse Wheel, or Windows touch pad two finger vertical move
    
    ############# a common shortcut for scroll
    def cg_wheel(self, touch, scale, x, y):
        pass

    ############# a common shortcut for pinch/spread
    def cg_ctrl_wheel(self, touch, scale, x, y):
        pass

    ############# a common shortcut for horizontal scroll
    def cg_shift_wheel(self, touch, scale, x, y):
        pass
