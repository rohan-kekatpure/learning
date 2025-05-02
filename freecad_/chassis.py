import sys

from tensorflow.python.keras.initializers.initializers_v1 import HeUniform

sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')

import FreeCAD
import Part
from FreeCAD import Vector as V

def make_face_from_points(points):
    """
    Makes face from points. Points must be listed in CW or CCW
    ordering, otherwise resulting face may be self intersecting
    """

    # Append the first point as the last element
    # to make the closed wire necessary for a face
    points.append(points[0])    
    edges = []
    for i in range(len(points) - 1):
        line = Part.makeLine(points[i], points[i + 1])
        edges.append(line)

    wire = Part.Wire(edges)
    face = Part.Face(wire)
    return face

def mirror_shape(doc, source_shape, base_point, normal_vector):
    """
    If you use shape.mirror(base, normal) you get mirroring in
    the source objects _local_ coordinate system. This is not
    what we want. We want to mirror the shape in the _global_
    coordinate system. To get mirroring with respect to a global
    system, we need to do mirroring at the Part level, not the
    shape level. So we create a dummy part, mirror, then delete
    dummies.
    """
    sourceobj = doc.addObject('Part::Feature', '_source_dummy')
    sourceobj.Shape = source_shape
    targetobj = doc.addObject('Part::Mirroring', '_target_dummy')
    targetobj.Source = sourceobj
    targetobj.Normal = normal_vector
    targetobj.Base = base_point
    target_shape = targetobj.Shape
    doc.removeObject('_source_dummy')
    doc.removeObject('_target_dummy')
    return target_shape

def main():
    doc = App.newDocument('chassis')

    # Dimensions
    CLEARANCE = 5
    WIDTH = 80
    HEIGHT = 25
    OVERHANG = 10
    HCUT = 0
    VCUT = 5
    FLARE_LEN = 10
    MIDSECTION_LEN = 60
    TAPER_LEN = 10
    CASTER_LEN = 44
    CASTER_WID = 36
    CASTER_HT = 30
    BATTERY_SECTION_LEN = 30
    THICKNESS = 8
    CASTER_SCREW_DIA = 3
    


    # Create top body
    p1 = V(0, 0, 0)
    p2 = V(p1.x - WIDTH / 2, 0, 0)
    p3 = V(p2.x, p2.y + BATTERY_SECTION_LEN, 0)
    p4 = V(p3.x + OVERHANG, p3.y, 0)
    p5 = V(p4.x + HCUT, p4.y + VCUT, 0)
    p6 = V(p3.x, p5.y + FLARE_LEN, 0)
    p7 = V(p6.x, p6.y + MIDSECTION_LEN, 0)
    p8 = V(-CASTER_LEN / 2 - CLEARANCE, p7.y + TAPER_LEN, 0)
    p9 = V(p8.x, p8.y + 2 * CLEARANCE + CASTER_WID, 0)
    p10 = V(0, p9.y, 0)

    points = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    mirrored = [V(-p.x, p.y, p.z) for p in points[1: -1]]
    points.extend(reversed(mirrored))
    top_body = make_face_from_points(points)
    top_body = top_body.extrude(V(0, 0, 1) * THICKNESS)

    # left wheel attachment
    ljoint = Part.makeCylinder(THICKNESS, MIDSECTION_LEN, p6, V(0, 1, 0), 90)
    ljoint = ljoint.rotated(p6, V(0, 1, 0), -90)
    lwhlattach = Part.makeBox(
        THICKNESS, MIDSECTION_LEN, HEIGHT,
        V(p6.x - THICKNESS, p6.y, -HEIGHT)
    )
    lwhlattach = lwhlattach.fuse(ljoint)

    # right wheel attachment
    rwhlattach = mirror_shape(doc, lwhlattach, p1, V(1, 0, 0))


    chassis = top_body.fuse(lwhlattach).fuse(rwhlattach)
    Part.show(chassis, 'chassis')
    doc.saveAs('chassis.FCStd')

if __name__ == '__main__':
    main()





