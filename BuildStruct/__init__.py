# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab

#from solid import scad_render
#from solid import objects #import cube, cylinder, difference, translate, union
#from solid.utils import right, part, rotate, color

import solid.objects
import solid.utils



class Node(list):
  def __iadd__(self, other):
    self.append(other)
    return self


class Model(Node):
  def __init__(self, *, Path):
    super().__init__()
    self.SEGMENTS = 48
    self.Output = None
    self.Path = Path
    
  def __call__(self):
    part = solid.utils.part()

    for node in self:
      part(node())
    
    self.Output = solid.scad_render(part, file_header=f'$fn = {self.SEGMENTS};')

    if self.Path: 
      with open(self.Path, 'wt') as f:
        f.write(self.Output)

    return part



class Building(Node):
  def __init__(self):
    super().__init__()
    self.Studs = []
    self.Studs.append(Stud())

  def __call__(self):
    part = solid.utils.part()

    for stud in self.Studs:
      part(stud())

    return part
    
  

class Stud(Node):
  def __init__(self):
    super().__init__()
  
  def __call__(self):
    cube = solid.objects.cube([1.5, 6, 144])
    import pdb; pdb.set_trace()
    return cube







