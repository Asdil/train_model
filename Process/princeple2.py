#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re
type1 = ['A', 'B', 'C', 'D', 'E']
type7 = re.compile(r'[A-H]+')
type9 = ['times', 'surd', '错', '对', 'X', 'Ｘ', '√', '×', '不正确', '正确']


def my_principle(test_df, lab):
    # 首先从 teach_item_type 开始
    if lab == 'teach_item_type':
        # 判断是否是判断题
        answer = test_df['answer']

        # 预处理
        answer = str(answer)
        answer = answer.strip()  # 去除两边空格
        answer = answer.replace('.', '')  # 去除.

        # 特殊情况,单选题
        # A D
        patten = re.match(r'[A-D] +[A-D]', answer)
        if patten != None:
            if patten.group() == answer:
                return [u'1']

        answer = answer.replace(' ', '')

        ### 开始使用规则 ######

        # 1.判断是否是单选
        if answer in type1:
            return [u'1']
        tmp = re.sub(r'[\d]+', ' ', answer)   # 1A2D 这种形式
        patten = re.match(r'( [A-D])+', tmp)  # 如果是
        if patten != None:
            if patten.group() == tmp:
                return [u'1']

        # 2.判断是否为判断题
        if answer in type9:
            return [u'9']
        tmp = re.sub(r'[\d]+', '', answer)
        patten = re.match(r'(√|×|x|times|正确|错误)+', tmp)
        if patten != None:
            if patten.group() == tmp:
                return [u'9']

        # 3.判断是否为多选题
        answer = answer.replace('、', '')
        if len(answer) <= 5 and len(type7.findall(answer)) == 1:
            return [u'7']

    return True

