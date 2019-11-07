__version__ = "0.1.0"


class Axis:
  def __init__(self, ns, axis):
    self.val = 0
    self.axis = axis
    self.ns = ns

  def __add__(self, val):
    self.ns.c_relative()
    getattr(self.ns, f"c_{self.axis}")(val, False)

  def __iadd__(self, val):
    self.ns.c_relative()
    getattr(self.ns, f"c_{self.axis}")(val, False)

  def __isub__(self, val):
    self.ns.c_relative()
    getattr(self.ns, f"c_{self.axis}")(-val, False)


class Namespace(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = []
        self.relative = False
        self.x = Axis(self, "x")
        self.y = Axis(self, "y")
        self.z = Axis(self, "z")
        super().__setitem__("commands", self.commands)
        super().__setitem__("x", self.x)
        super().__setitem__("y", self.y)
        super().__setitem__("z", self.z)

    def append(self, cmd):
        self.commands.append(cmd)

    def c_x(self, to=None, abs=True):
        if to is None:
            return self.x

        if abs:
            self.c_absolute()

        self.append(f"X{to}")

    def c_y(self, to=None, abs=True):
        if to is None:
            return self.y

        if abs:
            self.c_absolute()

        self.append(f"Y{to}")

    def c_z(self, to=None, abs=True):
        if to is None:
            return self.z

        if abs:
            self.c_absolute()

        self.append(f"Z{to}")

    def c_relative(self, to=None):
        if not self.relative:
            self.append(f"relative = True")
            self.relative = True

    def c_absolute(self, to=None):
        if self.relative:
            self.append(f"relative = False")
            self.relative = False

    def c_goto(self):
        def fn(x=None, y=None, z=None):
            self.c_absolute()
            if x is not None:
                self.c_x(x)

            if y is not None:
                self.c_y(y)

            if z is not None:
                self.c_z(z)

        return fn

    def c_move(self):
        def fn(x=None, y=None, z=None):
            self.c_relative()
            if x is not None:
                self["x"] = x

            if y is not None:
                self["y"] = y

            if z is not None:
                self["z"] = z

        return fn

    def __getitem__(self, key):
        fn = getattr(self, f"c_{key}", None)
        if fn is not None:
            return fn()

        return super().__getitem__(key)

    def __setitem__(self, key, val):
        fn = getattr(self, f"c_{key}", None)
        if fn is not None:
            return fn(val)

        return super().__setitem__(key, val)


class ProgramMeta(type):
    def __prepare__(name, bases):
        return Namespace()


class Program(metaclass=ProgramMeta):
    pass
