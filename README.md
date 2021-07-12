Common Gestures Example
=======================

*Gestures in place of (and using) the Kivy touch api*

## Behavior

The class `CommonGestures` detects the common gestures for `scale`, `move`, `swipe`, `long press move`, `long press`, `tap`, and `double tap`. A `long press move` is initiated with a `long press`. On the desktop the class also detects `mouse wheel` and the touchpad equivalent `two finger move`.

Designed for use on Android, the gestures can be used on any Kivy supported platform and input device.

These gestures can be **added** to Kivy widgets by subclassing a Kivy Widget and `CommonGestures`, and then including the methods for the required gestures. For a minimal example see `SwipeScreen` below.

`CommonGestures` methods detect gestures, they do not define behaviors.

## Examples

Run the example `main.py` it has five screens. It may be run on any OS.

The first screen demonstrates a Screen that responds to a swipe. To implement we create a new class `SwipeScreen` inheriting from `Screen`. The `SwipeScreen` class is then added to the screen manager in the usual way.
```
### A swipe sensitive Screen
class SwipeScreen(Screen, CommonGestures):
    # Gesture recognized
    ################################################
    def cg_swipe_horizontal(self, touch, right):
        # here we add the user defined behavior for the gesture
	# this method controls the ScreenManager 
        App.get_running_app().swipe_screen(right)
```
Controling the behavior of the screen manager from the `cg_swipe_horizontal()` callback is shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/main.py) where the `swipe_screen()` method is defined.

The `GestureCanvas` example illustrates changing objects on a canvas, the `long press move gesture`, and the utility of visual feedback with a long press. See the full example [gesturecanvas.py](https://github.com/Android-for-Python/Common-Gestures-Example/gesturecanvas.py).

Another example is `ZoomImage` an `Image` widget that pans, and zooms from the texture to optimize for resolution. See the full example [zoomimage.py](https://github.com/Android-for-Python/Common-Gestures-Example/zoomimage.py).

Some Kivy widgets have gestures predefined. You can **replace** the gestures by making a copy of `CommonGestures` and replacing its inheritance from `Widget` with inheritance from the Kivy widget you want to modify. Then implement the calls to that widget's behavior.

The Android Back Gesture is not included in `CommonGestures` as its use is now limited because on Android >= 10 devices it is used to pause an app. However an example usage is shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/main.py). 

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

    ############# mouse wheel or touch pad two finger move
    def cg_wheel(self, touch, scale, x, y):
        pass
```

## Hardware Considerations

### Android and iOS

Pinch/spread focus is the mid point between two fingers. The `cg_wheel()` callback is not generated.

### Windows

This is required at the top of main.py to disable an undocumented Kivy feature:
```
if platform == 'win':
    # Dispose of that nasty red dot on Windows
    Config.set('input', 'mouse', 'mouse, disable_multitouch')
```

### Mouse

As usual, `Move`, `Long Press Move`, `Swipe`, and `Long Press` are initiated with press the left mouse button, and end when the press ends.

Mouse wheel movement generates a `cg_wheel()` callback.

### Touch Pad

As usual, `Move`, `Long Press Move`, `Swipe`, and `Long Press` are initiated with **'one and a half taps'**, or a press on the bottom left corner of the trackpad. 

Two finger pinch/spread uses the cursor location as focus. Note that the cursor may move significantly during a pinch/spread.

A two finger vertical move is interpretd by a touch pad as a mouse wheel event.

### Mac

idk

