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
        self._SWIPE_TIME          = 2/30                # sec 
        self._SWIPE_VELOCITY      = 10                  # inches/sec, heuristic
        self._WHEEL_SENSITIVITY   = 1.1                 # heuristic

    #####################
    # Kivy Touch Events
    #####################
    # In the case of a RelativeLayout, the touch.pos value is not persistent.
    # Because the same Touch is called twice, once with Window relative and
    # once with the RelativeLayout relative values. 
    # The on_touch_* callbacks have the required value because of collide_point
    # but only within the scope of that touch callback.
    #
    # This is an issue for gestures with persistence, and with two touches
    # (one of which always depends on persistence)
    # So if we have a RelativeLayout we can't rely on the value in touch.pos .
    # So regardless of there being a RelativeLayout, we save each touch.pos
    # in self._persistent_pos[] and use that when the current value is
    # required. Some Clock events require the start value, we propagate
    # this as an argument.
    
    ### touch down ###
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._touches.append(touch)
            if touch.is_mouse_scrolling:
                self._gesture_state = 'Wheel'
                scale = self._WHEEL_SENSITIVITY
                x, y = self._pos_to_widget(*touch.pos)
                if touch.button == 'scrollleft':
                    self.cg_shift_wheel(touch,1/scale, x, y)
                elif touch.button == 'scrollright':
                    self.cg_shift_wheel(touch,scale, x, y)
                else: 
                    if touch.button == 'scrollup':
                        scale = 1/scale
                    if self._CTRL:
                        self.cg_ctrl_wheel(touch,scale, x, y)
                    elif self._SHIFT:
                        self.cg_shift_wheel(touch,scale, x, y)
                    else:
                        self.cg_wheel(touch,scale, x, y)

            elif len(self._touches) == 1:
                if 'button' in touch.profile and touch.button == 'right':
                    # Two finger tap or right click
                    self._gesture_state = 'Right' 
                else:
                    self._gesture_state = 'Dont Know' 
                    # schedule a posssible long press
                    self._long_press_schedule =\
                        Clock.schedule_once(partial(self._long_press_event,
                                                    touch, (*touch.pos),
                                                    (*touch.opos)),
                                            self._LONG_PRESS)
                    # schedule a posssible tap 
                    if not self._single_tap_schedule:
                        self._single_tap_schedule =\
                            Clock.schedule_once(partial(self._single_tap_event,
                                                        touch ,(*touch.pos)),
                                                self._DOUBLE_TAP_TIME)

                self._persistent_pos = [(0,0),(0,0)]
                self._persistent_pos[0] = tuple(touch.pos)
            elif len(self._touches) == 2:
                self._gesture_state = 'Scale'
                # If two fingers it cant be a long press, swipe or tap
                self._not_long_press() 
                self._not_single_tap()
                self._not_swipe()
                self._persistent_pos[1] = tuple(touch.pos)
                x, y = self._scale_midpoint()
                self.cg_scale_start(self._touches[0],self._touches[1], x, y)

        return super().on_touch_down(touch)

    ### touch move ###
    def on_touch_move(self, touch):
        if touch in self._touches and self.collide_point(*touch.pos):
            if touch.dx or touch.dy:
                # If moving it cant be a pending long press or tap
                self._not_long_press()
                self._not_single_tap() 
                # State changes
                if self._gesture_state == 'Long Pressed':
                    self._gesture_state = 'Long Press Move'
                    x, y = self._pos_to_widget(*touch.opos)
                    self._start_velocity_clock(touch)
                    self.cg_long_press_move_start(touch, x, y)

                elif self._gesture_state == 'Dont Know':
                    # possible pre-empt as swipe
                    self._persistent_pos[0] = tuple(touch.pos)
                    self._swipe_schedule =\
                        Clock.schedule_once(partial(self._possible_swipe,
                                                    touch, (*touch.opos),
                                                    time()),
                                            self._SWIPE_TIME)
                    # start the move, will be reset if is swipe
                    self._gesture_state = 'Move' 
                    x, y = self._pos_to_widget(*touch.opos)
                    self._start_velocity_clock(touch)
                    self.cg_move_start(touch, x, y)

                if self._gesture_state == 'Scale':
                    if len(self._touches) <= 2:
                        indx = self._touches.index(touch)
                        self._persistent_pos[indx] = tuple(touch.pos)
                    if len(self._touches) > 1:
                        finger_distance = self._scale_distance()
                        if self._finger_distance:
                            scale = finger_distance / self._finger_distance
                            if abs(scale) != 1:
                                x, y = self._scale_midpoint()
                                self.cg_scale(self._touches[0],
                                              self._touches[1],
                                              scale, x, y)
                        self._finger_distance = finger_distance

                else: 
                    x, y = self._pos_to_widget(*touch.pos)
                    if self._gesture_state == 'Move':
                        self._persistent_pos[0] = tuple(touch.pos)
                        self.cg_move_to(touch, x, y, self._velocity)
                        
                    elif self._gesture_state == 'Long Press Move':
                        self.cg_long_press_move_to(touch, x, y, self._velocity)
                        
        return super().on_touch_move(touch)                    

    ### touch up ###
    def on_touch_up(self, touch):
        if touch in self._touches and self.collide_point(*touch.pos):
            self._not_long_press()
            self._not_swipe()
            x, y = self._pos_to_widget(*touch.pos)

            if self._gesture_state == 'Dont Know':
                if touch.is_double_tap:
                    self._not_single_tap()
                    self.cg_double_tap(touch, x, y)
                    self._new_gesture()
                else:
                    self._remove_gesture(touch)

            elif self._gesture_state == 'Right':
                self.cg_two_finger_tap(touch, x, y)
                
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
    #

    ### long press clock ###
    def _long_press_event(self, touch, x, y, ox, oy, dt):
        distance_squared = (x -ox)**2 + (y -oy)**2
        if distance_squared < self._DOUBLE_TAP_DISTANCE **2:
            x, y = self._pos_to_widget(x, y)
            self.cg_long_press(touch, x, y)
            self._gesture_state = 'Long Pressed'

    def _not_long_press(self):
        if self._long_press_schedule:
            Clock.unschedule(self._long_press_schedule)
            self._long_press_schedule = None

    ### single tap clock ###
    def _single_tap_event(self, touch, x, y, dt):
        if self._gesture_state == 'Dont Know':
            if not self._long_press_schedule:
                x, y = self._pos_to_widget(x, y)
                self.cg_tap(touch,x,y)
                self._new_gesture()

    def _not_single_tap(self):
        if self._single_tap_schedule:
            Clock.unschedule(self._single_tap_schedule)
            self._single_tap_schedule = None

    ### swipe clock ###
    def _possible_swipe(self, touch, ox, oy, start_time, dt):
        self._not_swipe()
        x, y = self._persistent_pos[0]
        if self._has_swipe_velocity(x, y, ox, oy, start_time):
            # A Swipe pre-empts a Move, so reset the Move
            wox, woy = self._pos_to_widget(ox, oy)
            self.cg_move_to(touch, wox, woy, self._velocity)
            self.cg_move_end(touch, wox, woy)
            self._gesture_state = 'Swipe'
            if self.touch_horizontal(touch):
                self.cg_swipe_horizontal(touch, x-ox > 0)
            else:
                self.cg_swipe_vertical(touch, y-oy > 0)


    def _not_swipe(self):
        if self._swipe_schedule:
            Clock.unschedule(self._swipe_schedule)
            self._swipe_schedule = None

    def _has_swipe_velocity(self, x, y, ox, oy, start_time):
        period = time() - start_time
        distance = sqrt((x-ox)**2 + (y-oy)**2)
        if period:
            velocity = distance / (period * Metrics.dpi)
        else:
            velocity = 0
        return velocity > self._SWIPE_VELOCITY

    ### velocity clock, for move operations ###
    def _start_velocity_clock(self,touch):
        self._velocity_time = time()
        self._velocity_x, self._velocity_y = self._persistent_pos[0]
        self._velocity_schedule =\
            Clock.schedule_interval(partial(self._velocity_clock, touch),
                                    self._MOVE_VELOCITY_SAMPLE)
                    
    def _velocity_clock(self, touch, dt):
        now = time()
        period = now - self._velocity_time
        x, y = self._persistent_pos[0]
        distance = sqrt((x - self._velocity_x)**2 +\
                        (y - self._velocity_y)**2)
        if period:
            self._velocity = distance / (period * Metrics.dpi) 
        else:
            self._velocity = 0
        self._velocity_time = now
        self._velocity_x = x
        self._velocity_y = y

    def _stop_velocity_clock(self):
        if self._velocity_schedule:
            Clock.unschedule(self._velocity_schedule)
            self._velocity_schedule = None

    ### touch direction ###
    # direction is the same with or without RelativeLayout

    def touch_horizontal(self, touch):
        return abs(touch.x-touch.ox) > abs(touch.y-touch.oy)

    def touch_vertical(self, touch):   
        return abs(touch.y-touch.oy) > abs(touch.x-touch.ox)

    ### Two finger touch ###
    
    def _scale_distance(self):
        x0, y0 = self._persistent_pos[0]
        x1, y1 = self._persistent_pos[1]
        return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)    

    def _scale_midpoint(self):
        x0, y0 = self._persistent_pos[0]
        x1, y1 = self._persistent_pos[1]
        midx = abs(x0 - x1)/2 + min(x0, x1)
        midy = abs(y0 - y1)/2 + min(y0, y1)
        # convert to widget
        x = midx - self.x
        y = midy - self.y
        return x, y

    ### Every result is in the self frame ###

    def _pos_to_widget(self, x, y):
        return (x - self.x, y - self.y)

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
        command_key = platform == 'macosx' and 'meta' in modifiers
        if 'ctrl' in modifiers or command_key:
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

    def cg_two_finger_tap(self, touch, x, y):
        # also a mouse right click, desktop only
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
