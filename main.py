import bpy
import math
import os
from random import randint
from PIL import Image


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
        file_path = f'alphabet/{word}.blend'
        inner_path = 'Object'
        object_name = word
        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
        )
        z_pos = float(f"0.{randint(0, 1000)}")
        bpy.data.objects[word].location = (0.7 * i, 1.9 * i - 10, 2.3 + z_pos)
        bpy.data.objects[word].rotation_euler = (0, math.radians(randint(-20, 20)), math.radians(angles[i]))
    return result


def setupcamera(cam, c):
    # настройка положения камеры

    cam.rotation_euler[0] = math.radians(c[0])
    cam.rotation_euler[1] = math.radians(c[1])
    cam.rotation_euler[2] = math.radians(c[2])

    cam.location.x = c[3]
    cam.location.y = c[4]
    cam.location.z = c[5]


def render():
    # вырезание заднего фона
    img = Image.open("background.jpg")
    x_pos = randint(0, img.width - 350)
    y_pos = randint(0, img.height - 80)
    img = img.crop((x_pos, y_pos, x_pos + 350, y_pos + 80))
    img.save("tiny_background.png")

    # загрузка blend файла (камера и источник света)
    bpy.ops.wm.open_mainfile(filepath='my_scene.blend')
    captcha_key = generate_word()
    cam = bpy.context.scene.camera
    filepath = "tiny_background.png"

    setupcamera(cam, [75.8042, 0.000419, -299.221, 21.326, -13.4999, 9.32324])

    # наложение заднего фона
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

    # рендер
    FILE_PATH = "result.png"

    previous_path = bpy.context.scene.render.filepath

    bpy.context.scene.render.filepath = FILE_PATH
    bpy.ops.render.render(write_still=True)
    bpy.context.scene.render.filepath = previous_path

    return captcha_key


if __name__ == "__main__":
    print(render())
