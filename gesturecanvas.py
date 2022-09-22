from kivy.graphics import Color, Rectangle, Line
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Quad
from kivy.graphics.transformation import Matrix
from kivy.metrics import Metrics
from kivy.utils import platform
from math import sqrt, cos, sin, pi, radians
from gestures4kivy import CommonGestures

### Move an item on a canvas
###################################################

class GestureCanvas(CommonGestures):
    # The CommonGestures class is derived from Widget,
    # for a canvas only operations inherit only from CommonGestures.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_scale = 1
    
    ############# Gestures

    def cgb_select(self, touch, focus_x, focus_y, long_press):
        if long_press and self.inside_box(focus_x, focus_y):
            self.visual_feedback(True, focus_x, focus_y)
    
    def cgb_long_press_end(self, touch, focus_x, focus_y):
        self.visual_feedback(False, focus_x, focus_y)

    def cgb_drag(self, touch, focus_x, focus_y, delta_x, delta_y):
        self.move_box(focus_x, focus_y, delta_x, delta_y)

    def cgb_rotate(self, touch0, touch1, focus_x, focus_y, delta_angle):
        self.rotate_box(delta_angle, focus_x , focus_y)

    def cgb_zoom(self, touch0, touch1, focus_x, focus_y, delta_scale):
        self.zoom_box(delta_scale, focus_x , focus_y)

    ############ Behaviors

    def zoom_box(self, delta_scale, x , y):
        if self.inside_box(x, y):
            px = x + self.x
            py = y + self.y
            new_x = []
            new_y = []
            for ox, oy, in zip(self.box_x, self.box_y):
                qx = px + delta_scale * (ox - px)
                qy = py + delta_scale * (oy - py)
                new_x.append(qx)
                new_y.append(qy)
            if self.box_inside_widget(new_x, new_y):
                self.total_scale *= delta_scale
                self.box_x = new_x
                self.box_y = new_y
                self.draw_box(x,y)

    def rotate_box(self, angle_delta, x, y):
        if self.inside_box(x, y):
            px = x + self.x
            py = y + self.y
            new_x = []
            new_y = []
            angle = radians(angle_delta)
            for ox, oy, in zip(self.box_x, self.box_y):
                qx = px + cos(angle) * (ox - px) - sin(angle) * (oy - py)
                qy = py + sin(angle) * (ox - px) + cos(angle) * (oy - py)
                new_x.append(qx)
                new_y.append(qy)
            if self.box_inside_widget(new_x, new_y):
                self.box_x = new_x
                self.box_y = new_y
                self.draw_box(x,y)

    def move_box(self, x, y, delta_x, delta_y):
        if self.inside_box(x, y):
            new_x = []
            new_y = []
            for ox, oy, in zip(self.box_x, self.box_y):
                qx = ox + delta_x
                qy = oy + delta_y
                new_x.append(qx)
                new_y.append(qy)
            if self.box_inside_widget(new_x, new_y):
                self.box_x = new_x
                self.box_y = new_y
                self.draw_box(x,y)

    def visual_feedback(self, yes, x, y):
        mobile = platform == 'android' or platform == 'ios'
        self.visual_fb = yes and mobile
        self.draw_box(x,y)

    ############ Utilities

    # https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
    def inside_box(self,x,y):
        x += self.x
        y += self.y
        xl = self.box_x[1:] + self.box_x[:1]  
        yl = self.box_y[1:] + self.box_y[:1]  
        a = []
        b = []
        for xe, ye, xn, yn in zip(self.box_x,self.box_y,xl,yl):
            a.append(sqrt((xe-xn)**2 + (ye-yn)**2))
            b.append(sqrt((xe-x)**2 + (ye-y)**2))
        bl = b[1:] + b[:1]
        u = []
        for ae, be, bn in zip(a, b, bl):
            u.append((ae + be + bn) / 2)
        A = 0
        for ue, ae, be, bn in zip(u, a, b, bl):
            A += sqrt(ue * (ue - ae) * (ue - be) * (ue - bn))
        A -= 0.00000001 # allow degraded precision
        Aref = (self.box_edge * self.total_scale) **2
        return A <= Aref and A > 0

    def box_inside_widget(self, box_x, box_y):
        if min(box_x) >= self.x and\
           min(box_y) >= self.y and\
           max(box_x) <= self.x + self.width and\
           max(box_y) <= self.y + self.height:
            return True
        return False

    def on_size(self, *args):
        self.visual_fb = False
        self.box_edge = Metrics.dpi
        # Window coordinates
        midpointbox = self.box_edge/2
        midpointwidget_x = self.width/2 + self.x
        midpointwidget_y = self.height/2 + self.y
        self.box_x = [midpointwidget_x - midpointbox,
                      midpointwidget_x + midpointbox,
                      midpointwidget_x + midpointbox,
                      midpointwidget_x - midpointbox]
        self.box_y = [midpointwidget_y - midpointbox,
                      midpointwidget_y - midpointbox,
                      midpointwidget_y + midpointbox,
                      midpointwidget_y + midpointbox]
        self.draw_box(0,0)
        
    def draw_box(self, x, y):
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1) # white
            Rectangle(pos = self.pos, size= self.size)
            Color(1,0,0) # red
            mergedxy = self.box_x + self.box_y
            mergedxy[::2] = self.box_x
            mergedxy[1::2] = self.box_y
            Quad(points = mergedxy)
            
            if self.visual_fb:
                Color(0,0,1) # blue
                Line(circle=(self.x + x, self.y + y, Metrics.dpi / 3),
                     width = 4)




            
                
