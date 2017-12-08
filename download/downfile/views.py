# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.http import HttpResponse

pwd = os.getcwd()
father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
grand_father_path = os.path.abspath(os.path.dirname(father_path)+os.path.sep+".")

# Create your views here.
from django.http import StreamingHttpResponse


import zipfile
def zip_wrong_file(startdir):
    z = zipfile.ZipFile(father_path+'/wrong_answer.zip', 'w', zipfile.ZIP_DEFLATED, allowZip64=True)
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            z.write(os.path.join(dirpath, filename))
    z.close()

def big_file_download(request):
    # do something...
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = father_path + '/wrong_answer'
    zip_wrong_file(the_file_name)
    the_file_name = father_path + '/wrong_answer.zip'
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

def raw_df_download(request):
    # do something...
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = father_path+'/Data1/raw_df.pkl'
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


