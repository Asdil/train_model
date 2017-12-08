import sys
import os
sys.path.append(os.path.dirname(__file__))
from monitor import RedisHelper


def send_model(model_name, information=None):
    obj = RedisHelper()
    f = open(model_name, 'rb')
    file_data = f.read()
    f.close()
    obj.public(model_name, file_data, information)




