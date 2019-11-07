__version__ = "0.1.0"


class Namespace(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.commands = []
        self.relative = False
        super().__setitem__("commands", self.commands)

    def append(self, cmd):
        self.commands.append(cmd)

    def c_x(self, to=None):
        if to is None:
            self["relative"] = True
            return 0

        self.append(f"X{to}")

    def c_y(self, to=None):
        if to is None:
            self["relative"] = True
            return 0

        self.append(f"Y{to}")

    def c_z(self, to=None):
        if to is None:
            self["relative"] = True
            return 0

        self.append(f"Z{to}")

    def c_relative(self, to):
        if self.relative != to:
            self.append(f"relative = {to}")
            self.relative = to

    def c_goto(self):
        def fn(x=None, y=None, z=None):
            self["relative"] = False
            if x is not None:
                self["x"] = x

            if y is not None:
                self["y"] = y

            if z is not None:
                self["z"] = z

        return fn

    def c_move(self):
        def fn(x=None, y=None, z=None):
            self["relative"] = True
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
