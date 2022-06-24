import os

if not os.path.isdir('assets'):
    os.mkdir('assets')

abs_file_name = os.path.abspath('./assets/oop.txt')
file  = open(abs_file_name,'w',encoding='utf-8')
print("Hello! Python!",file=file)
file.close()