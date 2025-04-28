# run with `freecadcmd filename.py`. freecadcmd is found in
# the FreeCAD folder; add it to path to make the freecadcmd
# available in your path

import FreeCAD as App
import Part
from FreeCAD import Vector as V

doc = App.newDocument('extrusion_example')

# 1. Define the points of the trapezoid in the XY plane
p1 = V(0, 0, 0)
p2 = V(10, 0, 0)
p3 = V(8, 5, 0)
p4 = V(2, 5, 0)

# 2. Create the edges of a closed trapezoid
edge1 = Part.LineSegment(p1, p2).toShape()
edge2 = Part.LineSegment(p2, p3).toShape()
edge3 = Part.LineSegment(p3, p4).toShape()
edge4 = Part.LineSegment(p4, p1).toShape()

# 3. Create the wire from the edges
trapezoid_wire = Part.Wire([edge1, edge2, edge3, edge4])

# 4. Create the face from the wire
trapezoid_shape = Part.Face(trapezoid_wire)

# 5. Define the extrusion direction and length
extrude_dir = V(1, 1, 1)
extrude_length = 10  # millimeters

# 6. Extrude the trapezoid using Part.extrude
extruded_shape = trapezoid_shape.extrude(extrude_dir * extrude_length)

# 7. Add the extruded shape to the document
Part.show(extruded_shape)

doc.saveAs('ExtrusionExample.FCStd')
