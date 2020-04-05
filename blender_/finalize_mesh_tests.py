import bpy

# Select all
bpy.ops.object.select_all(action='SELECT')

# Convert to mesh
bpy.ops.object.convert(target='MESH')
