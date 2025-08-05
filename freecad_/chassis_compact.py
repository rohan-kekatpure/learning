import sys
sys.path.append('/Applications/FreeCAD.app/Contents/Resources/lib')

import FreeCAD
import Part
from FreeCAD import Vector as V

import transformlib as T

def main():
    doc = App.newDocument('chassis')

    # Dimensions
    MARGIN = 25
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
    CASTER_PCB_SCREW_VSEP = -5

    WHEEL_DIA = 66
    GEARBOX_AXLE_DIA = 7.5
    GEARBOX_SCREW_DIA = 3
    GEARBOX_BLINDHOLE_DIA = 4
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

    lw1 = p2
    lw2 = V(lw1.x, lw1.y, lw1.z - BED_ELEVATION)
    lw3 = V(lw2.x, lw2.y + PCB_SCREW_VSPACING / 2, lw2.z)
    lw4 = p3
    lwhlpoints = [lw1, lw2, lw3, lw4]
    lwhlface = T.make_face_from_points(lwhlpoints)
    lwhlattach = lwhlface.extrude(V(-1, 0, 0) * BODY_THICKNESS)
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
    chassis = T.tap(
        chassis,
        gbx_left_s1,
        V(-1, 0, 0),
        GEARBOX_SCREW_DIA,
        BODY_THICKNESS
    )

    gbx_left_s2 = V(
        gbx_left_s1.x,
        gbx_left_s1.y,
        gbx_left_s1.z - GEARBOX_SCREW_SEP
    )
    chassis = T.tap(
        chassis,
        gbx_left_s2,
        V(-1, 0, 0),
        GEARBOX_SCREW_DIA,
        BODY_THICKNESS
    )

    gbx_left_axle = V(
        gbx_left_s1.x,
        gbx_left_s1.y + GEARBOX_AXLE_SCREW_HSEP,
        gbx_left_s1.z - GEARBOX_AXLE_SCREW_VSEP
    )
    chassis = T.tap(
        chassis,
        gbx_left_axle,
        V(-1, 0, 0),
        GEARBOX_AXLE_DIA,
        BODY_THICKNESS
    )


    gbx_left_blindhole = V(
        gbx_left_axle.x,
        gbx_left_axle.y - 11,
        0.5 * (gbx_left_s1.z + gbx_left_s2.z)
    )
    chassis = T.tap(
        chassis,
        gbx_left_blindhole,
        V(-1, 0, 0),
        GEARBOX_BLINDHOLE_DIA,
        0.5 * BODY_THICKNESS
    )

    gbx_right_axle = V(
        -p2.x,
        gbx_left_axle.y,
        gbx_left_axle.z
    )
    chassis = T.tap(
        chassis,
        gbx_right_axle,
        V(1, 0, 0),
        GEARBOX_AXLE_DIA,
        BODY_THICKNESS
    )

    gbx_right_s1 = V(
        gbx_right_axle.x,
        gbx_left_s1.y,
        gbx_left_s1.z
    )
    chassis = T.tap(
        chassis,
        gbx_right_s1,
        V(1, 0, 0),
        GEARBOX_SCREW_DIA,
        BODY_THICKNESS
    )

    gbx_right_s2 = V(
        gbx_right_axle.x,
        gbx_left_s2.y,
        gbx_left_s2.z
    )
    chassis = T.tap(
        chassis,
        gbx_right_s2,
        V(1, 0, 0),
        GEARBOX_SCREW_DIA,
        BODY_THICKNESS
    )

    gbx_right_blindhole = V(
        gbx_right_axle.x,
        gbx_left_blindhole.y,
        gbx_left_blindhole.z
    )
    chassis = T.tap(
        chassis,
        gbx_right_blindhole,
        V(1, 0, 0),
        GEARBOX_BLINDHOLE_DIA,
        0.5 * BODY_THICKNESS
    )

    # PCB screws
    pcbsargs = (
        V(0, 0, -1),
        PCB_SCREW_DIA,
        BODY_THICKNESS
    )

    pcbs1 = V(p0.x - PCB_SCREW_HSPACING / 2, p2.y, p0.z + BODY_THICKNESS)
    pcbs2 = V(pcbs1.x, pcbs1.y + PCB_SCREW_VSPACING, pcbs1.z)
    pcbs3 = V(pcbs2.x + PCB_SCREW_HSPACING, pcbs2.y, pcbs2.z)
    pcbs4 = V(pcbs1.x + PCB_SCREW_HSPACING, pcbs1.y, pcbs1.z)
    for loc in [pcbs1, pcbs2, pcbs3, pcbs4]:
        chassis = T.tap(chassis, loc, *pcbsargs)

    # Caster wheel screws and caster buffer
    cwsargs = (
        V(0, 0, -1),
        CASTER_SCREW_THREAD_DIA,
        BODY_THICKNESS,
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

    caster_buffer_DX = CASTER_SCREW_HSEP + 2 # TODO: make a constant
    caster_buffer_DY = CASTER_SCREW_VSEP + 2 # TODO: make a constant
    caster_buffer_DZ = h = WHEEL_DIA / 2 +abs(gbx_left_axle.z) - CASTER_HT

    caster_buffer_origin = V(
        cws4.x,
        cws4.y,
        -caster_buffer_DZ
    )
    caster_mesa = Part.makeBox(
        caster_buffer_DX,
        caster_buffer_DY,
        caster_buffer_DZ,
        caster_buffer_origin
    )

    # chassis = chassis.fuse(caster_mesa)

    for loc in [cws1, cws2, cws3, cws4]:
        chassis = T.tap(chassis, loc, *cwsargs)

    # Bounding boxes for various components
    # Gearbox BB
    GB_DY = 70
    GB_DX = 19
    GB_DZ = 22.30
    GB_ORIGIN = V(
        p2.x,
        gbx_left_axle.y + 5 - GB_DY,
        p2.z - GB_DZ
    )
    GB_BBOX_LEFT = Part.makeBox(GB_DX, GB_DY, GB_DZ, GB_ORIGIN)
    GB_BBOX_RIGHT = T.mirror_shape(doc, GB_BBOX_LEFT, p0, V(1, 0, 0))

    # Battery
    BAT_DZ = 17
    BAT_DY = 48
    BAT_DX = 26.5
    BAT_ORIGIN = V(p0.x - BAT_DX / 2, p0.y, p0.z - BAT_DZ)
    BAT_BBOX = Part.makeBox(BAT_DX, BAT_DY, BAT_DZ, BAT_ORIGIN)

    BBOXES = (
        GB_BBOX_LEFT
        .fuse(GB_BBOX_RIGHT)
        .fuse(BAT_BBOX)
    )

    # Standins for the PCB
    standin_rad = 1.2 * PCB_SCREW_DIA / 2.
    standin_height = 10
    standin1 = Part.makeCylinder(standin_rad, standin_height, pcbs1, V(0, 0, 1))
    standin2 = Part.makeCylinder(standin_rad, standin_height, pcbs2, V(0, 0, 1))
    standin3 = Part.makeCylinder(standin_rad, standin_height, pcbs3, V(0, 0, 1))
    standin4 = Part.makeCylinder(standin_rad, standin_height, pcbs4, V(0, 0, 1))

    standins = (
        standin1
        .fuse(standin2)
        .fuse(standin3)
        .fuse(standin4)
    )

    # PCB board
    PCB_DX = 48
    PCB_DY = 96
    PCB_DZ = 2
    PCB_ORIGIN = V(
        pcbs1.x - 4.5,
        pcbs1.y - 4.5,
        standin_height + BODY_THICKNESS
    )
    PCB_BBOX = Part.makeBox(
        PCB_DX,
        PCB_DY,
        PCB_DZ,
        PCB_ORIGIN
    )

    # Wheels
    WHL_RAD = WHEEL_DIA / 2.0
    WHL_WIDTH = 20
    LWHL_ORIGIN = V(
        gbx_left_axle.x - BODY_THICKNESS,
        gbx_left_axle.y,
        gbx_left_axle.z
    )
    LWHL = Part.makeCylinder(
        WHL_RAD,
        WHL_WIDTH,
        LWHL_ORIGIN,
        V(-1, 0, 0)
    )

    RWHL = T.mirror_shape(doc, LWHL, p0, V(1, 0, 0))

    WHEELS_BBOX = LWHL.fuse(RWHL)

    # Assemble everything
    Part.show(chassis, 'CHASSIS')
    Part.show(BBOXES, 'BOUNDING_BOXES')
    Part.show(standins, 'STANDINS')
    Part.show(PCB_BBOX, 'PCB_BBOX')
    Part.show(WHEELS_BBOX, 'WHEELS')
    doc.saveAs('chassis.FCStd')

if __name__ == '__main__':
    main()




