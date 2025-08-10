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

def tap(body, center, axis, thread_dia, thread_len, head_dia=0, head_len=0):
    lhead = head_len
    ltot = head_len + thread_len
    if axis == V(0, 0, 1):
        thread_loc = V(center.x, center.y, center.z - ltot)
        head_loc = V(center.x, center.y, center.z - lhead)
    elif axis == V(0, 1, 0):
        thread_loc = V(center.x, center.y - ltot, center.z)
        head_loc = V(center.x, center.y - lhead, center.z)
    elif axis == V(1, 0, 0):
        thread_loc = V(center.x - ltot, center.y, center.z)
        head_loc = V(center.x - lhead, center.y, center.z)
    else:
        raise ValueError('tap axis is not x, y or z')

    screw = Part.makeCylinder(thread_dia / 2, thread_len, thread_loc, axis)
    if head_dia > 0:

        head = Part.makeCylinder(head_dia / 2, head_len, head_loc, axis)
        screw = screw.fuse(head)
    body = body.cut(screw)
    return body


def main():
    doc = App.newDocument('chassis')

    # Dimensions
    CLEARANCE = 10
    WIDTH = 80
    HEIGHT = 30
    OVERHANG = 10
    CASTER_SCREW_THREAD_DIA = 3
    CASTER_SCREW_HEAD_DIA = 5
    PCB_SCREW_THREAD_DIA = 4
    PCB_SCREW_HEAD_DIA = 6
    PCB_SCREW_HSPACING = 38.5
    PCB_SCREW_VSPACING = 86.6
    CASTER_SCREW_HSEP = 30
    CASTER_SCREW_VSEP = 24
    CASTER_HT = 34
    WHEEL_DIA = 66
    GEARBOX_AXLE_DIA = 7.5
    GEARBOX_AXLE_HEIGHT = HEIGHT / 2
    GEARBOX_SCREW_DIA = 3
    GEARBOX_AXLE_SCREW_HSEP = 20
    GEARBOX_AXLE_SCREW_VSEP = 8.75
    PCB_WID = 50
    PCB_LEN = 90
    VCUT = 5
    FLARE_LEN = 10
    MIDSECTION_LEN = PCB_LEN
    TAPER_LEN = 10
    BATTERY_SECTION_LEN = 30
    THICKNESS = 8


    # Create top body
    p1 = V(0, 0, 0)
    p2 = V(p1.x - WIDTH / 2, 0, 0)
    p3 = V(p2.x, p2.y + BATTERY_SECTION_LEN, 0)
    p4 = V(p3.x + OVERHANG, p3.y, 0)
    p5 = V(p4.x, p4.y + VCUT, 0)
    p6 = V(p3.x, p5.y + FLARE_LEN, 0)
    p7 = V(p6.x, p6.y + MIDSECTION_LEN, 0)
    p8 = V(-CASTER_SCREW_HSEP / 2 - CLEARANCE, p7.y + TAPER_LEN, 0)
    p9 = V(p8.x, p8.y + 2 * CLEARANCE + CASTER_SCREW_VSEP, 0)
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

    # Caster buffer
    gbx_axle_z = -HEIGHT + GEARBOX_AXLE_HEIGHT
    h = abs(gbx_axle_z) + WHEEL_DIA / 2. - CASTER_HT
    caster_mesa = Part.makeBox(
        abs(2 * p8.x),
        p9.y - p8.y,
        h,
        V(p8.x, p8.y, -h)
    )
    chassis = chassis.fuse(caster_mesa)

    # Caster wheel screws
    cwsargs = (
        V(0, 0, 1),
        CASTER_SCREW_THREAD_DIA,
        4 * THICKNESS,
        CASTER_SCREW_HEAD_DIA,
        2
    )
    cws1 = V(p8.x + CLEARANCE, p8.y + CLEARANCE, p8.z + THICKNESS)
    cws2 = V(cws1.x, cws1.y + CASTER_SCREW_VSEP, cws1.z)
    cws3 = V(cws2.x + CASTER_SCREW_HSEP, cws2.y, cws2.z)
    cws4 = V(cws1.x + CASTER_SCREW_HSEP, cws1.y, cws1.z)
    for loc in [cws1, cws2, cws3, cws4]:
        chassis = tap(chassis, loc, *cwsargs)

    # PCB screws
    pcbsargs = (
        V(0, 0, 1),
        PCB_SCREW_THREAD_DIA,
        2 * THICKNESS
    )
    pcbs1 = V(p1.x - PCB_SCREW_HSPACING / 2, p6.y, p6.z + THICKNESS)
    pcbs2 = V(pcbs1.x, pcbs1.y + PCB_SCREW_VSPACING, pcbs1.z)
    pcbs3 = V(pcbs2.x + PCB_SCREW_HSPACING, pcbs2.y, pcbs2.z)
    pcbs4 = V(pcbs1.x + PCB_SCREW_HSPACING, pcbs1.y, pcbs1.z)
    for loc in [pcbs1, pcbs2, pcbs3, pcbs4]:
        chassis = tap(chassis, loc, *pcbsargs)

    # Gearbox mounting
    gbx_left_axle = V(
        p6.x,
        p6.y + 2 * CLEARANCE,
        gbx_axle_z
    )

    gbx_left_s1 = V(
        gbx_left_axle.x,
        gbx_left_axle.y + GEARBOX_AXLE_SCREW_HSEP,
        gbx_left_axle.z + GEARBOX_AXLE_SCREW_VSEP
    )

    gbx_left_s2 = V(
        gbx_left_axle.x,
        gbx_left_axle.y + GEARBOX_AXLE_SCREW_HSEP,
        gbx_left_axle.z - GEARBOX_AXLE_SCREW_VSEP
    )

    gbx_right_axle = V(
        -gbx_left_axle.x + THICKNESS,
        gbx_left_axle.y,
        gbx_left_axle.z
    )

    gbx_right_s1 = V(
        gbx_right_axle.x,
        gbx_left_s1.y,
        gbx_left_s1.z
    )

    gbx_right_s2 = V(
        gbx_right_axle.x,
        gbx_left_s2.y,
        gbx_left_s2.z
    )

    gbx_axle_locations = [
        gbx_left_axle,
        gbx_right_axle
    ]
    for loc in gbx_axle_locations:
        chassis = tap(chassis, loc, V(1, 0, 0), GEARBOX_AXLE_DIA, 2 * THICKNESS)

    gbx_screw_locations = [
        gbx_left_s1,
        gbx_left_s2,
        gbx_right_s1,
        gbx_right_s2
    ]
    for loc in gbx_screw_locations:
        chassis = tap(chassis, loc, V(1, 0, 0), GEARBOX_SCREW_DIA, 2 * THICKNESS)


    Part.show(chassis, 'chassis')
    doc.saveAs('chassis.FCStd')

if __name__ == '__main__':
    main()



