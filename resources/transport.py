import os

files_we_need = []
files = os.listdir('/home/petya/Downloads/blender/glass_russian_alphabet_1/')
for file in files:
    if file.endswith('.blend'):
        files_we_need.append(file)
        print(file[:-1])
        os.system(f'cp /home/petya/Downloads/blender/glass_russian_alphabet_1/{file} '
                  f'/home/petya/PycharmProjects/glass-captcha/cyrillic_alphabet/{file}')
print(sorted(files_we_need))
