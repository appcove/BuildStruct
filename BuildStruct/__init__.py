# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab

from solid import scad_render
from solid.objects import cube, cylinder, difference, translate, union
from solid.utils import right, part, rotate, color



class Part():
  def __init__(self):
    super().__init__()
    self.Things = []

  def __call__(self, *things):
    self.Things += things

  def Generate(self):
    p = part()
    for thing in self.Things:
      if isinstance(thing, Part):
        p(thing.Generate())
      else:
        p(thing)
    return p
  

class Model(Part):
  def __init__(self):
    super().__init__()
    self.SEGMENTS = 48
    self.Output = None
    
  def __call__(self, thing):
    self.Things.append(thing)
    return thing

  def Render(self):
    p = self.Generate()
    self.Output = scad_render(p, file_header=f'$fn = {self.SEGMENTS};')
  
  def Write(self, path):
    if self.Output is None: 
      self.Render()
    with open(path, 'wt') as f:
      f.write(self.Output)

      
  def Wall(self, *args, **kwargs):
    return self(Modules.Wall(*args, **kwargs))
   

class Modules():
  from .Wall import Wall




