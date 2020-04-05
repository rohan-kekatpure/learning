import bpy
from mathutils import Vector
import os


def create_texture_and_material(tex_name_, mat_name_, tex_img_path_):
    mat = bpy.data.materials.new(name=mat_name_)
    tex = bpy.data.textures.new(tex_name_, 'IMAGE')
    img = bpy.data.images.load(tex_img_path_)
    tex.image = img
    slot = mat.texture_slots.add()
    slot.texture = tex
    return mat

def look_at(obj, point):
    loc = obj.matrix_world.to_translation()
    direction = point - loc
    rot_quaternion = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quaternion.to_euler()    


if __name__ == '__main__':
    context = bpy.context
    scene = context.scene

    # Delete initial Cube an
    objs = [
            scene.objects['Camera'], 
            scene.objects['Lamp'],
            scene.objects['Cube'],
    ]
    bpy.ops.object.delete({"selected_objects": objs})
    
    # Create table Base 
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1.0, depth=0.5, 
                                        calc_uvs=True, location=(0, 0, 0.25))
    comp_base = context.object
    comp_base.name = 'base'

    # Create table Stem
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.35, depth=4.0, 
                                        calc_uvs=True, location=(0, 0, 2.5))
    comp_stem = context.object
    comp_stem.name = 'stem'

    # Create table Top
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=4.0, depth=0.2, 
                                        calc_uvs=True, location=(0, 0, 4.6))
    comp_top = context.object
    comp_top.name = 'top'

    file_tex_wood = 'patch_wood.png'
    file_tex_brushed_steel = 'patch_brushed_steel.png'
    file_tex_black_metal = 'patch_black_metal.jpg'

    # # Create materials
    # mat_wood = create_texture_and_material('tex_wood', 'mat_wood', file_tex_wood)
    # mat_brushed_steel = create_texture_and_material('tex_brushed_steel', 'mat_brushed_steel', file_tex_brushed_steel)
    # mat_black_metal = create_texture_and_material('tex_black_metal', 'mat_black_metal', file_tex_black_metal)

    # Assign materials to objects
    table_object = {
        'base': [comp_base, 'tex_black_metal', 'mat_black_metal', file_tex_black_metal],
        'stem': [comp_stem, 'tex_brushed_steel', 'mat_brushed_steel', file_tex_brushed_steel],
        'top': [comp_top, 'tex_wood', 'mat_wood', file_tex_wood],
    }

    for comp_name, props in table_object.items():
        comp_obj, tex_name, mat_name, tex_file = props
        mat = create_texture_and_material(tex_name, mat_name, tex_file)
        if len(comp_obj.data.materials) > 0:        
            comp_obj.data.materials[0] = mat
        else:
            comp_obj.data.materials.append(mat)


    # Add camera
    cam_loc = Vector((-20, 0, 7))
    look_at_point = Vector((-5, 0, 5))
    bpy.ops.object.camera_add(view_align=False, location=cam_loc, rotation=(0, 0, 0))
    cam_obj = context.object    
    look_at(cam_obj, look_at_point)

    # Add lamp    
    lamp_data = bpy.data.lamps.new(name="lamp", type='HEMI')
    lamp_obj = bpy.data.objects.new(name="lamp", object_data=lamp_data)
    scene.objects.link(lamp_obj)
    lamp_obj.location = cam_loc
    look_at(lamp_obj, -look_at_point)

    # Export obj
    blend_file_path = bpy.data.filepath
    directory = os.path.dirname(blend_file_path)
    target_file = os.path.join(directory, 'table.obj')
    bpy.ops.export_scene.obj(filepath=target_file, check_existing=True, axis_forward='-Z', axis_up='Y', 
                             filter_glob="*.obj;*.mtl", use_selection=False, use_animation=False, 
                             use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, 
                             use_smooth_groups_bitflags=False, use_normals=True, use_uvs=True, 
                             use_materials=True, use_triangles=False, use_nurbs=False, use_vertex_groups=False, 
                             use_blen_objects=True, group_by_object=False, group_by_material=False, 
                             keep_vertex_order=False, global_scale=1, path_mode='AUTO')


    bpy.ops.wm.save_as_mainfile(filepath="./fromscript.blend")


