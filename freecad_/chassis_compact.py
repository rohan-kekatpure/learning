import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')

import FreeCAD
import Part
from FreeCAD import Vector as V

import transformlib as T

def main():
    doc = App.newDocument('chassis')

    # Dimensions
    MARGIN = 10
    PCB_SCREW_HSPACING = 38.5
    PCB_SCREW_VSPACING = 86.6
    PCB_LEN = 90
    PCB_WID = 50
    PCB_SCREW_DIA = 4
    BODY_THICKNESS = 5

    CASTER_SCREW_HSEP = 24
    CASTER_SCREW_VSEP = 36
    CASTER_HT = 34
    CASTER_SCREW_THREAD_DIA = 3
    CASTER_SCREW_HEAD_DIA = 5
    CASTER_PCB_SCREW_VSEP = 10 * 0

    WHEEL_DIA = 66
    GEARBOX_AXLE_DIA = 7.5
    GEARBOX_SCREW_DIA = 3
    GEARBOX_AXLE_SCREW_HSEP = 20
    GEARBOX_SCREW_SEP = 17.5
    GEARBOX_AXLE_SCREW_VSEP = GEARBOX_SCREW_SEP / 2.
    GEARBOX_BODY_VERT_CLR = 5
    GEARBOX_SCREW_CLR = 10

    BED_ELEVATION = 2 * GEARBOX_BODY_VERT_CLR + GEARBOX_SCREW_SEP + GEARBOX_SCREW_DIA


    # Create top body
    p0 = V(0, 0, 0)
    p1 = V(p0.x - PCB_SCREW_HSPACING / 2, 0, 0)
    p2 = V(p1.x - PCB_SCREW_DIA / 2 - MARGIN, p1.y + PCB_SCREW_DIA / 2 + MARGIN, 0)
    p3 = V(p2.x, p2.y + PCB_SCREW_VSPACING, 0)
    p4 = V(p1.x, p3.y + PCB_SCREW_DIA / 2 + MARGIN, 0)
    p5 = V(p0.x, p4.y, 0)

    points = [p0, p1, p2, p3, p4, p5]
    mirrored = [V(-p.x, p.y, p.z) for p in points[1: -1]]
    points.extend(reversed(mirrored))
    top_body = T.make_face_from_points(points)
    top_body = top_body.extrude(V(0, 0, 1) * BODY_THICKNESS)

    # left wheel attachment
    ljoint = Part.makeCylinder(BODY_THICKNESS, PCB_SCREW_VSPACING, p2, V(0, 1, 0), 90)
    ljoint = ljoint.rotated(p2, V(0, 1, 0), -90)
    lwhlattach = Part.makeBox(
        BODY_THICKNESS, PCB_SCREW_VSPACING, BED_ELEVATION,
        V(p2.x - BODY_THICKNESS, p2.y, -BED_ELEVATION)
    )

    lwhlattach = lwhlattach.fuse(ljoint)

    # right wheel attachment
    rwhlattach = T.mirror_shape(doc, lwhlattach, p0, V(1, 0, 0))
    chassis = top_body.fuse(lwhlattach).fuse(rwhlattach)

    # Gearbox mounting
    gbx_left_s1 = V(
        p2.x,
        p2.y + GEARBOX_SCREW_CLR,
        - (GEARBOX_SCREW_DIA / 2 + GEARBOX_BODY_VERT_CLR)
    )

    gbx_left_s2 = V(
        gbx_left_s1.x,
        gbx_left_s1.y,
        gbx_left_s1.z - GEARBOX_SCREW_SEP
    )

    gbx_left_axle = V(
        gbx_left_s1.x,
        gbx_left_s1.y + GEARBOX_AXLE_SCREW_HSEP,
        gbx_left_s1.z - GEARBOX_AXLE_SCREW_VSEP
    )


    gbx_right_axle = V(
        -gbx_left_axle.x + BODY_THICKNESS,
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
        chassis = T.tap(chassis, loc, V(1, 0, 0), GEARBOX_AXLE_DIA, 2 * BODY_THICKNESS)

    gbx_screw_locations = [
        gbx_left_s1,
        gbx_left_s2,
        gbx_right_s1,
        gbx_right_s2
    ]
    for loc in gbx_screw_locations:
        chassis = T.tap(chassis, loc, V(1, 0, 0), GEARBOX_SCREW_DIA, 2 * BODY_THICKNESS)


    # # Caster buffer
    # gbx_axle_z = -BED_ELEVATION + gbx_left_axle.z
    # h = abs(gbx_axle_z) + WHEEL_DIA / 2. - CASTER_HT
    # caster_mesa = Part.makeBox(
    #     abs(2 * p8.x),
    #     p9.y - p8.y,
    #     h,
    #     V(p8.x, p8.y, -h)
    # )

    # chassis = chassis.fuse(caster_mesa)

    # PCB screws
    pcbsargs = (
        V(0, 0, 1),
        PCB_SCREW_DIA,
        2 * BODY_THICKNESS
    )

    pcbs1 = V(p0.x - PCB_SCREW_HSPACING / 2, p2.y, p0.z + BODY_THICKNESS)
    pcbs2 = V(pcbs1.x, pcbs1.y + PCB_SCREW_VSPACING, pcbs1.z)
    pcbs3 = V(pcbs2.x + PCB_SCREW_HSPACING, pcbs2.y, pcbs2.z)
    pcbs4 = V(pcbs1.x + PCB_SCREW_HSPACING, pcbs1.y, pcbs1.z)
    for loc in [pcbs1, pcbs2, pcbs3, pcbs4]:
        chassis = T.tap(chassis, loc, *pcbsargs)

    # Caster wheel screws
    cwsargs = (
        V(0, 0, 1),
        CASTER_SCREW_THREAD_DIA,
        4 * BODY_THICKNESS,
        CASTER_SCREW_HEAD_DIA,
        2
    )

    cws1 = V(
        p5.x - CASTER_SCREW_HSEP / 2,
        pcbs2.y - CASTER_PCB_SCREW_VSEP,
        p0.z + BODY_THICKNESS
    )
    cws2 = V(cws1.x + CASTER_SCREW_HSEP, cws1.y, cws1.z)
    cws3 = V(cws2.x, cws2.y - CASTER_SCREW_VSEP, cws2.z)
    cws4 = V(cws1.x, cws3.y, cws3.z)
    for loc in [cws1, cws2, cws3, cws4]:
        chassis = T.tap(chassis, loc, *cwsargs)

    Part.show(chassis, 'chassis')
    doc.saveAs('chassis.FCStd')

if __name__ == '__main__':
    main()




