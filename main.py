bl_info = {
    "name" : "Cursor Array",
    "blender" : (2, 80, 2),
    "category" : "Object"
}

import bpy

class ObjectCursorArray(bpy.types.Operator):
    bl_idname = "object.cursor_array"
    bl_label = "Cursor Array"
    bl_options = {'REGISTER', 'UNDO'}

    total: bpy.props.IntProperty(name="Steps", min=1, max=100, default=2)

    def execute(self, context):
        scene = context.scene
        cursor = scene.cursor.location
        obj = context.active_object

        for i in range(total):
            obj_new = obj.copy()
            scene.collection.objects.link(obj_new)

            factor = i / total
            obj_new.location = (factor * obj_location) + (cursor * (1 - factor))

def menu_func(self, context):
    self.layout.operator(ObjectCursorArray.bl_idname)

addon_keymaps = []

def register():
    bpy.utils.register_class(ObjectCursorArray)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    kmi = km.keymap_items.new(ObjectCursorArray.bl_idname, 'T', 'PRESS', ctrl=True, shift=True)
    kmi.properties.total = 4
    addon_keymaps.append((km, kmi))


def unregister():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(ObjectCursorArray)

if __name__ == "__main__":
    register()
