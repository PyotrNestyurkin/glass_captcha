import bpy
import os

file_path = 'glass_alphabet/A.blend'
inner_path = 'Object'
object_name = 'A'
bpy.ops.wm.append(
    filepath=os.path.join(file_path, inner_path, object_name),
    directory=os.path.join(file_path, inner_path),
    filename='A'
)
print(bpy.data.collections['Collection'].all_objects.values())