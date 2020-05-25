# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab



from . import *

def wallrange(start, stop, *, StudSpacing=16, StudThickness=1.5):
  i = start
  while i < stop:
    yield i
    i += step
  yield stop



class Wall(Part):
  def __init__(self, *, X, Y, A, L, StartOffset=False, EndOffset=False):
    super().__init__()
    self.X = X
    self.Y = Y
    self.A = A
    self.L = L    
    self.C = [0.85, 0.7, 0.45]
    self.StudSpacing = 16
    self.StudThickness = 1.5
    self.StudWidth = 5.5
    self.StartOffset = StartOffset
    self.EndOffset = EndOffset


  def Generate(self):
    self.StartOffset = self.StudWidth if self.StartOffset is True else float(self.StartOffset)
    self.EndOffset = self.StudWidth if self.EndOffset is True else float(self.EndOffset)
    print(self.StartOffset)
    

    p = part()
    offset = 0 
    while offset < self.L - self.StudThickness - self.EndOffset:
      x = max(offset, self.StartOffset)
      p(translate([x,0,0])(cube([self.StudThickness, self.StudWidth, 96])))
      offset += self.StudSpacing
    x = self.L - self.StudThickness - self.EndOffset  
    p(translate([x,0,0])(cube([self.StudThickness, self.StudWidth, 96])))

    r = rotate(self.A)(p)
    t = translate([self.X, self.Y, 0])(r)

    z = color(self.C)(t)

    self(z)





    return super().Generate()
