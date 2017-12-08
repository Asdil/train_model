# -*- coding: utf-8 -*-
import os.path
pwd = os.path.dirname(__file__)
forbid = ['.sock', '.log', '.pid', '.cache', 'matrix_points_log']
def file_name(file_dir):
    for files in os.walk(file_dir):
        file_list = files[2]
        break
    for file in file_list:
        flag = True
        for each in forbid:
            if file.find(each) != -1:
                flag = False
                break
        if flag:
            if os.path.exists(file_dir+'/'+file):
                os.remove(file_dir+'/'+file)
