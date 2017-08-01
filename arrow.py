#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2017 "Laxminarayan Kamath G A"<kamathln@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.


from kivy.properties import *
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.metrics import *
from kivy.graphics import *
import math


piby180 = math.pi/180.0
# ------------------ KVector -------------------- #

class KVector(EventDispatcher):
    o_x = NumericProperty(0)
    o_y = NumericProperty(0)
    to_x = NumericProperty(0)
    to_y = NumericProperty(0)
    to_pos = ReferenceListProperty(to_x,to_y)

    def get_angle(self):
        return ((math.atan2(self.to_x - self.o_x, self.o_y - self.to_y)/piby180)+630.0 ) % 360.0 

    def set_angle(self,angle):
        self.to_x = self.o_x + (math.cos(angle * piby180) * self.distance)
        self.to_y = self.o_y + (math.sin(angle * piby180) * self.distance)

    def get_distance(self):
        absx = abs(self.to_x-self.o_x) 
        absy = abs(self.to_y-self.o_y) 
        return math.sqrt((absx*absx)+(absy*absy))

    def set_distance(self, distance):
        self.to_x = self.o_x + ((math.cos(self.angle * piby180) * distance))
        self.to_y = self.o_y + ((math.sin(self.angle * piby180) * distance))
        
    angle = AliasProperty(
                          get_angle, 
                          set_angle,
                          bind=['o_x','o_y','to_x', 'to_y']
                         )
    distance = AliasProperty(
                          get_distance, 
                          set_distance,
                          bind=['o_x','o_y','to_x', 'to_y']
                         )
def move_point(x,y,angle,distance):
    return  (
             x + (math.cos(angle * piby180) * distance),
             y + (math.sin(angle * piby180) * distance)
            )

# ------------ Arrow -------------- #

class Arrow(Widget,KVector):
    head_size = NumericProperty(cm(0.5))
    shaft_width = NumericProperty(cm(0.05))
    fletching_radius = NumericProperty(cm(0.1))
    acolor = ListProperty([1,1,1,1])
    

    def __init__(self,*args, **kwargs):
        Widget.__init__(self,*args,**kwargs)
        KVector.__init__(self,*args,**kwargs)

        with self.canvas:
            self.icolor = Color(self.acolor)
            self.head = Mesh(mode='triangle_fan',indices=[0,1,2])
            self.shaft = Line(width=self.shaft_width)
            self.fletching = Ellipse()
        
        self.bind(
                  o_x=self.update_dims,
                  o_y=self.update_dims,
                  to_x=self.update_dims,
                  to_y=self.update_dims,
                  head_size=self.update_dims,
                  shaft_width=self.update_shaft_width,
                  acolor=self.update_color,
                  )
        self.update_dims()
        self.update_shaft_width()
        self.update_color()

    def update_shaft_width(self,*args):
        self.shaft.width = self.shaft_width

    def update_color(self, *args):
        self.icolor.rgba = self.acolor

    def update_dims(self, *args):
        shaft_x1,shaft_y1 = move_point(self.o_x, self.o_y, self.angle, self.fletching_radius / math.sqrt(2))
        shaft_x2,shaft_y2 = move_point(self.to_x, self.to_y, self.angle, -self.head_size/math.sqrt(2.0))
        self.shaft.points = [
                             shaft_x1, 
                             shaft_y1,
                             shaft_x2,
                             shaft_y2
                            ]
        head_x1, head_y1 = move_point(self.to_x, self.to_y, self.angle + 135, self.head_size)
        head_x2, head_y2 = move_point(self.to_x, self.to_y, self.angle - 135, self.head_size)
        self.head.vertices = [
                              self.to_x,
                              self.to_y, 
                              0,
                              0,
                              head_x1,
                              head_y1,
                              0,
                              0,
                              head_x2,
                              head_y2,
                              0,
                              0,
                             ]

        self.fletching.pos=move_point(self.o_x,
                                      self.o_y,
                                      225,
                                      self.fletching_radius)
        self.fletching.size=[self.fletching_radius*math.sqrt(2)]*2

