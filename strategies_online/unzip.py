import os
import sys
import zipfile


file=zipfile.ZipFile('algo.zip',"r")
for name in file.namelist():
    utf8name=name.encode('cp437').decode('cp936')
    print("Extracting " + utf8name)
    pathname = os.path.dirname(utf8name)
    if not os.path.exists(pathname) and pathname!= "":
        os.makedirs(pathname)
    data = file.read(name)
    if not os.path.exists(utf8name):
        fo = open(utf8name, "wb")
        fo.write(data)
        fo.close     
file.close()

for i, filename in enumerate(os.listdir('D:\Desktop\Jupyter\99策略代码')):
    output = open(f'D:\Desktop\Jupyter\99策略代码\{filename}', 'r+', encoding='cp437')
    data = output.read()
    try:
        data = str(data).encode('cp437').decode('cp936')
        output.close
        new = open(f'D:\Desktop\Jupyter\99策略代码\{filename}', 'w', encoding='utf-8-sig')
        new.write(data)
        new.close
    except:
        None