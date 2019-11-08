import math
from . import Program
from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    x: float
    y: float

    def __add__(self, other):
        if isinstance(other, Polar):
            other = other.point()

        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, Polar):
            other = other.point()

        return Point(x=self.x - other.x, y=self.y - other.y)

    @property
    def over_x(self):
        return Point(x=self.x, y=-self.y)

    @property
    def over_y(self):
        return Point(x=-self.x, y=self.y)

    def polar(self):
        th = math.degrees(math.atan2(-self.y, self.x)) + 90
        while th < 0:
            th += 360

        r = math.hypot(self.x, self.y)
        return Polar(th=th, r=r)


@dataclass
class Polar:
    th: float  # degrees clockwise from north
    r: float

    @property
    def over_x(self):
        return Polar(th=180 - self.th, r=self.r)

    @property
    def over_y(self):
        return Polar(th=-self.th, r=self.r)

    def point(self):
        th = math.radians(self.th - 90)
        x = math.cos(th) * self.r
        y = -math.sin(th) * self.r
        return Point(x=x, y=y)


sf = 1.0

side = 148.49 * sf
big_diam = 28 * sf
small_diam = 8 * sf
safe = 0.5

height = side * sqrt(3) / 2
offset = Point(x=-height / 3, y=-side / 2)

top = offset + Point(x=0, y=side)
bottom = offset + Point(x=0, y=0)
right = offset + Point(x=height, y=side / 2)

top_inset = Polar(th=150, r=big_diam)
bottom_inset = top_inset.over_x
right_inset = Polar(th=270, r=big_diam)

top_center = top + top_inset
bottom_center = bottom + bottom_inset
right_center = right + right_inset

tan_offset = Polar(th=30, r=big_diam / 2)
left_offset = Polar(270, r=big_diam / 2)

tl_tan = top_center + left_offset
tr_tan = top_center + tan_offset

rt_tan = right_center + tan_offset
rb_tan = right_center + tan_offset.over_x

bl_tan = bottom_center + left_offset
br_tan = bottom_center + tan_offset.over_x

p = Program()
with p:
    p.feed = 1500
p.goto(x=tl_tan.x, y=tl_tan.y)

with p:
    p.z -= safe

p.arc_cw(x=tr_tan.x, y=tr_tan.y, i=top_center.x - tl_tan.x, j=top_center.y - tl_tan.y)

p.linear
p.goto(x=rt_tan.x, y=rt_tan.y)
p.arc_cw(
    x=rb_tan.x, y=rb_tan.y, i=right_center.x - rt_tan.x, j=right_center.y - rt_tan.y
)

p.linear
p.goto(x=br_tan.x, y=br_tan.y)
p.arc_cw(
    x=bl_tan.x, y=bl_tan.y, i=bottom_center.x - br_tan.x, j=bottom_center.y - br_tan.y
)

p.linear
p.goto(x=tl_tan.x, y=tl_tan.y)

with p:
    p.z += safe

with p:
    p.rapid
    p.goto(0, 0, 0)


for command in p.commands:
    print(command)
