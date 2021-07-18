from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import Metrics
from kivy.utils import platform
from commongestures import CommonGestures

### Move an item on a canvas
###################################################

class GestureCanvas(CommonGestures):
    # The CommonGestures class is derived from Widget,
    # for a canvas only operations inherit only from CommonGestures.
    
    ############# Gestures
    
    def cg_long_press(self, touch, x, y):
        if self.inside_box(x,y):
            self.visual_feedback(True, x, y)

    def cg_long_press_end(self, touch, x, y):
        self.visual_feedback(False, x, y)

    def cg_long_press_move_start(self, touch, x, y):
        self.start(x, y)

    def cg_long_press_move_to(self, touch, x, y, velocity):
        self.move_box(x, y)

    def cg_long_press_move_end(self, touch, x, y):
        self.visual_feedback(False, x, y)

    def cg_scale(self, touch0, touch1, scale, x, y):
        self.zoom_box(scale, x , y)

    def cg_ctrl_wheel(self, touch, scale, x, y):
        # let mouse users zoom with the wheel
        self.zoom_box(scale, x , y)

    ############ Behaviors

    def zoom_box(self, scale, x , y):
        if self.inside_box(x,y):
            box_edge = self.box_edge
            if box_edge * scale >=  Metrics.dpi / 2:
                new_box_edge = self.box_edge * scale
                new_box_x = self.box_x + (box_edge - new_box_edge)/2
                new_box_y = self.box_y + (box_edge - new_box_edge)/2
                if self.box_inside_widget(new_box_x,new_box_y,new_box_edge):
                    self.box_x = new_box_x
                    self.box_y = new_box_y
                    self.box_edge = new_box_edge
                    self.draw_box(x,y)

    def visual_feedback(self,yes, x, y):
        self.can_drag = yes
        self.draw_box(x,y)

    def start(self, x, y):
        if self.inside_box(x,y):
            # save where in the box we touched
            self.drag_offset_x = self.x + x - self.box_x
            self.drag_offset_y = self.y + y - self.box_y

    def move_box(self, x, y):
        if self.can_drag:
            new_box_x = x + self.x - self.drag_offset_x
            new_box_y = y + self.y - self.drag_offset_y  
            if self.box_inside_widget(new_box_x,new_box_y,self.box_edge):
                self.box_x = new_box_x
                self.box_y = new_box_y
                self.draw_box(x,y)
            else:
                # the box doesn't move but the cursor does
                self.drag_offset_x = self.x + x - self.box_x
                self.drag_offset_y = self.y + y - self.box_y

    ############ Utilities

    def inside_box(self,x,y):
        x += self.x # convert to canvas coordinates
        y += self.y
        if x >= self.box_x  and x <= self.box_x + self.box_edge and\
           y >= self.box_y  and y <= self.box_y + self.box_edge:
            return True
        return False

    def box_inside_widget(self, box_x,box_y,box_edge):
        if box_x >= self.x and\
           box_y >= self.y and\
           box_x + box_edge <= self.x + self.width and\
           box_y + box_edge <= self.y + self.height:
            return True
        return False

    def on_size(self, *args):
        self.can_drag = False
        self.box_edge = Metrics.dpi
        self.box_x = round(self.width/2 + self.x - self.box_edge/2)
        self.box_y = round(self.height/2 + self.y - self.box_edge/2)
        self.draw_box(0,0)
        
    def draw_box(self, x, y):
        mobile = platform == 'android' or platform == 'ios'
        self.canvas.clear()
        with self.canvas:
            Color(1,1,1) # white
            Rectangle(pos = self.pos, size= self.size)
            if self.can_drag and not mobile:
                Color(0,0,1) # blue
            else:
                Color(1,0,0) # red
            Rectangle(pos = (self.box_x, self.box_y),
                      size= (self.box_edge, self.box_edge))
            if self.can_drag and mobile:
                Color(0,0,1) # blue
                Line(circle=(self.x + x, self.y + y, Metrics.dpi / 3),
                     width = 4)
