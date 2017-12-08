# !/usr/bin/env python2
# -*- coding: utf-8 -*-
import hashlib


def get_md5_02(file_path):
  f = open(file_path, 'rb')
  md5_obj = hashlib.md5()
  while True:
    d = f.read(8096)
    if not d:
      break
    md5_obj.update(d)
  hash_code = md5_obj.hexdigest()
  f.close()
  md5 = str(hash_code).lower()
  return md5