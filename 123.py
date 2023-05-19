import bpy

bpy.ops.wm.open_mainfile(filepath='close_to_success_4.blend')
print(bpy.data.collections['Collection'].all_objects.values())
bpy.ops.render.render(write_still=True)
