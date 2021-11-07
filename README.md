Common Gestures Example
=======================

*An example of using gestures4kivy*

[**Other Examples**](https://github.com/Android-for-Python/INDEX-of-Examples)

## Dependencies 

This example depends on the [gestures4kivy package](https://github.com/Android-for-Python/gestures4kivy), which must be installed. The package install, API, and any known hardware specific issues are documented on the package homepage.

## The Examples

Run the example `main.py` it has five screens. It may be run on any OS.

The first screen demonstrates a Screen that responds to a swipe. To implement we create a new class `SwipeScreen` inheriting from `Screen`. A callback is added for each gesture we choose to recognize:

```
### A swipe sensitive Screen
class SwipeScreen(Screen, CommonGestures):

    def cg_swipe_horizontal(self, touch, right):
        # here we add the user defined behavior for the gesture
	# this method controls the ScreenManager in response to a swipe
        App.get_running_app().swipe_screen(right)
```

In this case the `swipe_screen()` method implements the gesture behavior when the callback occurs. The `SwipeScreen` class is added to the screen manager in the usual way. And `swipe_screen()` controls the screen manager as shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/main.py). 

The `GestureCanvas` example illustrates changing objects on a canvas, the `long press move` gesture, and the utility of visual feedback with a long press. See the full example [gesturecanvas.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/gesturecanvas.py).

Another example is `ZoomImage` an `Image` widget that pans, and zooms from the texture to optimize for resolution. See the full example [zoomimage.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/zoomimage.py).

Some Kivy widgets have gestures predefined. You can **replace** the gestures by making a copy of `CommonGestures` and replacing its inheritance from `Widget` with inheritance from the Kivy widget you want to modify. Then implement the calls to that widget's behavior.

The Android Back Gesture is not included in `CommonGestures` as its use is now limited because on Android >= 10 devices the back gesture is used to pause an app. However an example usage is shown in [main.py](https://github.com/Android-for-Python/Common-Gestures-Example/blob/main/main.py). 

