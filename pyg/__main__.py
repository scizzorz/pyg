from . import Program


class Foo(Program):
    goto(0, 0)
    move(10, 20)
    move(20, 30)


for command in Foo.commands:
    print(command)
