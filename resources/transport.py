import os
files_we_need = []
files = os.listdir('/home/petya/Downloads/blender/glass_alphabet_without_shadows/')
for file in files:
    if file.endswith('.blend'):
        files_we_need.append(file)
        print(file[:-1])
        os.system(f'cp /home/petya/Downloads/blender/glass_alphabet_container_1/{file} '
                  f'/home/petya/Downloads/blender/glass_alphabet_container_2/{file}')
print(sorted(files_we_need))