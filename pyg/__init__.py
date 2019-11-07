__version__ = "0.1.0"

from enum import Enum


class Axis:
  def __init__(self, program, axis):
    self.axis = axis
    self.program = program

  def push(self, val):
    self.program.push(f"{self.axis}{val}")

  def __iadd__(self, val):
    self.program.relative = True
    self.push(val)

  def __isub__(self, val):
    self.program.relative = True
    self.push(-val)


class Movement(Enum):
  absolute = 90  # G90
  relative = 91  # G91

  @property
  def cmd(self):
    return f"G{self.value} ; movement = {self.name}"


class Measurement(Enum):
  imperial = 20  # G20
  metric = 21  # G21

  @property
  def cmd(self):
    return f"G{self.value} ; measurement = {self.name}"


class Motion(Enum):
  rapid = 0  # G0
  linear = 1  # G1
  arc_cw = 2  # G2
  arc_ccw = 3  # G3

  @property
  def cmd(self):
    return f"G{self.value} ; motion = {self.name}"


class Plane(Enum):
  xy = 17  # G17
  xz = 18  # G18
  yz = 19  # G19

  @property
  def cmd(self):
    return f"G{self.value} ; plane = {self.name}"


class Program:
  def __init__(self):
    self.commands = []
    self.movement = Movement.absolute
    self.measurement = Measurement.metric
    self.motion = Motion.rapid
    self.plane = Plane.xy
    self.feed = None
    self._x = Axis(self, "X")
    self._y = Axis(self, "Y")
    self._z = Axis(self, "Z")

  def push(self, cmd):
    self.commands.append(cmd)

  def push_movement(self):
    self.push(self.movement.cmd)

  @property
  def relative(self):
    return self.movement == Movement.relative

  @relative.setter
  def relative(self, val):
    if self.relative != val:
      self.movement = Movement.relative if val else Movement.absolute
      self.push_movement()

  @property
  def absolute(self):
    return self.movement == Movement.absolute

  @absolute.setter
  def absolute(self, val):
    if self.absolute != val:
      self.movement = Movement.absolute if val else Movement.relative
      self.push_movement()

  @property
  def x(self):
    return self._x

  @x.setter
  def x(self, val):
    if val is not None:
      self.absolute = True
      self._x.push(val)
