from . import Program

p = Program()

p.feed = 300
p.goto(x=-10, y=0)
p.arc_cw
p.goto(x=10, y=0)
p.goto(x=-10, y=0)
p.rapid
p.goto(0, 0)

for command in p.commands:
    print(command)
