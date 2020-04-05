bl_info = {
    'name': 'Creating panels demonstation',
    'category': 'All'
}
 
import bpy
 
class addCubeSample(bpy.types.Operator):
    bl_idname = 'mesh.add_cube_sample'
    bl_label = 'Add Cube'
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}
 
class panel1(bpy.types.Panel):
    bl_idname = "panel.panel1"
    bl_label = "Panel1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
 
    def draw(self, context):
        self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube 1")
 
class panel2(bpy.types.Panel):
    bl_idname = "panel.panel2"
    bl_label = "Panel2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_PROPS"
 
    def draw(self, context):
        self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube 2")
 
class panel3(bpy.types.Panel):
    bl_idname = "panel.panel3"
    bl_label = "Panel3"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
 
    def draw(self, context):
        self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube 3")
 
class panel4(bpy.types.Panel):
    bl_idname = "panel.panel4"
    bl_label = "Panel4"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
 
    def draw(self, context):
        self.layout.operator("mesh.add_cube_sample", icon='MESH_CUBE', text="Add Cube 4")
 
def register() :
    bpy.utils.register_class(addCubeSample)
    bpy.utils.register_class(panel1)
    # bpy.utils.register_class(panel2)
    bpy.utils.register_class(panel3)
    bpy.utils.register_class(panel4)
 
def unregister() :
    bpy.utils.unregister_class(addCubeSample)
    bpy.utils.unregister_class(panel1)
    # bpy.utils.unregister_class(panel2)
    bpy.utils.unregister_class(panel3)
    bpy.utils.unregister_class(panel4)
 
if __name__ == "__main__" :
    register()