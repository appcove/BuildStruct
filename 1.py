#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab


import sys
from solid import scad_render
from solid.objects import cube, cylinder, difference, translate, union
from solid.utils import right, part

SEGMENTS = 24

M = []

for i in range(0,240,2):
  M.append(translate([i,0,0])(cube([2, 3.5, 96])))

a = part()(*M)







# Adding the file_header argument as shown allows you to change
# the detail of arcs by changing the SEGMENTS variable.  This can
# be expensive when making lots of small curves, but is otherwise
# useful.
file_out = scad_render(a, file_header=f'$fn = {SEGMENTS};')

with open(__file__ + '.scad', 'wt') as f:
  f.write(file_out)


