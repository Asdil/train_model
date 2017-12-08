# #!/usr/bin/env python2
# # -*- coding: utf-8 -*-
import zipfile
import os

file_list = os.listdir(r'.')

for file_name in file_list:
    if os.path.splitext(file_name)[1] == '.zip':
        print file_name

        file_zip = zipfile.ZipFile(file_name, 'r')
        for file in file_zip.namelist():
            file_zip.extract(file, r'.')
        file_zip.close()
