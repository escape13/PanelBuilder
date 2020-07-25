# addon info
bl_info = {
    "name": "PanelBuilder",
    "description": "Building panelled boxes and walls.",
    "author": "Timur Valeev",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "View3D > Add > Mesh",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/escape13/blender-add-on/blob/master/README.md",
    "tracker_url": "https://github.com/escape13/blender-add-on",
    "support": "COMMUNITY",
    "category": "Add Mesh",
}

import bpy
import bmesh

# add 'Add Panels' to Menu
class MENU_MT_MyCustom(bpy.types.Menu):
    bl_label = 'Panels'
    bl_idname = 'MENU_MT_my_custom_menu'

    def draw(self, context):
        layout = self.layout
        layout.operator(AddPanelledWall.bl_idname, icon = 'MESH_PLANE')
        layout.operator(AddPanelledBlock.bl_idname, icon = 'MESH_CUBE')

# add plugin section to menu
def MyCustomMenuAdd(self, context):
    self.layout.menu(MENU_MT_MyCustom.bl_idname, icon = 'PLUGIN')

# calculate rightest vertex
def rightVertex(n):
    return n * 13 - 5

# calculate highest vertex
def highestVertex(n):
    return n * 49 - 39

class AddPanelledWall(bpy.types.Operator):

    # class initialization
    bl_idname = 'mesh.add_panelledwall'
    bl_label = 'PanelledWall'
    bl_options = {'REGISTER', 'UNDO'}

    # user-input variables initialization
    num_x_n : bpy.props.IntProperty(name="Panels X Axis", description="Number of panels over the X axis", default=3, min=1, max=5000)
    num_z_n : bpy.props.IntProperty(name="Panels Z Axis", description="Number of panels over the Z axis", default=3, min=1, max=5000)
    padding_hor_n : bpy.props.FloatProperty(name="Horizontal Padding", description="Padding between horizontal panels", default=0.01, min=0, max=1)
    padding_vert_n : bpy.props.FloatProperty(name="Vertical Padding", description="Padding between vertical panels", default=0.02, min=0, max=1)
    scale_x_n: bpy.props.FloatProperty(name="Panel X scale", description="X scale of a panel unit", default=0.02, min=0.001, max=1000)
    scale_y_n : bpy.props.FloatProperty(name="Panel Y scale", description="Y scale of a panel unit", default=1, min=0.001, max=1000)
    scale_z_n : bpy.props.FloatProperty(name="Panel Z scale", description="Z scale of a panel unit", default=0.5, min=0.001, max=1000)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=cursor)
        obj = bpy.context.active_object

        # resizing the cube
        obj.name = "PanelledWall"
        bpy.ops.transform.resize(value=(self.scale_x_n, self.scale_y_n, self.scale_z_n))

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
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, self.padding_hor_n*self.scale_y_n*2, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

        # selecting back top edges
        bpy.ops.mesh.select_all(action = 'DESELECT')
        for edge in bm.edges:
            if (edge.index == 2 or edge.index == 13):
                edge.select = True
                continue
            edge.select = False

        # extruding selected edges by amount specified in user-input
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, self.padding_vert_n*self.scale_z_n*2), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

        # go to object mode
        bpy.ops.object.editmode_toggle()

        # adding horizontal array according to amount specified in user-input
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 1
        bpy.context.object.modifiers["Array"].relative_offset_displace[2] = 0
        bpy.context.object.modifiers["Array"].count = self.num_x_n

        #adding vertical array according to amount specified in user-input
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[2] = 1
        bpy.context.object.modifiers["Array.001"].count = self.num_z_n

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

        # applying horizontal array modifier
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")

        vertex1 = rightVertex(self.num_x_n)
        vertex2 = vertex1 + 1
        vertex3 = vertex2 + 3

        # parsing updated object data to obj and bm
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)

        # deleting right vertices
        for vert in bm.verts:
            if (vert.index == vertex1 or vert.index == vertex2 or vert.index == vertex3):
                vert.select = True
                continue
            vert.select = False

        bpy.ops.mesh.delete(type='VERT')

        # go to object mode
        bpy.ops.object.editmode_toggle()

        # applying vertical array modifier
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array.001")

        # positioning the wall
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        # changing the name of an object
        obj = bpy.context.active_object
        obj.name = "PanelledWall"


        return {'FINISHED'}



