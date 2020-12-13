# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab

#from solid import scad_render
#from solid import objects #import cube, cylinder, difference, translate, union
#from solid.utils import right, part, rotate, color

import solid.objects
import solid.utils
import sys
import typing
import math


class NodeType(dict):
  nextval = 0
  Parent = None
  def __init__(self):
    super().__init__()
    self.Parent = None

  def __setitem__(self, key, value):
    if not isinstance(value, NodeType):
      raise TypeError(f'May only set a NodeType, not {type(value)}.')

    if key is ...:
      NodeType.nextval += 1
      key = NodeType.nextval
     
    value.Parent = self
    super().__setitem__(key, value)

  def __setattr__(self, key, value):
    if not hasattr(type(self), key):
      raise AttributeError(f'Attributes must first be defined at the type level on object {self} of type {type(self)} with attribute {key}')
    return super().__setattr__(key, value)

  def Die(self, message):
    print()
    print('ⓧ  ' + str(message))
    print()
    sys.exit(1)

class Model(NodeType):
  SEGMENTS = 48
  Output = None
  Path = None

  def __init__(self, *, Path):
    super().__init__()
    self.Path = Path
    
  def __call__(self):
    part = solid.utils.part()

    for node in self.values():
      print(node)
      part(node())
    
    self.Output = solid.scad_render(part, file_header=f'$fn = {self.SEGMENTS};')

    if self.Path: 
      with open(self.Path, 'wt') as f:
        f.write(self.Output)

    return part



class PerimeterSegment():
  def __init__(self, Angle, Length):
    self.Angle = Angle
    self.Length = Length
    self.X1 = None
    self.Y1 = None
    self.X2 = None
    self.Y2 = None

class Building(NodeType):
  Perimeter = None
  ExteriorWallWidth = 5.5
  SillPlateThickness = 1.5
  SlabThickness = 6
  
  def __init__(self):
    super().__init__()
    self.Perimeter = []
    self['Foundation'] = Foundation()
    self['SillPlate'] = SillPlate()
    self['ExteriorWalls1'] = ExteriorWalls()

  def AddPerimeterSegment(self, *, Angle, Length):
    self.Perimeter.append(PerimeterSegment(Angle, Length))
 
  def __call__(self):
    # Validate Perimeter ends where it starts
    x,y = 0,0
    print(f'Validating Perimeter from 0,0:')
    for ps in self.Perimeter:
      ps.X1 = x
      ps.Y1 = y
      x += math.cos(math.radians(ps.Angle)) * ps.Length
      y += math.sin(math.radians(ps.Angle)) * ps.Length
      ps.X2 = x
      ps.Y2 = y
      print(f'►  Added {ps.Length} @ {ps.Angle} for new location of ({round(x,3)},{round(y,3)})')
    if (round(x,3), round(y,3)) != (0,0):
      self.Die(f'Perimeter is not closed because it ended at ({round(x,3)},{round(y,3)})')
    print(f'►  Perimeter validation success!')
    print()
      
   
    # Put it all together!

    part = solid.utils.part()
    
    if 'Foundation' in self:
      part(self['Foundation']())
    
    if 'SillPlate' in self:
      part(self['SillPlate']())
    
    if 'ExteriorWalls1' in self:
      part(self['ExteriorWalls1']())

    return part
   

class Foundation(NodeType):
  SlabThickness = None
  def __call__(self):
    self.SlabThickness = self.SlabThickness or self.Parent.SlabThickness

    p = solid.polygon([(ps.X2, ps.Y2) for ps in self.Parent.Perimeter])
    p = solid.linear_extrude(self.SlabThickness)(p)
    p = solid.utils.down(self.SlabThickness)(p)
    p = solid.color([.3,.3,.3])(p)
    return p    


class SillPlate(NodeType):
  Thickness = None
  Width = None
  
  def __call__(self):
    self.Width = self.Width or self.Parent.ExteriorWallWidth
    self.Thickness = self.Thickness or self.Parent.SillPlateThickness

    part = solid.part()
    for ps in self.Parent.Perimeter:
      p = solid.cube([ps.Length, self.Width, self.Thickness])
      p = solid.rotate(ps.Angle)(p)
      p = solid.translate([ps.X1, ps.Y1])(p)
      p = solid.color([0,0,1])(p)
      part(p)
    return part 


class ExteriorWalls(NodeType):
  Width = None
  Thickness = 2
  def __call__(self):
    self.Width = self.Width or self.Parent.ExteriorWallWidth

    part = solid.part()
    for ps in self.Parent.Perimeter:
      part2 = solid.part()

      p = solid.cube([ps.Length, self.Width, self.Thickness])
      p = solid.translate([0, 0, 2])(p)
      p = solid.color([0,1,0])(p)
      part2(p)
      
      p = solid.cube([ps.Length, self.Width, self.Thickness])
      p = solid.translate([0,0,144])(p)
      p = solid.color([0,1,0])(p)
      part2(p)
      
      for i in list(range(0, ps.Length-4, 24)) + [ps.Length - 2]:
        p = solid.cube([2, self.Width, 144-4])
        p = solid.translate([i,0,4])(p)
        p = solid.color([0,1,0])(p)
        part2(p)
      
      part2 = solid.rotate(ps.Angle)(part2)
      part2 = solid.translate([ps.X1, ps.Y1, 0])(part2)
      
      

      part(part2)
        

    return part 


class Stud(NodeType):
  def __init__(self):
    super().__init__()
  
  def __call__(self):
    cube = solid.objects.cube([1.5, 6, 144])
    return cube










