from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from commongestures import CommonGestures

class ZoomImage(Image, CommonGestures):

    # Display a region of a texture in an Image.
    # Controlled by pan and zoom gestures.
    #
    # Optimized for resolution by selecting from the texture.

    core_source = StringProperty(None)

    def __init__(self, source, **args):
        super().__init__(**args)
        self.core_source = source
        # Normal operation requires `keep_ratio` and `allow_stretch`
        # are both True.
        self.keep_ratio = True
        self.allow_stretch = True

    def on_core_source(self, *args):
        self.core_image = CoreImage(self.core_source)
        self._zi_image_location_in_widget()
        self._zi_init()

    def on_size(self, *args):
        self._zi_image_location_in_widget()

    # Gestures recognized
    ################################################

    # Zoom
    def cg_scale_start(self, touch0, touch1, x, y):
        self._zi_set_origin(x, y)

    def cg_scale(self, touch0, touch1, scale, x, y):
        self._zi_transform(x,y,scale)

    def cg_ctrl_wheel(self, touch, scale, x, y):
        # let mouse users zoom with the wheel
        self._zi_set_origin(x, y)
        self._zi_transform(x,y,scale)

    # Pan
    def cg_move_start(self, touch, x, y):
        self._zi_set_origin(x, y)

    def cg_move_to(self, touch, x, y, velocity):
        self._zi_transform(x,y,1)
        
    def cg_wheel(self, touch, scale, x, y):
        # let mouse users pan vertically with the wheel
        self._zi_set_origin(x, y)
        self._zi_transform(x, y*scale, 1)

    def cg_shift_wheel(self, touch, scale, x, y):
        # let mouse users pan horizontally with the wheel
        self._zi_set_origin(x, y)
        self._zi_transform(x*scale, y, 1)

    # Reset
    def cg_double_tap(self, touch, x, y):
        self._zi_init()

    # Behavior
    ################################################

    def _zi_set_origin(self, x, y):
        iw, ih = self.norm_image_size
        tw, th = self.core_image.size
        zoom   = self._zi_zoom_state
        left =  self._zi_region_pos['left'] 
        bottom =  self._zi_region_pos['bottom'] 
        self._zi_origin_xt =\
            left + (x - self.texture_offset_x ) * tw /(iw * zoom) 
        self._zi_origin_yt =\
            bottom + (y - self.texture_offset_y ) * th / (ih * zoom)

    def _zi_transform(self,x,y,scale):
        if not self._zi_inside_image(x,y):
            return
        iw, ih = self.norm_image_size
        tw, th = self.core_image.size
        xt = self._zi_origin_xt
        yt = self._zi_origin_yt
        # Zoom state
        zoom = max(1, self._zi_zoom_state * scale)
        # New rectangle
        wz = tw / zoom
        hz = th / zoom
        xo = x - self.texture_offset_x
        yo = y - self.texture_offset_y
        left   = xt - wz * xo / iw
        top    = yt + hz * (ih - yo) / ih
        right  = xt + wz * (iw - xo) / iw
        bottom = yt - hz * yo / ih
        # Stay in texture:
        if left < 0:
            right = right - left
            left = 0
        elif right > tw:
            left = tw - (right - left) 
            right = tw
        if bottom < 0:
            top  = top - bottom
            bottom = 0 
        elif top > th:
            bottom = th - (top - bottom)
            top = th
        # Ignore a zoom to less than a texture pixel
        if round(right - left) <= 0 or round(top - bottom) <= 0:
            return
        # Save state
        self._zi_zoom_state = zoom
        self._zi_region_pos = {'left' : left, 'bottom' : bottom}
        # Update image
        self.texture = self.core_image.texture.get_region(left, bottom,
                                                          right - left,
                                                          top - bottom)

    def _zi_init(self):
        self.texture = self.core_image.texture
        self._zi_zoom_state = 1               
        self._zi_region_pos = {'left' : 0, 'bottom' : 0}

    # Utilities
    ################################################

    def _zi_image_location_in_widget(self):
        iw, ih = self.norm_image_size
        tw, th = self.core_image.size
        if self.width / self.height > tw / th:
            texture_offset_x = (self.width - iw) / 2
            texture_offset_y = 0
        else:
            texture_offset_x = 0
            texture_offset_y = (self.height - ih) / 2
        # Origin of displayed texture in units of Image pixels
        self.texture_offset_x = texture_offset_x
        self.texture_offset_y = texture_offset_y

    def _zi_inside_image(self, x, y):
        # True if cursor is inside the image within this Widget
        return x >= self.texture_offset_x and\
            x <= self.width - self.texture_offset_x and\
            y >= self.texture_offset_y and\
            y <= self.height - self.texture_offset_y 

