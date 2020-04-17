import numpy as np
import bpy
import bmesh
from bmesh.ops import spin
import aarwild_bpy.funcs as A
import os

# Global constants
D = bpy.data
C = bpy.context
OPS = bpy.ops
METER_PER_INCH = .0254


def make_curve_from_coord(vlist):    
    n_points = vlist.shape[0]
    ndim = vlist.shape[1]
    # Generate vertices and edges
    if ndim == 2:
        vertices = [(v[0], v[1], 0) for v in vlist]
    elif ndim == 3:
        vertices = [(v[0], v[1], v[2]) for v in vlist]

    edges = [(i, i + 1) for i in range(n_points - 1)]
    faces = []

    # Create new mesh
    mesh = D.meshes.new('mesh')
    mesh.from_pydata(vertices, edges, faces)

    # Create new blender object and assign the mesh
    obj = D.objects.new('part', mesh)
    C.scene.collection.objects.link(obj)
    return obj


def main():
    A.delete_default_objects()
    A.change_units_to_inches()
    
    t = np.linspace(0.0, 8 * np.pi, 100)
    x = .01 * t * np.sin(t)
    y = .01 * t * np.cos(t)
    z = 0.01 * t
    vlist = np.vstack((x, y, z)).T    
    # vlist = np.vstack((x, y)).T    
    curve = make_curve_from_coord(vlist)

    OPS.mesh.primitive_circle_add(radius=0.5 * METER_PER_INCH, fill_type='NGON', vertices=32)
    xs0 = D.objects['Circle']
    xs_curr = xs0

    coll = D.collections[0]

    verts = curve.data.vertices
    nv = len(verts)    
    for i in range(nv - 1):
        v1 = verts[i].co
        v2 = verts[i + 1].co
        loc = 0.5 * (v1 + v2)

        xs_next = A.copy_to_collection(xs_curr, coll)        
        xs_next.name = 'xs_{}'.format(i)

        A.move(xs_next, loc)
        direction = v2 - v1
        src = xs_next.data.polygons[0].normal
        R = src.rotation_difference(direction)
        xs_next.rotation_euler = R.to_euler()
        xs_curr = xs_next       
    

    # Delete original curve and cross section object
    A.delete_objects([xs0.name, curve.name])
    OPS.object.select_all(action='SELECT')
    if len(D.objects) > 1:
        OPS.object.join()
    OPS.object.mode_set(mode='EDIT')        
    OPS.mesh.bridge_edge_loops(number_cuts=2)
    OPS.object.mode_set(mode='OBJECT')        


if __name__ == '__main__':
    main()
