# vim:fileencoding=utf-8:ts=2:sw=2:sts=2:expandtab



from . import *

def wallrange(start, stop, *, StudSpacing=16, StudThickness=1.5):
  i = start
  while i < stop:
    yield i
    i += step
  yield stop



class Wall(Part):
  def __init__(self, *, X, Y, Z=0, A, L, H=96, StartOffset=False, EndOffset=False):
    super().__init__()
    self.X = X
    self.Y = Y
    self.Z = Z
    self.A = A
    self.L = L
    self.H = H
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
      p(translate([x,0,self.StudThickness])(cube([self.StudThickness, self.StudWidth, self.H-self.StudThickness*2])))
      offset += self.StudSpacing
    x = self.L - self.StudThickness - self.EndOffset  
    p(translate([x,0,self.StudThickness])(cube([self.StudThickness, self.StudWidth, self.H-self.StudThickness*2])))

    p(translate([self.StartOffset,0,0])(cube([self.L - self.StartOffset - self.EndOffset, self.StudWidth, self.StudThickness])))
    p(translate([self.StartOffset,0,self.H-self.StudThickness])(cube([self.L - self.StartOffset - self.EndOffset, self.StudWidth, self.StudThickness])))

    r = rotate(self.A)(p)
    t = translate([self.X, self.Y, self.Z])(r)

    z = color(self.C)(t)

    self(z)





    return super().Generate()
