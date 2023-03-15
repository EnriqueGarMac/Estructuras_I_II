import matplotlib.pyplot as plt
from math import atan2, sin, cos, sqrt, pi, degrees
# Ref: http://paulbourke.net/geometry/polygonmesh/

class Cross_section:
    """
    Calculador de secciones

    :ivar EA: Standard axial stiffness of elements, default=15,000
    :ivar EI: Standard bending stiffness of elements, default=5,000
    :ivar figsize: (tpl) Matplotlibs standard figure size
    :ivar element_map: (dict) Keys are the element ids, values are the element objects
    :ivar node_map: (dict) Keys are the node ids, values are the node objects.
    :ivar node_element_map: (dict) maps node ids to element objects.
    :ivar loads_point: (dict) Maps node ids to point loads.
    :ivar loads_q: (dict) Maps element ids to q-loads.
    :ivar loads_moment: (dict) Maps node ids to moment loads.
    :ivar loads_dead_load: (set) Element ids that have a dead load applied.
    """

    def __init__(
        self,
        a: float = 0.0,
        Ixx: float = 0.0,
        Iyy: float = 0.0,
        Ixy: float = 0.0,
        I1: float = 0.0,
        I2: float = 0.0,
        theta: float = 0.0,
        cx: float = 0.0,
        cy: float = 0.0,
        pts: list = [],
    ):
      self.a = a
      self.cx = cx
      self.cy = cy
      self.Ixx = Ixx
      self.Iyy = Iyy
      self.Ixy = Ixy
      self.I1 = I1
      self.I2 = I2
      self.theta = theta
    def area(self):
      'Area of cross-section.'
      pts = self.pts
      if pts[0] != pts[-1]:
        pts = pts + pts[:1]
      x = [ c[0] for c in pts ]
      y = [ c[1] for c in pts ]
      s = 0
      for i in range(len(pts) - 1):
        s += x[i]*y[i+1] - x[i+1]*y[i]
      self.a = s/2.
      return s/2.


    def centroid(self):
      'Location of centroid.'
      pts = self.pts
      if pts[0] != pts[-1]:
        pts = pts + pts[:1]
      x = [ c[0] for c in pts ]
      y = [ c[1] for c in pts ]
      sx = sy = 0
      a = self.area()
      for i in range(len(pts) - 1):
        sx += (x[i] + x[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
        sy += (y[i] + y[i+1])*(x[i]*y[i+1] - x[i+1]*y[i])
      self.cx = sx/(6.*a)
      self.cy = sy/(6.*a)
      return sx/(6*a), sy/(6*a)


    def inertia(self):
      'Moments and product of inertia about centroid.'
      pts = self.pts
      if pts[0] != pts[-1]:
        pts = pts + pts[:1]
      x = [ c[0] for c in pts ]
      y = [ c[1] for c in pts ]
      sxx = syy = sxy = 0
      a = self.area()
      cx, cy = self.centroid()
      for i in range(len(pts) - 1):
        sxx += (y[i]**2 + y[i]*y[i+1] + y[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
        syy += (x[i]**2 + x[i]*x[i+1] + x[i+1]**2)*(x[i]*y[i+1] - x[i+1]*y[i])
        sxy += (x[i]*y[i+1] + 2*x[i]*y[i] + 2*x[i+1]*y[i+1] + x[i+1]*y[i])*(x[i]*y[i+1] - x[i+1]*y[i])
      self.Ix = sxx/12 - a*cy**2
      self.Iy = syy/12 - a*cx**2
      self.Pxy = sxy/24 - a*cx*cy
      return sxx/12 - a*cy**2, syy/12 - a*cx**2, sxy/24 - a*cx*cy


    def principal(self):
      'Principal moments of inertia and orientation.'
      Ixx = self.Ixx
      Iyy = self.Iyy
      Ixy = self.Ixy
      avg = (Ixx + Iyy)/2
      diff = (Ixx - Iyy)/2      # signed
      I1 = avg + sqrt(diff**2 + Ixy**2)
      I2 = avg - sqrt(diff**2 + Ixy**2)
      theta = atan2(-Ixy, diff)/2
      self.I1 = I1
      self.I2 = I2
      self.theta = theta
      return I1, I2, theta


    def calculate_section(self):
      'Text summary of cross-sectional properties.'
      
      a = self.area()
      self.a = a
      cx, cy = self.centroid()
      self.cx = cx
      self.cy = cy
      Ixx, Iyy, Ixy = self.inertia()
      self.Ixx = Ixx
      self.Iyy = Iyy
      self.Ixy = Ixy
      I1, I2, theta = self.principal()
      self.I1 = I1
      self.I2 = I2
      self.theta = theta
      summ = """Area
      A = {}
    Centroid
      cx = {}
      cy = {}
    Moments and product of inertia
      Ixx = {}
      Iyy = {}
      Ixy = {}
    Principal moments of inertia and direction
      I1 = {}
      I2 = {}
      θ︎ = {}°""".format(a, cx, cy, Ixx, Iyy, Ixy, I1, I2, degrees(theta))
      return summ

 
    def plot(self, pts, basename='section', format='none', size=(8, 8), dpi=100):
      'Draw an outline of the cross-section with centroid and principal axes.'
      pts = self.pts
      if pts[0] != pts[-1]:
        pts = pts + pts[:1]
      x = [ c[0] for c in pts ]
      y = [ c[1] for c in pts ]
  
      # Get the bounds of the cross-section
      minx = min(x)
      maxx = max(x)
      miny = min(y)
      maxy = max(y)
  
      # Whitespace border is 5% of the larger dimension
      b = .05*max(maxx - minx, maxy - miny)
  
      # Get the properties needed for the centroid and principal axes
      cx, cy = self.centroid()
      i = self.inertia()
      p = self.principal()
  
      # Principal axes extend 10% of the minimum dimension from the centroid
      length = min(maxx-minx, maxy-miny)/10
      a1x = [cx - length*cos(p[2]), cx + length*cos(p[2])]
      a1y = [cy - length*sin(p[2]), cy + length*sin(p[2])]
      a2x = [cx - length*cos(p[2] + pi/2), cx + length*cos(p[2] + pi/2)]
      a2y = [cy - length*sin(p[2] + pi/2), cy + length*sin(p[2] + pi/2)]
  
      # Plot and save
      # Axis colors chosen from http://mkweb.bcgsc.ca/colorblind/
      fig, ax = plt.subplots(figsize=size)
      ax.plot(x, y, 'k*-', lw=2)
      ax.plot(a1x, a1y, '-', color='#0072B2', lw=2)     # blue
      ax.plot(a2x, a2y, '-', color='#D55E00')           # vermillion
      ax.plot(cx, cy, 'ko', mec='k')
      ax.set_aspect('equal')
      plt.xlim(xmin=minx-b, xmax=maxx+b)
      plt.ylim(ymin=miny-b, ymax=maxy+b)
      if format == 'none':
          plt.show()
      else:
        filename = basename + '.' + format
        plt.savefig(filename, format=format, dpi=dpi)
        plt.close()
