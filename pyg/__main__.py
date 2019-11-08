from . import Program

p = Program()
p.feed = 300
p.x = 0
p.x = 10

p.x -= 10
p.x = 10
p.move(0)
p.goto(x=0, y=10)

for command in p.commands:
    print(command)
