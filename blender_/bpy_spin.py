import numpy as np
import bpy
import bmesh
from bmesh.ops import spin
import bpy_aarwild_280 as A
import os

# Global constants
D = bpy.data
C = bpy.context
METER_PER_INCH = .0254


def make_shape_from_rz(rz_mtx, filename_blend=None, filename_dae=None):    
    r = rz_mtx[:, 0]
    z = rz_mtx[:, 1]
    n_points = rz_mtx.shape[0]

    # Convert r and z to inches
    z *= METER_PER_INCH
    r *= METER_PER_INCH

    # Generate vertices and edges
    vertices = [(r[i], 0, z[i]) for i in range(n_points)]
    edges = [(i, i + 1) for i in range(n_points - 1)]
    faces = []

    # Create new mesh
    mesh = D.meshes.new('mesh')
    mesh.from_pydata(vertices, edges, faces)

    # Create new blender object and assign the mesh
    obj = D.objects.new('part', mesh)
    C.scene.collection.objects.link(obj)

    # Create new bmesh object for low-level 
    # mesh manipulation
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    axis = (0, 0, 1)
    dvec = (0, 0, 0)
    angle = 2 * np.pi
    steps = 32
    center = obj.location
    geom = bm.verts[:] + bm.edges[:]
    spin(bm, geom=geom, cent=center, axis=axis, dvec=dvec, 
         angle=angle, steps=steps)

    bm.to_mesh(obj.data)
    obj.data.update()

    # Scale globally so that height is 12 inches.
    scale_factor = 12.0 * METER_PER_INCH / obj.dimensions.z
    A.scale(obj, scale_factor)

    # Recalculate normals
    A.recalculate_normals(obj)

    # Apply solid modifier
    thickness = 0.1 * METER_PER_INCH
    modifier_name = 'solidify_1'
    A.applymod_solidify(obj, thickness, modifier_name)

    # Save blend file
    if filename_blend and filename_blend.endswith('.blend'):
        A.write_blendfile(filename_blend)

    # Save dae file
    if filename_dae and filename_dae.endswith('.dae'):
        A.export_dae(filename_dae)


def main():
    A.delete_default_objects()
    A.change_units_to_inches()
    
    base_dir = '/Users/rohan/work/code/learning/cv/rz_curves'
    output_dir = './lampshades'

    for f in sorted(os.listdir(base_dir)):
        # Delete all previous objects
        objects = [o.name for o in D.objects]
        A.delete_objects(objects)

        # Create next object and save
        npy_file = os.path.join(base_dir, f)
        rz_mat = np.load(npy_file)
        basename, extn = os.path.splitext(f)
        filename_blend = os.path.join(output_dir, basename + '.blend')
        filename_dae = os.path.join(output_dir, basename + '.dae')
        make_shape_from_rz(rz_mat, filename_blend, filename_dae)


if __name__ == '__main__':
    main()