import os
import zipfile
pwd = os.getcwd()
father_path = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
def zip_wrong_file():
    startdir = pwd + '/wrong_answer'
    z = zipfile.ZipFile(pwd+'/wrong_answer.zip', 'w', zipfile.ZIP_DEFLATED)
    print startdir
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            z.write(os.path.join(dirpath, filename))
    z.close()
#zip_wrong_file()
