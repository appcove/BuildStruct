#!/usr/bin/python3
# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab



import BuildStruct as BS






Model = BS.Model(Path=__file__+'.scad')
Model += BS.Building()


Model()



