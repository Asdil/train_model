#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
import sys
sys.path.append('..')

type1 = ['A', 'B', 'C', 'D']
type7 = ['A', 'B', 'C', 'D', 'E', 'F']
type2 = ['①', '②', '③', '④', '⑤', '⑥']
type9 = ['times', 'surd', '错', '对', 'X', 'Ｘ', '√', '×']


def principle1(words, content):
    _words = words.strip()  # 去除两边空格
    _words = _words.replace('.', '')  # 去除.
    _words = _words.replace(' ', '')  # 去除空格

    # 首先判断是否为判断题
    if _words in type9:
        return [9.0]
    if _words.find('√') != -1 or _words.find('×') != -1 or _words.find('x') != -1:
        tmp = set(_words)  # 如果只包含√×
        if len(tmp) == 2:
            if u'√' in tmp:
                if '×' in tmp or 'x' in tmp:
                    return [9.0]
        else:
            tmp = re.match(r'(\d(√|×|x))+', str(_words)) # 如果是  1x2√ 这种形式
            if tmp != None:
                if tmp.group() == _words:
                    return [9.0]

    # 判断是否是单选题
    if len(_words) == 1 and _words in type1:
        if 'input' in content: # 如果输入端有input则是填空题
            return [2.0]
        return [1.0]

    # 判断是否是多选
    if 2 <= len(_words) <= 4:
        flag = True
        for each in _words:
            if each in type7:
                content
            else:
                flag = False
                break
        if flag:
            if 'E' in _words or 'F' in _words or 'input' in content: # 如果题干包含input E, F
                return [2.0]
            return [7.0]
        flag = True
        for each in _words:
            if each in type2:
                continue
            else:
                flag = False
                break
        if flag:
            return [2.0]
    if len(words.strip()) == 1 and 'input' in content:
        return [2.0]
    return -1


def principle2(words, label, model, i):
    if label == [9.0]:
        return model.predict([words])
    if label == [1.0]:
        return model.predict([words])
    if label == [7.0]:
        return model.predict([words])
    return -1


