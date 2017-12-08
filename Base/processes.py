#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 16:51:52 2017

@author: xidong.zhang@wenba100.com

"""

import re
import jieba
import json


def extract_question_options(x):
    try:
        return "\t".join([v[u'detail'] for v in json.loads(x)])
    except:
        return u''

extract_chinese = lambda x: "\t".join(re.findall(u'[\u4e00-\u9fa5]+', x))

#segment_sentence = lambda x: "\t".join(["\t".join(jieba.cut(sentence)) for sentence in x.split('\t')])

def segment_sentence(x):
    """
    "\t".join(["\t".join(jieba.cut(sentence)) for sentence in x.split('\t')])
    """
    step1 = re.compile(' +')
    step2 = re.compile(' [0-9](?=[A-Z])')
    try:
        words = " ".join([" ".join(jieba.cut(sentence)) for sentence in x.split('\t')])
        words = step1.sub(' ', words)
        words = step2.sub(' ', words)
        return words
    except Exception, e:
        return x