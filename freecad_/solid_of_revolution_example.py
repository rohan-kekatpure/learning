import FreeCAD
import Part
from FreeCAD import Vector as V

doc = App.newDocument('solid_of_revolution')

radius = 10
center_width = 2 * radius
vnorm = V(0, 0, 1)

# left arc
x1, y1 = radius, radius
c1 = V(x1, y1, 0)
arcleft = Part.makeCircle(radius, c1, vnorm, 0, 270)

# right arc
x2, y2 = x1 + radius + center_width + radius, y1
c2 = V(x2, y2, 0)
arcright = Part.makeCircle(radius, c2, vnorm, 270, 180)

# line 1
l1_start = V(x1 + radius, y1, 0)
l1_end = V(x2 - radius, y2, 0)
l1 = Part.makeLine(l1_start, l1_end)

# line 2
l2_start = V(x1, y1 - radius, 0)
l2_end = V(x2, y2 - radius, 0)
l2 = Part.makeLine(l2_start, l2_end)

# Face
edges = [arcleft, l1, arcright, l2]
wire = Part.Wire(edges)
face = Part.Face(wire)
placement = App.Placement(
    App.Vector(0,-100,0),
    App.Rotation(App.Vector(0,0,1),0)
)
face.Placement = placement

# Solid of revolution
sarc = face.revolve(V(0, 0, 0), V(1, 0, 0), 90)
Part.show(sarc)

doc.saveAs('solid_of_revolution.FCStd')