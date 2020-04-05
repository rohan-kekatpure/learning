import bpy
import aarwild_bpy.funcs as F
from mathutils import Vector as V


F.delete_default_objects()

# Sample data
# control_point_coords = [
#     (0, 1, 0),
#     (1, 1, 0),
#     (1, 0, 0)
# ]

control_point_coords = [
    (0,  0.0, 0),
    (0.15,  0.43, 0),
    (0.30, 0.78, 0),
    (0.5, 1.0, 0)
]

# Create the curve datablock
curve_data = bpy.data.curves.new('myCurve', type='CURVE')
curve_data.dimensions = '2D'
curve_data.resolution_u = 12

# Map coords to spline
polyline = curve_data.splines.new('BEZIER')

# polyline.bezier_points.add(len(control_point_coords) - 1)
# for i, coord in enumerate(control_point_coords):
#     bezier_point = polyline.bezier_points[i]
#     bezier_point.co = coord
#     bezier_point.handle_left_type = 'AUTO'
#     bezier_point.handle_right_type = 'AUTO'

polyline.bezier_points.add(1)
polyline.bezier_points[0].co = (0, 0, 0)
polyline.bezier_points[0].handle_left = (0, 0, 0)
polyline.bezier_points[0].handle_left_type = 'FREE'
polyline.bezier_points[0].handle_right = (0.15, 0.43, 0)
polyline.bezier_points[0].handle_right_type = 'FREE'


polyline.bezier_points[1].co = (0.5, 1.0, 0)
polyline.bezier_points[1].handle_left = (0.3, 0.8, 0)
polyline.bezier_points[1].handle_left_type = 'FREE'
polyline.bezier_points[1].handle_right = (0.5, 1.0, 0)
polyline.bezier_points[1].handle_right_type = 'FREE'

# Create object
curve = bpy.data.objects.new('myCurve', curve_data)
coll = bpy.data.collections['Collection']
coll.objects.link(curve)
