from . import Program


class Foo(Program):
    x = 10
    x = 30
    x += 20
    y = 20
    y += 10
    x, y = 10, 30
    x += 10
    x += 10
    x += 10
    x += 10


for command in Foo.commands:
    print(command)
