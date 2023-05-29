import os

files_we_need = []
files = os.listdir('/home/petya/Downloads/rus_alpha_5/')
for file in files:
    if file.endswith('.blend'):
        files_we_need.append(file)
        print(file[:-1])
        os.system(f'cp /home/petya/Downloads/rus_alpha_5/{file} '
                  f'/home/petya/Downloads/rus_alpha_6/{file}')
print(sorted(files_we_need))
