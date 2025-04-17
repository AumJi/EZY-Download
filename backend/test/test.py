# import os

# path = 'backend/app/temp_download'

# for i in os.listdir(path):
#     folder_path = os.path.join(path, i)
#     for j in os.listdir(os.path.join(folder_path)):
#         os.rename(os.path.join(folder_path,j),os.path.join(folder_path,j.split('.')[0]+ '.png'))


# title = 'sunset, car, Jirapat Wichaidit '
# lst = [ i.strip() for i in title.split(',')]
# print(lst)

# import shutil, os

# shutil.make_archive('backend/app/storage/download','zip','backend/app/storage/temp_download')

import io,os,zipfile

path = 'backend/app/storage/temp_download'

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with zipfile.ZipFile('Python.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(path, zipf)