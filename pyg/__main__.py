from dataclasses import dataclass
from . import Program
from math import sqrt


@dataclass
class Point:
    x: float = None
    y: float = None
    z: float = None


side = 148.49
big_diam = 28
small_diam = 8
safe = 0.5

height = side * sqrt(3) / 2
offx = -height / 3
offy = -side / 2

top = Point(x=offx, y=offy + side)
bottom = Point(x=offx, y=offy)
right = Point(x=offx + height, y=offy + side / 2)

tan_x = big_diam / 4
tan_y = big_diam * sqrt(3) / 4

top_center = Point(x=top.x + big_diam / 2, y=top.y - big_diam * sqrt(3) / 2)
bottom_center = Point(x=bottom.x + big_diam / 2, y=bottom.y + big_diam * sqrt(3) / 2)
right_center = Point(x=right.x - big_diam, y=right.y)

tl_tan = Point(x=top.x, y=top_center.y)
tr_tan = Point(x=top_center.x + tan_x, y=top_center.y + tan_y)

rt_tan = Point(x=right_center.x + tan_x, y=right_center.y + tan_y)
rb_tan = Point(x=right_center.x + tan_x, y=right_center.y - tan_y)

bl_tan = Point(x=bottom.x, y=bottom_center.y)
br_tan = Point(x=bottom_center.x + tan_x, y=bottom_center.y - tan_y)

p = Program()
with p:
    p.feed = 1500
p.goto(x=tl_tan.x, y=tl_tan.y)

with p:
  p.z -= safe

p.arc_cw(x=tr_tan.x, y=tr_tan.y, i=top_center.x - tl_tan.x, j=top_center.y - tl_tan.y)

p.linear
p.goto(x=rt_tan.x, y=rt_tan.y)
p.arc_cw(x=rb_tan.x, y=rb_tan.y, i=right_center.x - rt_tan.x, j=right_center.y - rt_tan.y)

p.linear
p.goto(x=br_tan.x, y=br_tan.y)
p.arc_cw(x=bl_tan.x, y=bl_tan.y, i=bottom_center.x - br_tan.x, j=bottom_center.y - br_tan.y)

p.linear
p.goto(x=tl_tan.x, y=tl_tan.y)

with p:
  p.z += safe

with p:
  p.rapid
  p.goto(0, 0, 0)


for command in p.commands:
    print(command)
