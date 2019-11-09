__version__ = "0.1.0"

from contextlib import contextmanager
from enum import Enum


class Axis:
    def __init__(self, program, axis):
        self.axis = axis
        self.program = program

    def push(self, val):
        self.program.push(f"{self.axis}{val:.3f}")

    def __iadd__(self, val):
        if val is not None:
            self.program.relative
            self.push(val)

    def __isub__(self, val):
        if val is not None:
            self.program.relative
            self.push(-val)


class Movement(Enum):
    absolute = 90  # G90
    relative = 91  # G91

    @property
    def cmd(self):
        return f"G{self.value}"
        return f"G{self.value} ; movement = {self.name}"


class Measurement(Enum):
    imperial = 20  # G20
    metric = 21  # G21

    @property
    def cmd(self):
        return f"G{self.value}"
        return f"G{self.value} ; measurement = {self.name}"


class Motion(Enum):
    rapid = 0  # G0
    linear = 1  # G1
    arc_cw = 2  # G2
    arc_ccw = 3  # G3

    @property
    def cmd(self):
        return f"G{self.value}"
        return f"G{self.value} ; motion = {self.name}"


class Plane(Enum):
    xy = 17  # G17
    xz = 18  # G18
    yz = 19  # G19

    @property
    def cmd(self):
        return f"G{self.value}"
        return f"G{self.value} ; plane = {self.name}"


class Program:
    def __init__(self):
        self.bufstack = []
        self.buffer = []
        self.commands = []

        self._movement = None
        self._measurement = None
        self._motion = None
        self._plane = None

        # feed rate
        self._feed = None

        # tool coordinates
        self._x = Axis(self, "X")
        self._y = Axis(self, "Y")
        self._z = Axis(self, "Z")

        # initializes everything
        with self.rapid:
            self.movement = Movement.absolute
            self.measurement = Measurement.metric
            self.plane = Plane.xy

    def push(self, cmd):
        self.buffer.append(cmd)

    def squash(self):
        if len(self.buffer) == 0:
            return

        self.commands.append(" ".join(self.buffer))
        self.buffer = []

    def drop(self):
        self.buffer = []

    def push_motion(self):
        self.push(self.motion.cmd)

    def push_measurement(self):
        self.push(self.measurement.cmd)

    def push_movement(self):
        self.push(self.movement.cmd)

    def push_plane(self):
        self.push(self.plane.cmd)

    def push_feed(self):
        self.push(f"F{self._feed}")

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, val):
        if val != self._movement:
            with self:
                self._movement = val
                self.push_movement()

    @property
    def motion(self):
        return self._motion

    @motion.setter
    def motion(self, val):
        if val != self._motion:
            self._motion = val
            self.push_motion()

    @property
    def plane(self):
        return self._plane

    @plane.setter
    def plane(self, val):
        if val != self._plane:
            self._plane = val
            self.push_plane()

    @property
    def measurement(self):
        return self._measurement

    @measurement.setter
    def measurement(self, val):
        if val != self._measurement:
            self._measurement = val
            self.push_measurement()

    @property
    def feed(self):
        return self._feed

    @feed.setter
    def feed(self, val):
        if self._feed != val:
            with self:
                self._feed = val
                self.push_feed()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        if val is not None:
            self.absolute
            self._x.push(val)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        if val is not None:
            self.absolute
            self._y.push(val)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, val):
        if val is not None:
            self.absolute
            self._z.push(val)

    @property
    def relative(self):
        self.movement = Movement.relative

    @property
    def absolute(self):
        self.movement = Movement.absolute

    @property
    def metric(self):
        self.measurement = Measurement.metric

    @property
    def imperial(self):
        self.measurement = Measurement.imperial

    @property
    @contextmanager
    def rapid(self):
        with self:
            self.motion = Motion.rapid
            yield

    @property
    @contextmanager
    def linear(self):
        with self:
            self.motion = Motion.linear
            yield

    @property
    def xy(self):
        self.plane = Plane.xy

    @property
    def xz(self):
        self.plane = Plane.xz

    @property
    def yz(self):
        self.plane = Plane.yz

    def move(self, x=None, y=None, z=None):
        self.x += x
        self.y += y
        self.z += z

    def goto(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def arc(self, motion, x=None, y=None, z=None, i=None, j=None, k=None):
        with self:
            self.motion = motion
            self.x = x
            self.y = y
            self.z = z
            if i is not None:
                self.push(f"I{i:.3f}")
            if j is not None:
                self.push(f"J{j:.3f}")
            if k is not None:
                self.push(f"K{k:.3f}")

    def arc_cw(self, **kwargs):
        self.arc(Motion.arc_cw, **kwargs)

    def arc_ccw(self, **kwargs):
        self.arc(Motion.arc_ccw, **kwargs)

    def __enter__(self):
        self.bufstack.append(self.buffer)
        self.buffer = []

    def __exit__(self, type, value, traceback):
        self.squash()
        self.buffer = self.bufstack.pop()
