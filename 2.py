#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab


from BuildStruct import *


M = Model()



M.Wall(X=0, Y=0, A=0, L=230, H=96)
M.Wall(X=230, Y=0, A=90, L=230, H=96, StartOffset=True, EndOffset=True)
M.Wall(X=230, Y=230, A=180, L=230, H=96)
M.Wall(X=0, Y=230, A=270, L=230, H=96, StartOffset=True, EndOffset=True)



M.Write(__file__ + '.scad')


