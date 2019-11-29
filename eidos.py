import math
from pyg import Program
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


sf = 0.8

tool_diam = 6.35
side = 148.49 * sf
big_diam = 28 * sf
small_diam = 8 * sf
small_inset = 34 * sf
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

tan_offset = Polar(th=30, r=big_diam / 2 + tool_diam / 2)
left_offset = Polar(270, r=big_diam / 2 + tool_diam / 2)

tl_tan = top_center + left_offset
tr_tan = top_center + tan_offset

rt_tan = right_center + tan_offset
rb_tan = right_center + tan_offset.over_x

bl_tan = bottom_center + left_offset
br_tan = bottom_center + tan_offset.over_x

sm_top_inset = Polar(th=150, r=small_inset + tool_diam / 2)
sm_bottom_inset = sm_top_inset.over_x
sm_right_inset = Polar(th=270, r=small_inset + tool_diam / 2)

sm_top_center = top + sm_top_inset
sm_bottom_center = bottom + sm_bottom_inset
sm_right_center = right + sm_right_inset


class P(Program):
    cut: float = 300
    plunge: float = 100
    safety: float = 10
    depth_per_pass: float = 0.5
    max_depth: float = 19.0

    def safe(self):
        self.feed = self.plunge
        with self.linear:
            self.z = self.safety

    def depth(self, to):
        self.feed = self.plunge
        with self.linear:
            self.z = to

    def outline(self):
        self.feed = self.cut

        with self.arc_cw:
            self.x = tr_tan.x
            self.y = tr_tan.y
            self.i = top_center.x - tl_tan.x
            self.j = top_center.y - tl_tan.y

        with self.linear:
            self.x = rt_tan.x
            self.y = rt_tan.y

        with self.arc_cw:
            self.x = rb_tan.x
            self.y = rb_tan.y
            self.i = right_center.x - rt_tan.x
            self.j = right_center.y - rt_tan.y

        with self.linear:
            self.x = br_tan.x
            self.y = br_tan.y

        with self.arc_cw:
            self.x = bl_tan.x
            self.y = bl_tan.y
            self.i = bottom_center.x - br_tan.x
            self.j = bottom_center.y - br_tan.y

        with self.linear:
            self.x = tl_tan.x
            self.y = tl_tan.y

    def inner(self):
        # cut top line
        self.feed = self.cut
        with self.linear:
            self.goto(x=sm_top_center.x, y=sm_top_center.y)

        # center
        self.feed = self.cut * 3
        with self.linear:
            self.move(x=-sm_top_center.x, y=-sm_top_center.y)

        # cut right line
        self.feed = self.cut
        with self.linear:
            self.goto(x=sm_right_center.x, y=sm_right_center.y)

        # center
        self.feed = self.cut * 3
        with self.linear:
            self.move(x=-sm_right_center.x, y=-sm_right_center.y)

        # cut bottom line
        self.feed = self.cut
        with self.linear:
            self.feed = self.cut
            self.goto(x=sm_bottom_center.x, y=sm_bottom_center.y)

        # center
        self.feed = self.cut * 3
        with self.linear:
            self.move(x=-sm_bottom_center.x, y=-sm_bottom_center.y)

    def go(self):
        # home to center
        with self.rapid:
            self.goto(x=0, y=0, z=self.safety)

        # cut out inner
        x = 0
        while x <= self.max_depth:
            self.depth(-x)
            self.inner()
            x += self.depth_per_pass
        self.safe()

        # home to outline start
        with self.rapid:
            self.goto(x=tl_tan.x, y=tl_tan.y)

        # engage outline
        x = 0
        while x <= self.max_depth:
            self.depth(-x)
            self.outline()
            x += self.depth_per_pass
        self.safe()

        # home to center
        with self.rapid:
            self.goto(x=0, y=0)


p = P()
p.go()
for command in p.commands:
    print(command)
