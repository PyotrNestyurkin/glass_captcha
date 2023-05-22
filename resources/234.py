import bpy
import math

for o in bpy.context.scene.objects:
    if o.name == "Cube":
        bpy.ops.object.delete(use_global=False)


cam = bpy.context.scene.camera
filepath = "background.jpg"

cam.location.x = -0.71
cam.location.y = -12
cam.location.z = 5.5

cam.rotation_euler[0] = math.radians(64)
cam.rotation_euler[1] = math.radians(-0)
cam.rotation_euler[2] = math.radians(-3)

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
scale = render.resolution_percentage / 100

# FILE_NAME = "Space Monkey.png"
FILE_PATH = "Space Monkey 1.png"

# Save Previous Path
previous_path = bpy.context.scene.render.filepath

# Render Image
bpy.context.scene.render.filepath = FILE_PATH
bpy.ops.render.render(write_still=True)

# Restore Previous Path
bpy.context.scene.render.filepath = previous_path
