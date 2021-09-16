Common Gestures Example
=======================

*Use a Gestures api in place of (and depending on) the Kivy touch api*

## Behavior

The class `CommonGestures` detects the common Android gestures for `scale`, `move`, `swipe`, `long press move`, `long press`, `tap`, and `double tap`. A `long press move` is initiated with a `long press`. On the desktop the class also detects `mouse wheel` and the touchpad equivalent `two finger move`. 

Designed for use on Android, the gestures can be used on any Kivy supported platform and input device. To be clear these are Android style gestures that are available across platforms and input devices.

In addition, for platforms with a mouse scroll wheel the usual conventions are detected: `scroll wheel` can be used for vertical scroll, `shift-scroll wheel` can be used for horizontal scroll, and `ctrl-scroll wheel` can be used for zoom. Also on touch pads, vertical or horizontal two finger movement emulates a mouse scroll wheel. Also a mouse right click, or pad two finger tap is detected.

These gestures can be **added** to Kivy widgets by subclassing a Kivy Widget and `CommonGestures`, and then including the methods for the required gestures. For a minimal example see `SwipeScreen` below.

`CommonGestures` callback methods detect gestures, they do not define behaviors.

## Examples

Run the example `main.py` it has five screens. It may be run on any OS.

The first screen demonstrates a Screen that responds to a swipe. To implement we create a new class `SwipeScreen` inheriting from `Screen`. A callback is added for each gesture we choose to recognize:

```
### A swipe sensitive Screen
class SwipeScreen(Screen, CommonGestures):

    def cg_swipe_horizontal(self, touch, right):
        # here we add the user defined behavior for the gesture
	# this method controls the ScreenManager 
        App.get_running_app().swipe_screen(right)
```
In this case the `swipe_screen()` method implements the gesture behavior when the callback occurs. The `SwipeScreen` class is added to the screen manager in the usual way. And `swipe_screen()` controls the screen manager as shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/main.py). 

The `GestureCanvas` example illustrates changing objects on a canvas, the `long press move` gesture, and the utility of visual feedback with a long press. See the full example [gesturecanvas.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/gesturecanvas.py).

Another example is `ZoomImage` an `Image` widget that pans, and zooms from the texture to optimize for resolution. See the full example [zoomimage.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/zoomimage.py).

Some Kivy widgets have gestures predefined. You can **replace** the gestures by making a copy of `CommonGestures` and replacing its inheritance from `Widget` with inheritance from the Kivy widget you want to modify. Then implement the calls to that widget's behavior.

The Android Back Gesture is not included in `CommonGestures` as its use is now limited because on Android >= 10 devices the back gesture is used to pause an app. However an example usage is shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/main.py). 

## API

`CommonGestures` implements these gesture callbacks, a child class may use any subset:

```
    ############################################
    # User Events
    # define some subset in the derived class
    ############################################

    ############# Tap and Long Press
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
        # velocity is average of the last 0.2 sec, in inches/sec  :)
        pass

    def cg_move_end(self, touch, x, y):
        pass

    ############### Move preceded by a long press
    def cg_long_press_move_start(self, touch, x, y):
        pass

    def cg_long_press_move_to(self, touch, x, y, velocity):
        # velocity is average of the last 0.2 sec, in inches/sec  :)
        pass

    def cg_long_press_move_end(self, touch, x, y):
        pass

    ############### fast horizontal movement
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
	
```

## Hardware Considerations

### Android

Pinch/spread focus is the mid point between two fingers. The mouse wheel callbacks are not generated.

### Windows

This is required at the top of main.py to disable a Kivy feature:
```
if platform == 'win':
    # Dispose of that nasty red dot on Windows
    Config.set('input', 'mouse', 'mouse, disable_multitouch')
```
On some touchpads pinch/spread will not be detected if this feature is not disabled.

#### Mouse

As usual, `Move`, `Long Press Move`, `Swipe`, and `Long Press` are initiated with press the left mouse button, and end when the press ends. The right mouse button generates a `cg_two_finger_tap()` callback.

Mouse wheel movement generates t `cg_wheel()`, `cg_shift_wheel()`, and `cg_ctrl_wheel()` callbacks.

#### Touch Pad

As usual, `Move`, `Long Press Move`, `Swipe`, and `Long Press` are initiated with **'one and a half taps'**, or a press on the bottom left corner of the trackpad. 

Two finger pinch/spread uses the cursor location as focus. Note that the cursor may move significantly during a pinch/spread.

A two finger move is interpreted by a touch pad as the equivalent mouse wheel event. A two finger tap generates a `cg_two_finger_tap()` callback.

### Mac

Two finger pinch/spread is not available. Use `Command` and `vertical scroll`.

Force Click (deep press) is reported as a long press, this is a happy coincidence and not by design.

### iOS
Not tested

### Linux
Not tested

### Rasberry
Not tested



## Acknowledgement

A big thank you to Elliot for his analysis, constructive suggestions, and testing.