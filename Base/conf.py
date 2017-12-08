import codecs
import os


class Config(object):
    pwd = abs_path = os.path.dirname(__file__)
    father_path = os.path.abspath(os.path.dirname(pwd))
    stop_words_path = father_path + "/StopWords/new_stop_words.txt"

    @classmethod
    def get_stop_words(cls):
        f = codecs.open(cls.stop_words_path, encoding='utf-8')
        stop_words = f.readlines()
        return stop_words