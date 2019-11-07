from . import Program

p = Program()
p.relative = True
p.x = 0
p.x = 10

p.x += 10
p.x = 10



for command in p.commands:
    print(command)
