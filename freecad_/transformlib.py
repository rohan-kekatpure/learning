import sys

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


def tap(body, center, direction, thread_dia, thread_len, head_dia=0, head_len=0):
    screw = Part.makeCylinder(thread_dia / 2, thread_len, center, direction)
    if head_dia > 0:
        head = Part.makeCylinder(head_dia / 2, head_len, center, direction)
        screw = screw.fuse(head)
    body = body.cut(screw)
    return body