# addon class
class AddPanelledBlock(bpy.types.Operator):

    # addon initialize
    bl_idname = 'mesh.add_panelledblock'
    bl_label = 'PanelledBlock'
    bl_options = {'REGISTER', 'UNDO'}

    # user-input variables
    num_x : bpy.props.IntProperty(name="Panels X Axis", description="Number of panels over the X axis", default=3, min=1, max=5000)
    num_y : bpy.props.IntProperty(name="Panels Y Axis", description="Number of panels over the Y axis", default=4, min=1, max=5000)
    num_z : bpy.props.IntProperty(name="Panels Z Axis", description="Number of panels over the Z axis", default=3, min=1, max=5000)
    padding_hor : bpy.props.FloatProperty(name="Horizontal Padding", description="Padding between horizontal panels", default=0.01, min=0, max=1)
    padding_vert : bpy.props.FloatProperty(name="Vertical Padding", description="Padding between vertical panels", default=0.02, min=0, max=1)
    scale_x : bpy.props.FloatProperty(name="Panel X scale", description="X scale of a panel unit", default=0.02, min=0.001, max=1000)
    scale_y : bpy.props.FloatProperty(name="Panel Y scale", description="Y scale of a panel unit", default=1, min=0.001, max=1000)
    scale_z : bpy.props.FloatProperty(name="Panel Z scale", description="Z scale of a panel unit", default=0.5, min=0.001, max=1000)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location

        # main cycle adding 4 walls
        for i in range(4):

            # adding a cube
            bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=cursor)
            obj = bpy.context.active_object

            # resizing the cube
            obj.name = "PanelledWallElem"
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
                bpy.context.object.modifiers["Array"].count = self.num_y
            elif (i == 1 or i == 3):
                bpy.context.object.modifiers["Array"].count = self.num_x

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

            # applying horizontal array modifier
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")

            if (i == 0 or i == 2):
                vertex1 = rightVertex(self.num_y)
                vertex2 = vertex1 + 1
                vertex3 = vertex2 + 3
            elif (i == 1 or i == 3):
                vertex1 = rightVertex(self.num_x)
                vertex2 = vertex1 + 1
                vertex3 = vertex2 + 3

            # parsing updated object data to obj and bm
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.context.tool_settings.mesh_select_mode = (True, False, False)
            obj = bpy.context.active_object
            bm = bmesh.from_edit_mesh(obj.data)

            # deleting right vertices
            for vert in bm.verts:
                if (vert.index == vertex1 or vert.index == vertex2 or vert.index == vertex3):
                    vert.select = True
                    continue
                vert.select = False

            bpy.ops.mesh.delete(type='VERT')
            # go to object mode
            bpy.ops.object.editmode_toggle()

            # assembling the box
            if (i == 1):
                bpy.ops.transform.rotate(value=-1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                move_x = -(self.num_x * 2 * self.scale_y + (self.num_x - 1) * 2 * self.scale_y * self.padding_hor)
                bpy.ops.transform.translate(value=(move_x, -0, -0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            if (i == 2):
                bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                move_y = self.num_y * 2 * self.scale_y + (self.num_y - 1) * 2 * self.scale_y * self.padding_hor
                bpy.ops.transform.translate(value=(0, move_y, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                move_x = -(self.num_x * 2 * self.scale_y + (self.num_x - 1) * 2 * self.scale_y * self.padding_hor)
                bpy.ops.transform.translate(value=(move_x, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            if (i == 3):
                bpy.ops.transform.rotate(value=1.5708, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
                move_y = self.num_y * 2 * self.scale_y + (self.num_y - 1) * 2 * self.scale_y * self.padding_hor
                bpy.ops.transform.translate(value=(0, move_y, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array.001")

        # joining the elements
        bpy.ops.object.select_all(action='DESELECT')

        for o in bpy.data.objects:
            if o.name in ("PanelledWallElem", "PanelledWallElem.001", "PanelledWallElem.002", "PanelledWallElem.003"):
                o.select_set(True)

        bpy.ops.object.join()

        # renaming the elements
        obj = bpy.context.active_object
        obj.name = "PanelledBlock"

        # positioning the object
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)

        return {'FINISHED'}


classes = (
    MENU_MT_MyCustom,
    AddPanelledBlock,
    AddPanelledWall
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_mesh_add.append(MyCustomMenuAdd)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.VIEW3D_MT_mesh_add.remove(MyCustomMenuAdd)
