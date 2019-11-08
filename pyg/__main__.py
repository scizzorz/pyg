from . import Program
from math import sqrt

side = 100
height = side * sqrt(3) / 2
offx = -height / 3
offy = -side / 2

top = dict(x=offx, y=offy)
bottom = dict(x=offx, y=offy + side)
right = dict(x=offx + height, y=offy + side / 2)

p = Program()
p.goto(**top)
with p:
  p.feed = 300
  p.linear
p.goto(**bottom)
p.goto(**right)
p.goto(**top)

for command in p.commands:
    print(command)
