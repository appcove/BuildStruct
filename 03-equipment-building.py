#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab


from BuildStruct import *


M = Model()



w = M.Wall(X=0, Y=0, A=0, L=12*40, H=12*12)
w.StudWidth = 6
w.StudThickness = 2

w = M.Wall(X=0, Y=12*24-6, A=0, L=12*40, H=12*12)
w.StudWidth = 6
w.StudThickness = 2

w = M.Wall(X=6, Y=0, A=90, L=12*24, H=12*12, StartOffset=True, EndOffset=True)
w.StudWidth = 6
w.StudThickness = 2

w = M.Wall(X=12*40, Y=0, A=90, L=12*24, H=12*12, StartOffset=True, EndOffset=True)
w.StudWidth = 6
w.StudThickness = 2

#M.Wall(X=230, Y=0, A=90, L=230, H=96, StartOffset=True, EndOffset=True)

M.Write(__file__ + '.scad')


