# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab

from solid import scad_render
from solid.objects import cube, cylinder, difference, translate, union
from solid.utils import right, part

class Model():
  def __init__(self):
    self.SEGMENTS = 48
    self.Things = []
    self.Output = None


  def __call__(self, thing):
    self.Things.append(thing)

  def Render(self):
    p = part()
    for thing in self.Things:
      if isinstance(thing, Assembly):
        p(thing.Generate())
      else:
        p(thing)
        
    self.Output = scad_render(p, file_header=f'$fn = {self.SEGMENTS};')
 
  
  def Write(self, path):
    if self.Output is None: 
      self.Render()

    with open(path, 'wt') as f:
      f.write(self.Output)


class Assembly():
  def __init__(self):
    self.Things = []

  def Generate(self):
    p = part()
    p(*self.Things)
    return p

  def __call__(self, thing):
    self.Things.append(thing)




