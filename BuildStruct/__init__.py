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

  def Die(self, message):
    print()
    print('ⓧ  ' + str(message))
    print()
    sys.exit(1)

class Model(NodeType):
  def __init__(self, *, Path):
    super().__init__()
    self.SEGMENTS = 48
    self.Output = None
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
  def __init__(self):
    super().__init__()
    self.Perimeter = []
    self['Foundation'] = Foundation()
    self['SillPlate'] = SillPlate()

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
      
   
    # 
    part = solid.utils.part()
    part(self['Foundation']())
    part(self['SillPlate']())
    return part
   

class Foundation(NodeType):
  
  def __call__(self):
    p = solid.polygon([(ps.X2, ps.Y2) for ps in self.Parent.Perimeter])
    p = solid.linear_extrude(6)(p)
    p = solid.utils.down(6)(p)
    p = solid.color([.3,.3,.3])(p)
    return p    


class SillPlate(NodeType):
  
  def __call__(self):
    part = solid.part()
    for ps in self.Parent.Perimeter:
      p = solid.cube([ps.Length, 6, 2])
      p = solid.rotate(ps.Angle)(p)
      p = solid.translate([ps.X1, ps.Y1])(p)
      p = solid.color([0,0,1])(p)
      part(p)
    return part 




class Stud(NodeType):
  def __init__(self):
    super().__init__()
  
  def __call__(self):
    cube = solid.objects.cube([1.5, 6, 144])
    return cube










