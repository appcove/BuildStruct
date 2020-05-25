#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab


from Core import *


M = Model()



wall1 = Assembly()
for i in range(0,240,16):
  wall1(translate([i,0,0])(cube([1.5, 3.5, 96])))

wall2 = Assembly()
for i in range(0,240,16):
  wall2(translate([i,240,0])(cube([1.5, 3.5, 96])))


M(wall1)
M(wall2)

M.Write(__file__ + '.scad')


