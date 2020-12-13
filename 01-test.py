#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab



import BuildStruct as BS






Model = BS.Model(Path=__file__+'.scad')

Model['Building'] = BS.Building()
Model['Building'].AddPerimeterSegment(Angle=0, Length=40*12)
Model['Building'].AddPerimeterSegment(Angle=90, Length=24*12)
Model['Building'].AddPerimeterSegment(Angle=180, Length=40*12)
Model['Building'].AddPerimeterSegment(Angle=270, Length=24*12)



Model()



