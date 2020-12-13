#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab



import BuildStruct as BS






Model = BS.Model(Path=__file__+'.scad')

Building = Model['Building'] = BS.Building()
Building.SillPlateThickness = 2
Building.ExteriorWallWidth = 6

Building.AddPerimeterSegment(Angle=0, Length=40*12)
Building.AddPerimeterSegment(Angle=90, Length=24*12)
Building.AddPerimeterSegment(Angle=180, Length=40*12)
Building.AddPerimeterSegment(Angle=270, Length=24*12)






Model()



