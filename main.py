import bpy
import math
import os
from random import randint


def generate_word():
    # генерация текстовой составляющей и расстановка букв
    result = ''
    words = list(map(chr, range(65, 91)))
    words.remove('O')
    angles = [0, -2, -4, -7, -10, -15, -20, -25]
    for i in range(8):
        word = words[randint(0, len(words) - 1)]
        words.remove(word)
        result += word
        file_path = f'glass_alphabet_container_2/{word}.blend'
        inner_path = 'Object'
        object_name = word
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
        )
        bpy.data.objects[word].location = (0.7 * i, 1.9 * i - 10, 2.3)
        bpy.data.objects[word].rotation_euler = (0, 0, math.radians(angles[i]))
    return result


bpy.ops.wm.open_mainfile(filepath='close_to_success_8.blend')
print(generate_word())
cam = bpy.context.scene.camera
filepath = "background.jpg"


def setupcamera(c):
    # настройка положения камеры

    cam.rotation_euler[0] = math.radians(c[0])
    cam.rotation_euler[1] = math.radians(c[1])
    cam.rotation_euler[2] = math.radians(c[2])

    cam.location.x = c[3]
    cam.location.y = c[4]
    cam.location.z = c[5]


setupcamera([75.8042, 0.000419, -299.221, 21.326, -13.4999, 9.32324])

img = bpy.data.images.load(filepath)
cam.data.show_background_images = True
bg = cam.data.background_images.new()
bg.image = img
bpy.context.scene.render.film_transparent = True

bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree

for every_node in tree.nodes:
    tree.nodes.remove(every_node)

RenderLayers_node = tree.nodes.new('CompositorNodeRLayers')
RenderLayers_node.location = -300, 300

comp_node = tree.nodes.new('CompositorNodeComposite')
comp_node.location = 400, 300

AplhaOver_node = tree.nodes.new(type="CompositorNodeAlphaOver")
AplhaOver_node.location = 150, 450

Scale_node = tree.nodes.new(type="CompositorNodeScale")
bpy.data.scenes["Scene"].node_tree.nodes["Scale"].space = 'RENDER_SIZE'
Scale_node.location = -150, 500

Image_node = tree.nodes.new(type="CompositorNodeImage")
Image_node.image = img
Image_node.location = -550, 500

links = tree.links
link1 = links.new(RenderLayers_node.outputs[0], AplhaOver_node.inputs[2])
link2 = links.new(AplhaOver_node.outputs[0], comp_node.inputs[0])
link3 = links.new(Scale_node.outputs[0], AplhaOver_node.inputs[1])
link4 = links.new(Image_node.outputs[0], Scale_node.inputs[0])

### Rendering Procedure
render = bpy.context.scene.render
scale = render.resolution_percentage / 10000

FILE_PATH = "result.png"

# Save Previous Path
previous_path = bpy.context.scene.render.filepath

for mat in bpy.data.materials:
    if not mat.use_nodes:
        mat.metallic = 1
        continue
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Metallic"].default_value = 1

# Render Image

bpy.context.scene.render.filepath = FILE_PATH
bpy.ops.render.render(write_still=True)

# Restore Previous Path
bpy.context.scene.render.filepath = previous_path
