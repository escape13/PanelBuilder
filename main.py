# addon info
bl_info = {
    'name' : 'Panel Builider',
    'blender': (2, 82, 0),
    'category': 'Add Mesh',
    'location': 'View3D > Add > Mesh',
    'version': (1, 0, 0),
    'author': 'Timur Valeev'
}

import bpy
import bmesh

# add 'Add Panels' to Menu
class MENU_MT_MyCustom(bpy.types.Menu):
    bl_label = 'Add Panels'
    bl_idname = 'MENU_MT_my_custom_menu'

    def draw(self, context):
        layout = self.layout
        layout.operator(AddMeshPanel.bl_idname, icon = 'MESH_CUBE')

# add plugin section to menu
def MyCustomMenuAdd(self, context):
    self.layout.menu(MENU_MT_MyCustom.bl_idname, icon = 'PLUGIN')

# addon class
class AddMeshPanel(bpy.types.Operator):
    # addon initialize
    bl_idname = 'mesh.add_panel'
    bl_label = 'Panelled Walls'
    bl_options = {'REGISTER', 'UNDO'}
    # user-input variables
    num_x : bpy.props.IntProperty(name="Panels X Axis", description="Number of panels over the X axis", default=4, min=1, max=300)
    num_y : bpy.props.IntProperty(name="Panels Y Axis", description="Number of panels over the Y axis", default=3, min=1, max=300)
    num_z : bpy.props.IntProperty(name="Panels Z Axis", description="Number of panels over the Z axis", default=3, min=1, max=300)
    padding_hor : bpy.props.FloatProperty(name="Horizontal Padding", description="Padding between horizontal panels", default=0.05, min=0, max=1)
    padding_vert : bpy.props.FloatProperty(name="Vertical Padding", description="Padding between vertical panels", default=0.05, min=0, max=1)
    scale_x : bpy.props.FloatProperty(name="Panel X scale", description="X scale of a panel unit", default=0.05, min=0.001, max=100)
    scale_y : bpy.props.FloatProperty(name="Panel Y scale", description="Y scale of a panel unit", default=1, min=0.001, max=100)
    scale_z : bpy.props.FloatProperty(name="Panel Z scale", description="Z scale of a panel unit", default=0.5, min=0.001, max=100)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location
        # main cycle adding 4 walls
        for i in range(4):
            # adding a cube
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=cursor)
            # resizing the cube
            bpy.ops.transform.resize(value=(self.scale_x, self.scale_y, self.scale_z))
            # enter edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            # deselect everything
            bpy.ops.mesh.select_all(action = 'DESELECT')
            # change selection to edges
            bpy.context.tool_settings.mesh_select_mode = (False, True, False)
            # assign created object to obj
            obj = bpy.context.active_object
            # assign obj data to bm
            bm = bmesh.from_edit_mesh(obj.data)
            # selecting right-side edge
            for edge in bm.edges:
                if (edge.index == 3):
                    edge.select = True
                    continue
                edge.select = False
            # extruding selected edge by amount specified in user-input
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, self.padding_hor*self.scale_y*2, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            # selecting back top edges
            bpy.ops.mesh.select_all(action = 'DESELECT')
            for edge in bm.edges:
                if (edge.index == 2 or edge.index == 13):
                    edge.select = True
                    continue
                edge.select = False
            # extruding selected edges by amount specified in user-input
            bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, self.padding_vert*self.scale_z*2), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
            # go to object mode
            bpy.ops.object.editmode_toggle()
            # adding horizontal array according to amount specified in user-input
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 1
            bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0
            if (i == 0 or i == 2):
                bpy.context.object.modifiers["Array"].count = self.num_x
            elif (i == 1 or i == 3):
                bpy.context.object.modifiers["Array"].count = self.num_y

            #adding vertical array according to amount specified in user-input
            bpy.ops.object.modifier_add(type='ARRAY')
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0
            bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
            bpy.context.object.modifiers["Array.001"].count = self.num_z

            # parsing updated object data to obj an bm
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.context.tool_settings.mesh_select_mode = (True, False, False)
            obj = bpy.context.active_object
            bm = bmesh.from_edit_mesh(obj.data)

            # moving origin to the back-left-down vertex
            for vert in bm.verts:
                if (vert.index == 0):
                    vert.select = True
                    continue
                vert.select = False

            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.view3d.snap_cursor_to_center()
            move_x = -(self.num_y * 2 * self.scale_y + (self.num_y - 1) * 2 * self.scale_y * self.padding_hor)
            # applying horizontal array modifier
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")
            # parsing ubdated object data to obj and bm
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.context.tool_settings.mesh_select_mode = (True, False, False)
            obj = bpy.context.active_object
            bm = bmesh.from_edit_mesh(obj.data)
            # deleting right vertices
            """if (i == 0 or i == 2):
                for vert in bm.verts:
                    if (vert.index == 47 or vert.index == 48 or vert.index == 51):
                        vert.select = True
                        continue
                    vert.select = False
            elif (i == 1 or i == 3):
                for vert in bm.verts:
                    if (vert.index == 34 or vert.index == 35 or vert.index == 38):
                        vert.select = True
                        continue
                    vert.select = False
            bpy.ops.mesh.delete(type='VERT')
            # go to object mode
            bpy.ops.object.editmode_toggle()
            """



        return {'FINISHED'}


classes = (
    MENU_MT_MyCustom,
    AddMeshPanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(MyCustomMenuAdd)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.VIEW3D_MT_mesh_add.remove(MyCustomMenuAdd)

if __name__ == "__main__":
    register()
