import FreeCAD as App
import Part
from FreeCAD import Vector as V


doc = App.newDocument('bevel_test')

box = Part.makeBox(10, 10, 2)
cyl = Part.makeCylinder(1, 3, V(5, 5, -0.5)) 
box = box.cut(cyl)
box = box.makeFillet(0.3, box.Edges)
Part.show(box, 'Box')

doc.saveAs('bevel_test.FCStd')
