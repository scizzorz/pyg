from pyg import Program

max_x_offset = -820
max_y_offset = -360
max_z_offset = -65


class Surface(Program):
    min_x: float = -820
    max_x: float = 0
    min_y: float = -358
    max_y: float = 0
    cut: float = 900
    plunge: float = 100
    depth: float = 1.0
    tool_diam: float = 25.4
    overlap: float = 0.7

    def insert(self):
        self.feed = self.plunge
        with self.linear:
            self.z = -self.depth

    def extract(self):
        self.feed = self.plunge
        with self.linear:
            self.z = 0

    def surface(self, inset=0):
        self.feed = self.cut

        skip = (self.tool_diam * self.overlap) * inset

        with self.linear:
            self.y = self.min_y + skip

        with self.linear:
            self.x = self.min_x + skip

        with self.linear:
            self.y = self.max_y - skip

        with self.linear:
            self.x = self.max_y - skip - (self.tool_diam * self.overlap)

    def go(self):
        # home to center
        with self.rapid:
            self.goto(x=0, y=0, z=0)

        self.insert()
        for n in range(11):
            self.surface(n)
        self.extract()


p = Surface()
p.go()
for command in p.commands:
    print(command)
